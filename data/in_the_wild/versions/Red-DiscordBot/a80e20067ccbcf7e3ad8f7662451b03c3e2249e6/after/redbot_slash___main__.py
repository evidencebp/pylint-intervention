#!/usr/bin/env python

# Discord Version check

import asyncio
import functools
import getpass
import json
import logging
import os
import pip
import platform
import shutil
import signal
import sys
from argparse import Namespace
from copy import deepcopy
from pathlib import Path

import discord

# Set the event loop policies here so any subsequent `get_event_loop()`
# calls, in particular those as a result of the following imports,
# return the correct loop object.
from redbot import _update_event_loop_policy, __version__

_update_event_loop_policy()

import redbot.logging
from redbot.core.bot import Red
from redbot.core.cli import interactive_config, confirm, parse_cli_flags
from redbot.setup import get_data_dir, get_name, save_config
from redbot.core import data_manager, drivers
from redbot.core._sharedlibdeprecation import SharedLibImportWarner


log = logging.getLogger("red.main")

#
#               Red - Discord Bot v3
#
#         Made by Twentysix, improved by many
#


def _get_instance_names():
    with data_manager.config_file.open(encoding="utf-8") as fs:
        data = json.load(fs)
    return sorted(data.keys())


def list_instances():
    if not data_manager.config_file.exists():
        print(
            "No instances have been configured! Configure one "
            "using `redbot-setup` before trying to run the bot!"
        )
        sys.exit(1)
    else:
        text = "Configured Instances:\n\n"
        for instance_name in _get_instance_names():
            text += "{}\n".format(instance_name)
        print(text)
        sys.exit(0)


def debug_info():
    """Shows debug information useful for debugging."""
    if sys.platform == "linux":
        import distro  # pylint: disable=import-error

    IS_WINDOWS = os.name == "nt"
    IS_MAC = sys.platform == "darwin"
    IS_LINUX = sys.platform == "linux"

    pyver = sys.version
    pipver = pip.__version__
    redver = __version__
    dpy_version = discord.__version__
    if IS_WINDOWS:
        os_info = platform.uname()
        osver = "{} {} (version {})".format(os_info.system, os_info.release, os_info.version)
    elif IS_MAC:
        os_info = platform.mac_ver()
        osver = "Mac OSX {} {}".format(os_info[0], os_info[2])
    else:
        os_info = distro.linux_distribution()
        osver = "{} {}".format(os_info[0], os_info[1]).strip()
    user_who_ran = getpass.getuser()
    info = (
        "Debug Info for Red\n\n"
        + "Red version: {}\n".format(redver)
        + "Python version: {}\n".format(pyver)
        + "Python executable: {}\n".format(sys.executable)
        + "Discord.py version: {}\n".format(dpy_version)
        + "Pip version: {}\n".format(pipver)
        + "OS version: {}\n".format(osver)
        + "System arch: {}\n".format(platform.machine())
        + "User: {}\n".format(user_who_ran)
    )
    print(info)
    sys.exit(0)


async def edit_instance(red, cli_flags):
    no_prompt = cli_flags.no_prompt
    token = cli_flags.token
    owner = cli_flags.owner
    old_name = cli_flags.instance_name
    new_name = cli_flags.edit_instance_name
    data_path = cli_flags.edit_data_path
    copy_data = cli_flags.copy_data
    confirm_overwrite = cli_flags.overwrite_existing_instance

    if data_path is None and copy_data:
        print("--copy-data can't be used without --edit-data-path argument")
        sys.exit(1)
    if new_name is None and confirm_overwrite:
        print("--overwrite-existing-instance can't be used without --edit-instance-name argument")
        sys.exit(1)
    if no_prompt and all(to_change is None for to_change in (token, owner, new_name, data_path)):
        print(
            "No arguments to edit were provided. Available arguments (check help for more "
            "information): --edit-instance-name, --edit-data-path, --copy-data, --owner, --token"
        )
        sys.exit(1)

    await _edit_token(red, token, no_prompt)
    await _edit_owner(red, owner, no_prompt)

    data = deepcopy(data_manager.basic_config)
    name = _edit_instance_name(old_name, new_name, confirm_overwrite, no_prompt)
    _edit_data_path(data, data_path, copy_data, no_prompt)

    save_config(name, data)
    if old_name != name:
        save_config(old_name, {}, remove=True)


