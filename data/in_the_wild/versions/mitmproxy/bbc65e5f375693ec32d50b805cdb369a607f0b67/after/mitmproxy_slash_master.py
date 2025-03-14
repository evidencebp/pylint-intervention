import asyncio
import traceback

from mitmproxy import addonmanager, hooks
from mitmproxy import command
from mitmproxy import eventsequence
from mitmproxy import http
from mitmproxy import log
from mitmproxy import options
from mitmproxy.net import server_spec
from . import ctx as mitmproxy_ctx


class Master:
    """
        The master handles mitmproxy's main event loop.
    """

    event_loop: asyncio.AbstractEventLoop

    def __init__(self, opts):
        self.should_exit = asyncio.Event()
        self.options: options.Options = opts or options.Options()
        self.commands = command.CommandManager(self)
        self.addons = addonmanager.AddonManager(self)
        self.log = log.Log(self)

        mitmproxy_ctx.master = self
        mitmproxy_ctx.log = self.log
        mitmproxy_ctx.options = self.options

    async def run(self) -> None:
        self.event_loop = asyncio.get_running_loop()
        self.event_loop.set_exception_handler(self._asyncio_exception_handler)
        self.should_exit.clear()

        await self.running()
        await self.should_exit.wait()

        await self.done()

    def shutdown(self):
        """
        Shut down the proxy. This method is thread-safe.
        """
        # We may add an exception argument here.
        self.event_loop.call_soon_threadsafe(self.should_exit.set)

    async def running(self) -> None:
        await self.addons.trigger_event(hooks.RunningHook())

    async def done(self) -> None:
        await self.addons.trigger_event(hooks.DoneHook())

    def _asyncio_exception_handler(self, loop, context):
        exc: Exception = context["exception"]
        if isinstance(exc, OSError) and exc.errno == 10038:
            return  # suppress https://bugs.python.org/issue43253
        self.log.error(
            "\n".join(traceback.format_exception(exc)) +
            "\nPlease lodge a bug report at:" +
            "\n\thttps://github.com/mitmproxy/mitmproxy/issues"
        )

    async def load_flow(self, f):
        """
        Loads a flow
        """

        if isinstance(f, http.HTTPFlow):
            if self.options.mode.startswith("reverse:"):
                # When we load flows in reverse proxy mode, we adjust the target host to
                # the reverse proxy destination for all flows we load. This makes it very
                # easy to replay saved flows against a different host.
                _, upstream_spec = server_spec.parse_with_mode(self.options.mode)
                f.request.host, f.request.port = upstream_spec.address
                f.request.scheme = upstream_spec.scheme

        for e in eventsequence.iterate(f):
            await self.addons.handle_lifecycle(e)
