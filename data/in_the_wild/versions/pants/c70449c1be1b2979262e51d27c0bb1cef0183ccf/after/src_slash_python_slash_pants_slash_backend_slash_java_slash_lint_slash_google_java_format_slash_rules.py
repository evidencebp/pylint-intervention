# Copyright 2021 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
import logging
from dataclasses import dataclass

from pants.backend.java.lint.google_java_format.skip_field import SkipGoogleJavaFormatField
from pants.backend.java.lint.google_java_format.subsystem import GoogleJavaFormatSubsystem
from pants.backend.java.target_types import JavaSourceField
from pants.core.goals.fmt import FmtRequest, FmtResult
from pants.core.goals.generate_lockfiles import GenerateToolLockfileSentinel
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.fs import Digest
from pants.engine.internals.native_engine import Snapshot
from pants.engine.internals.selectors import Get, MultiGet
from pants.engine.process import ProcessResult
from pants.engine.rules import collect_rules, rule
from pants.engine.target import FieldSet, Target
from pants.engine.unions import UnionRule
from pants.jvm.jdk_rules import InternalJdk, JvmProcess
from pants.jvm.resolve import jvm_tool
from pants.jvm.resolve.coursier_fetch import ToolClasspath, ToolClasspathRequest
from pants.jvm.resolve.jvm_tool import GenerateJvmLockfileFromTool
from pants.util.logging import LogLevel
from pants.util.strutil import pluralize, strip_v2_chroot_path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GoogleJavaFormatFieldSet(FieldSet):
    required_fields = (JavaSourceField,)

    source: JavaSourceField

    @classmethod
    def opt_out(cls, tgt: Target) -> bool:
        return tgt.get(SkipGoogleJavaFormatField).value


class GoogleJavaFormatRequest(FmtRequest):
    field_set_type = GoogleJavaFormatFieldSet
    name = GoogleJavaFormatSubsystem.options_scope


class GoogleJavaFormatToolLockfileSentinel(GenerateToolLockfileSentinel):
    resolve_name = GoogleJavaFormatSubsystem.options_scope


@dataclass(frozen=True)
class Setup:
    process: JvmProcess
    original_snapshot: Snapshot


@rule(level=LogLevel.DEBUG)
async def setup_google_java_format(
    request: GoogleJavaFormatRequest,
    tool: GoogleJavaFormatSubsystem,
    jdk: InternalJdk,
) -> Setup:

    lockfile_request = await Get(
        GenerateJvmLockfileFromTool, GoogleJavaFormatToolLockfileSentinel()
    )
    source_files, tool_classpath = await MultiGet(
        Get(
            SourceFiles,
            SourceFilesRequest(field_set.source for field_set in request.field_sets),
        ),
        Get(ToolClasspath, ToolClasspathRequest(lockfile=lockfile_request)),
    )

    source_files_snapshot = (
        source_files.snapshot
        if request.prior_formatter_result is None
        else request.prior_formatter_result
    )

    toolcp_relpath = "__toolcp"
    extra_immutable_input_digests = {
        toolcp_relpath: tool_classpath.digest,
    }

    maybe_java11_or_higher_options = []
    if jdk.jre_major_version >= 11:
        maybe_java11_or_higher_options = [
            "--add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED",
            "--add-exports=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED",
            "--add-exports=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED",
            "--add-exports=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED",
            "--add-exports=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED",
        ]

    args = [
        *maybe_java11_or_higher_options,
        "com.google.googlejavaformat.java.Main",
        *(["--aosp"] if tool.aosp else []),
        "--replace",
        *source_files_snapshot.files,
    ]

    process = JvmProcess(
        jdk=jdk,
        argv=args,
        classpath_entries=tool_classpath.classpath_entries(toolcp_relpath),
        input_digest=source_files_snapshot.digest,
        extra_immutable_input_digests=extra_immutable_input_digests,
        extra_nailgun_keys=extra_immutable_input_digests,
        output_files=source_files_snapshot.files,
        description=f"Run Google Java Format on {pluralize(len(request.field_sets), 'file')}.",
        level=LogLevel.DEBUG,
    )

    return Setup(process, original_snapshot=source_files_snapshot)


@rule(desc="Format with Google Java Format", level=LogLevel.DEBUG)
async def google_java_format_fmt(
    request: GoogleJavaFormatRequest, tool: GoogleJavaFormatSubsystem
) -> FmtResult:
    if tool.skip:
        return FmtResult.skip(formatter_name=request.name)
    setup = await Get(Setup, GoogleJavaFormatRequest, request)
    result = await Get(ProcessResult, JvmProcess, setup.process)
    output_snapshot = await Get(Snapshot, Digest, result.output_digest)
    return FmtResult(
        setup.original_snapshot,
        output_snapshot,
        stdout=strip_v2_chroot_path(result.stdout),
        stderr=strip_v2_chroot_path(result.stderr),
        formatter_name=request.name,
    )


@rule
def generate_google_java_format_lockfile_request(
    _: GoogleJavaFormatToolLockfileSentinel, tool: GoogleJavaFormatSubsystem
) -> GenerateJvmLockfileFromTool:
    return GenerateJvmLockfileFromTool.create(tool)


def rules():
    return [
        *collect_rules(),
        *jvm_tool.rules(),
        UnionRule(FmtRequest, GoogleJavaFormatRequest),
        UnionRule(GenerateToolLockfileSentinel, GoogleJavaFormatToolLockfileSentinel),
    ]