async def _edit_token(red, token, no_prompt):
    if token:
        if not len(token) >= 50:
            print(
                "The provided token doesn't look a valid Discord bot token."
                " Instance's token will remain unchanged.\n"
            )
            return
        await red._config.token.set(token)
    elif not no_prompt and confirm("Would you like to change instance's token?", default=False):
        await interactive_config(red, False, True, print_header=False)
        print("Token updated.\n")


async def _edit_owner(red, owner, no_prompt):
    if owner:
        if not (15 <= len(str(owner)) <= 21):
            print(
                "The provided owner id doesn't look like a valid Discord user id."
                " Instance's owner will remain unchanged."
            )
            return
        await red._config.owner.set(owner)
    elif not no_prompt and confirm("Would you like to change instance's owner?", default=False):
        print(
            "Remember:\n"
            "ONLY the person who is hosting Red should be owner."
            " This has SERIOUS security implications."
            " The owner can access any data that is present on the host system.\n"
        )
        if confirm("Are you sure you want to change instance's owner?", default=False):
            print("Please enter a Discord user id for new owner:")
            while True:
                owner_id = input("> ").strip()
                if not (15 <= len(owner_id) <= 21 and owner_id.isdecimal()):
                    print("That doesn't look like a valid Discord user id.")
                    continue
                owner_id = int(owner_id)
                await red._config.owner.set(owner_id)
                print("Owner updated.")
                break
        else:
            print("Instance's owner will remain unchanged.")
        print()


def _edit_instance_name(old_name, new_name, confirm_overwrite, no_prompt):
    if new_name:
        name = new_name
        if name in _get_instance_names() and not confirm_overwrite:
            name = old_name
            print(
                "An instance with this name already exists.\n"
                "If you want to remove the existing instance and replace it with this one,"
                " run this command with --overwrite-existing-instance flag."
            )
    elif not no_prompt and confirm("Would you like to change the instance name?", default=False):
        name = get_name()
        if name in _get_instance_names():
            print(
                "WARNING: An instance already exists with this name. "
                "Continuing will overwrite the existing instance config."
            )
            if not confirm(
                "Are you absolutely certain you want to continue with this instance name?",
                default=False,
            ):
                print("Instance name will remain unchanged.")
                name = old_name
            else:
                print("Instance name updated.")
            print()
    else:
        name = old_name
    return name


def _edit_data_path(data, data_path, copy_data, no_prompt):
    # This modifies the passed dict.
    if data_path:
        data["DATA_PATH"] = data_path
        if copy_data and not _copy_data(data):
            print("Can't copy data to non-empty location. Data location will remain unchanged.")
            data["DATA_PATH"] = data_manager.basic_config["DATA_PATH"]
    elif not no_prompt and confirm("Would you like to change the data location?", default=False):
        data["DATA_PATH"] = get_data_dir()
        if confirm(
            "Do you want to copy the data from old location?", default=True
        ) and not _copy_data(data):
            print("Can't copy the data to non-empty location.")
            if not confirm("Do you still want to use the new data location?"):
                data["DATA_PATH"] = data_manager.basic_config["DATA_PATH"]
                print("Data location will remain unchanged.")
            else:
                print("Data location updated.")


def _copy_data(data):
    if Path(data["DATA_PATH"]).exists():
        if any(os.scandir(data["DATA_PATH"])):
            return False
        else:
            # this is needed because copytree doesn't work when destination folder exists
            # Python 3.8 has `dirs_exist_ok` option for that
            os.rmdir(data["DATA_PATH"])
    shutil.copytree(data_manager.basic_config["DATA_PATH"], data["DATA_PATH"])
    return True


