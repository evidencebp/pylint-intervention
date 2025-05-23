# Copyright 2020 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
from __future__ import annotations

import os
from abc import ABC
from dataclasses import dataclass
from pathlib import PurePath
from typing import ClassVar, Iterable, Mapping, Optional, Sequence, Tuple

from pants.base.build_root import BuildRoot
from pants.engine.addresses import Addresses
from pants.engine.console import Console
from pants.engine.environment import CompleteEnvironment
from pants.engine.fs import Digest, Workspace
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.internals.native_engine import EMPTY_DIGEST
from pants.engine.process import InteractiveProcess, InteractiveProcessResult
from pants.engine.rules import Effect, Get, collect_rules, goal_rule
from pants.engine.target import FilteredTargets, Target
from pants.engine.unions import UnionMembership, union
from pants.option.global_options import GlobalOptions
from pants.option.option_types import BoolOption, StrOption
from pants.util.contextutil import temporary_dir
from pants.util.frozendict import FrozenDict
from pants.util.memo import memoized_property
from pants.util.meta import frozen_after_init


@union
@dataclass(frozen=True)
class ReplImplementation(ABC):
    """A REPL implementation for a specific language or runtime.

    Proxies from the top-level `repl` goal to an actual implementation.
    """

    name: ClassVar[str]

    targets: Sequence[Target]
    chroot: str  # Absolute path of the chroot the sources will be materialized to.

    def in_chroot(self, relpath: str) -> str:
        return os.path.join(self.chroot, relpath)

    @memoized_property
    def addresses(self) -> Addresses:
        return Addresses(t.address for t in self.targets)


class ReplSubsystem(GoalSubsystem):
    name = "repl"
    help = "Open a REPL with the specified code loadable."

    @classmethod
    def activated(cls, union_membership: UnionMembership) -> bool:
        return ReplImplementation in union_membership

    shell = StrOption(
        default=None,
        help="Override the automatically-detected REPL program for the target(s) specified.",
    )
    restartable = BoolOption(
        default=False,
        help="True if the REPL should be restarted if its inputs have changed.",
    )


class Repl(Goal):
    subsystem_cls = ReplSubsystem


@frozen_after_init
@dataclass(unsafe_hash=True)
class ReplRequest:
    digest: Digest
    args: Tuple[str, ...]
    extra_env: FrozenDict[str, str]
    append_only_caches: FrozenDict[str, str]
    run_in_workspace: bool

    def __init__(
        self,
        *,
        digest: Digest,
        args: Iterable[str],
        extra_env: Optional[Mapping[str, str]] = None,
        append_only_caches: Mapping[str, str] | None = None,
        run_in_workspace: bool = True,
    ) -> None:
        self.digest = digest
        self.args = tuple(args)
        self.extra_env = FrozenDict(extra_env or {})
        self.append_only_caches = FrozenDict(append_only_caches or {})
        self.run_in_workspace = run_in_workspace


@goal_rule
async def run_repl(
    console: Console,
    workspace: Workspace,
    repl_subsystem: ReplSubsystem,
    specified_targets: FilteredTargets,
    build_root: BuildRoot,
    union_membership: UnionMembership,
    global_options: GlobalOptions,
    complete_env: CompleteEnvironment,
) -> Repl:
    # TODO: When we support multiple languages, detect the default repl to use based
    #  on the targets.  For now we default to the python repl.
    repl_shell_name = repl_subsystem.shell or "python"
    implementations = {impl.name: impl for impl in union_membership[ReplImplementation]}
    repl_implementation_cls = implementations.get(repl_shell_name)
    if repl_implementation_cls is None:
        available = sorted(implementations.keys())
        console.print_stderr(
            f"{repr(repl_shell_name)} is not a registered REPL. Available REPLs (which may "
            f"be specified through the option `--repl-shell`): {available}"
        )
        return Repl(-1)

    with temporary_dir(root_dir=global_options.pants_workdir, cleanup=False) as tmpdir:
        repl_impl = repl_implementation_cls(targets=specified_targets, chroot=tmpdir)
        request = await Get(ReplRequest, ReplImplementation, repl_impl)

        input_digest = request.digest
        if request.run_in_workspace:
            workspace.write_digest(
                request.digest,
                path_prefix=PurePath(tmpdir).relative_to(build_root.path).as_posix(),
                # We don't want to influence whether the InteractiveProcess is able to restart. Because
                # we're writing into a temp directory, we can safely mark this side_effecting=False.
                side_effecting=False,
            )
            input_digest = EMPTY_DIGEST

        env = {**complete_env, **request.extra_env}
        result = await Effect(
            InteractiveProcessResult,
            InteractiveProcess(
                argv=request.args,
                env=env,
                input_digest=input_digest,
                run_in_workspace=request.run_in_workspace,
                restartable=repl_subsystem.restartable,
                append_only_caches=request.append_only_caches,
            ),
        )
    return Repl(result.exit_code)


def rules():
    return collect_rules()