async def run_bot(red: Red, cli_flags: Namespace):

    driver_cls = drivers.get_driver_class()

    await driver_cls.initialize(**data_manager.storage_details())

    redbot.logging.init_logging(
        level=cli_flags.logging_level, location=data_manager.core_data_path() / "logs"
    )

    log.debug("====Basic Config====")
    log.debug("Data Path: %s", data_manager._base_data_path())
    log.debug("Storage Type: %s", data_manager.storage_type())

    if cli_flags.edit:
        try:
            edit_instance(red, cli_flags)
        except (KeyboardInterrupt, EOFError):
            print("Aborted!")
        finally:
            await driver_cls.teardown()
        sys.exit(0)

    # lib folder has to be in sys.path before trying to load any 3rd-party cog (GH-3061)
    # We might want to change handling of requirements in Downloader at later date
    LIB_PATH = data_manager.cog_data_path(raw_name="Downloader") / "lib"
    LIB_PATH.mkdir(parents=True, exist_ok=True)
    if str(LIB_PATH) not in sys.path:
        sys.path.append(str(LIB_PATH))
    sys.meta_path.insert(0, SharedLibImportWarner())

    if cli_flags.token:
        token = cli_flags.token
    else:
        token = os.environ.get("RED_TOKEN", None)
        if not token:
            token = await red._config.token()

    prefix = cli_flags.prefix or await red._config.prefix()

    if not (token and prefix):
        if cli_flags.no_prompt is False:
            new_token = await interactive_config(
                red, token_set=bool(token), prefix_set=bool(prefix)
            )
            if new_token:
                token = new_token
        else:
            log.critical("Token and prefix must be set in order to login.")
            sys.exit(1)

    if cli_flags.dry_run:
        await red.http.close()
        sys.exit(0)
    try:
        await red.start(token, bot=True, cli_flags=cli_flags)
    except discord.LoginFailure:
        log.critical("This token doesn't seem to be valid.")
        db_token = await red._config.token()
        if db_token and not cli_flags.no_prompt:
            if confirm("\nDo you want to reset the token?"):
                await red._config.token.set("")
                print("Token has been reset.")


def handle_early_exit_flags(cli_flags: Namespace):
    if cli_flags.list_instances:
        list_instances()
    elif cli_flags.version:
        print(description)
        print("Current Version: {}".format(__version__))
        sys.exit(0)
    elif cli_flags.debuginfo:
        debug_info()
    elif not cli_flags.instance_name and (not cli_flags.no_instance or cli_flags.edit):
        print("Error: No instance name was provided!")
        sys.exit(1)


async def shutdown_handler(red, signal_type=None):
    if signal_type:
        log.info("%s received. Quitting...", signal_type)
        exit_code = 0
    else:
        log.info("Shutting down from unhandled exception")
        exit_code = 1
    await red.logout()
    await red.loop.shutdown_asyncgens()
    pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in pending]
    await asyncio.gather(*pending, loop=red.loop, return_exceptions=True)
    sys.exit(exit_code)


def exception_handler(red, loop, context):
    msg = context.get("exception", context["message"])
    if isinstance(msg, KeyboardInterrupt):
        # Windows support is ugly, I'm sorry
        logging.error("Received KeyboardInterrupt, treating as interrupt")
        signal_type = signal.SIGINT
    else:
        logging.critical("Caught fatal exception: %s", msg)
        signal_type = None
    loop.create_task(shutdown_handler(red, signal_type))


def main():
    cli_flags = parse_cli_flags(sys.argv[1:])
    handle_early_exit_flags(cli_flags)
    try:
        loop = asyncio.get_event_loop()

        if cli_flags.no_instance:
            print(
                "\033[1m"
                "Warning: The data will be placed in a temporary folder and removed on next system "
                "reboot."
                "\033[0m"
            )
            cli_flags.instance_name = "temporary_red"
            data_manager.create_temp_config()

        data_manager.load_basic_configuration(cli_flags.instance_name)

        red = Red(
            cli_flags=cli_flags, description=description, dm_help=None, fetch_offline_members=True
        )

        if os.name != "nt":
            # None of this works on windows, and we have to catch KeyboardInterrupt in a global handler!
            # At least it's not a redundant handler...
            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
            for s in signals:
                loop.add_signal_handler(
                    s, lambda s=s: asyncio.create_task(shutdown_handler(red, s))
                )

        exc_handler = functools.partial(exception_handler, red)
        loop.set_exception_handler(exc_handler)
        # We actually can't use asyncio.run and have graceful cleanup on Windows...
        loop.create_task(run_bot(red, cli_flags))
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    description = "Red V3"
    main()
