"""
noxfile
~~~~~~~

Nox configuration script
"""
# pylint: disable=resource-leakage,3rd-party-module-not-gated


import datetime
import os
import pathlib
import sys
import tempfile

# fmt: off
if __name__ == "__main__":
    sys.stderr.write(
        "Do not execute this file directly. Use nox instead, it will know how to handle this file\n"
    )
    sys.stderr.flush()
    exit(1)
# fmt: on

import nox  # isort:skip
from nox.command import CommandFailed  # isort:skip

IS_PY3 = sys.version_info > (2,)

# Be verbose when runing under a CI context
CI_RUN = (
    os.environ.get("JENKINS_URL")
    or os.environ.get("CI")
    or os.environ.get("DRONE") is not None
)
PIP_INSTALL_SILENT = CI_RUN is False
SKIP_REQUIREMENTS_INSTALL = "SKIP_REQUIREMENTS_INSTALL" in os.environ
EXTRA_REQUIREMENTS_INSTALL = os.environ.get("EXTRA_REQUIREMENTS_INSTALL")

# Global Path Definitions
REPO_ROOT = pathlib.Path(os.path.dirname(__file__)).resolve()
SITECUSTOMIZE_DIR = str(REPO_ROOT / "tests" / "support" / "coverage")
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
COVERAGE_OUTPUT_DIR = ARTIFACTS_DIR / "coverage"
IS_DARWIN = sys.platform.lower().startswith("darwin")
IS_WINDOWS = sys.platform.lower().startswith("win")
IS_FREEBSD = sys.platform.lower().startswith("freebsd")
# Python versions to run against
_PYTHON_VERSIONS = ("3", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10")

# Nox options
#  Reuse existing virtualenvs
nox.options.reuse_existing_virtualenvs = True
#  Don't fail on missing interpreters
nox.options.error_on_missing_interpreters = False

# Change current directory to REPO_ROOT
os.chdir(str(REPO_ROOT))

RUNTESTS_LOGFILE = ARTIFACTS_DIR.joinpath(
    "logs",
    "runtests-{}.log".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")),
)

# Prevent Python from writing bytecode
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def session_run_always(session, *command, **kwargs):
    """
    Patch nox to allow running some commands which would be skipped if --install-only is passed.
    """
    try:
        # Guess we weren't the only ones wanting this
        # https://github.com/theacodes/nox/pull/331
        return session.run_always(*command, **kwargs)
    except AttributeError:
        old_install_only_value = session._runner.global_config.install_only
        try:
            # Force install only to be false for the following chunk of code
            # For additional information as to why see:
            #   https://github.com/theacodes/nox/pull/181
            session._runner.global_config.install_only = False
            return session.run(*command, **kwargs)
        finally:
            session._runner.global_config.install_only = old_install_only_value


def find_session_runner(session, name, **kwargs):
    for s, _ in session._runner.manifest.list_all_sessions():
        if name not in s.signatures:
            continue
        for signature in s.signatures:
            for key, value in kwargs.items():
                param = "{}={!r}".format(key, value)
                if IS_PY3:
                    # Under Python2 repr unicode string are always "u" prefixed, ie, u'a string'.
                    param = param.replace("u'", "'")
                if param not in signature:
                    break
            else:
                return s
            continue
    session.error(
        "Could not find a nox session by the name {!r} with the following keyword arguments: {!r}".format(
            name, kwargs
        )
    )


def _create_ci_directories():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    # Allow other users to write to this directory.
    # This helps when some tests run under a different name and yet
    # they need access to this path, for example, code coverage.
    ARTIFACTS_DIR.chmod(0o777)
    COVERAGE_OUTPUT_DIR.mkdir(exist_ok=True)
    COVERAGE_OUTPUT_DIR.chmod(0o777)
    ARTIFACTS_DIR.joinpath("xml-unittests-output").mkdir(exist_ok=True)


def _get_session_python_version_info(session):
    try:
        version_info = session._runner._real_python_version_info
    except AttributeError:
        session_py_version = session_run_always(
            session,
            "python",
            "-c",
            'import sys; sys.stdout.write("{}.{}.{}".format(*sys.version_info))',
            silent=True,
            log=False,
        )
        version_info = tuple(
            int(part) for part in session_py_version.split(".") if part.isdigit()
        )
        session._runner._real_python_version_info = version_info
    return version_info


def _get_pydir(session):
    version_info = _get_session_python_version_info(session)
    if version_info < (3, 5):
        session.error("Only Python >= 3.5 is supported")
    if IS_WINDOWS and version_info < (3, 6):
        session.error("Only Python >= 3.6 is supported on Windows")
    return "py{}.{}".format(*version_info)


def _get_pip_requirements_file(session, transport, crypto=None, requirements_type="ci"):
    assert requirements_type in ("ci", "pkg")
    pydir = _get_pydir(session)

    if IS_WINDOWS:
        if crypto is None:
            _requirements_file = os.path.join(
                "requirements",
                "static",
                requirements_type,
                pydir,
                "{}-windows.txt".format(transport),
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
            _requirements_file = os.path.join(
                "requirements", "static", requirements_type, pydir, "windows.txt"
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
        _requirements_file = os.path.join(
            "requirements", "static", requirements_type, pydir, "windows-crypto.txt"
        )
        if os.path.exists(_requirements_file):
            return _requirements_file
        session.error("Could not find a windows requirements file for {}".format(pydir))
    elif IS_DARWIN:
        if crypto is None:
            _requirements_file = os.path.join(
                "requirements",
                "static",
                requirements_type,
                pydir,
                "{}-darwin.txt".format(transport),
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
            _requirements_file = os.path.join(
                "requirements", "static", requirements_type, pydir, "darwin.txt"
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
        _requirements_file = os.path.join(
            "requirements", "static", requirements_type, pydir, "darwin-crypto.txt"
        )
        if os.path.exists(_requirements_file):
            return _requirements_file
        session.error("Could not find a darwin requirements file for {}".format(pydir))
    elif IS_FREEBSD:
        if crypto is None:
            _requirements_file = os.path.join(
                "requirements",
                "static",
                requirements_type,
                pydir,
                "{}-freebsd.txt".format(transport),
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
            _requirements_file = os.path.join(
                "requirements", "static", requirements_type, pydir, "freebsd.txt"
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
        _requirements_file = os.path.join(
            "requirements", "static", requirements_type, pydir, "freebsd-crypto.txt"
        )
        if os.path.exists(_requirements_file):
            return _requirements_file
        session.error("Could not find a freebsd requirements file for {}".format(pydir))
    else:
        if crypto is None:
            _requirements_file = os.path.join(
                "requirements",
                "static",
                requirements_type,
                pydir,
                "{}-linux.txt".format(transport),
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
            _requirements_file = os.path.join(
                "requirements", "static", requirements_type, pydir, "linux.txt"
            )
            if os.path.exists(_requirements_file):
                return _requirements_file
        _requirements_file = os.path.join(
            "requirements", "static", requirements_type, pydir, "linux-crypto.txt"
        )
        if os.path.exists(_requirements_file):
            return _requirements_file
        session.error("Could not find a linux requirements file for {}".format(pydir))


def _upgrade_pip_setuptools_and_wheel(session, upgrade=True):
    if SKIP_REQUIREMENTS_INSTALL:
        session.log(
            "Skipping Python Requirements because SKIP_REQUIREMENTS_INSTALL was found in the environ"
        )
        return False

    install_command = [
        "python",
        "-m",
        "pip",
        "install",
        "--progress-bar=off",
    ]
    if upgrade:
        install_command.append("-U")
    install_command.extend(
        [
            "pip>=20.2.4,<21.2",
            "setuptools!=50.*,!=51.*,!=52.*,<59",
            "wheel",
        ]
    )
    session_run_always(session, *install_command, silent=PIP_INSTALL_SILENT)
    return True


def _install_requirements(
    session, transport, *extra_requirements, requirements_type="ci"
):
    if not _upgrade_pip_setuptools_and_wheel(session):
        return False

    # Install requirements
    requirements_file = _get_pip_requirements_file(
        session, transport, requirements_type=requirements_type
    )
    install_command = ["--progress-bar=off", "-r", requirements_file]
    session.install(*install_command, silent=PIP_INSTALL_SILENT)

    if extra_requirements:
        install_command = ["--progress-bar=off"]
        install_command += list(extra_requirements)
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

    if EXTRA_REQUIREMENTS_INSTALL:
        session.log(
            "Installing the following extra requirements because the"
            " EXTRA_REQUIREMENTS_INSTALL environment variable was set: %s",
            EXTRA_REQUIREMENTS_INSTALL,
        )
        # We pass --constraint in this step because in case any of these extra dependencies has a requirement
        # we're already using, we want to maintain the locked version
        install_command = ["--progress-bar=off", "--constraint", requirements_file]
        install_command += EXTRA_REQUIREMENTS_INSTALL.split()
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

    return True


def _run_with_coverage(session, *test_cmd, env=None):
    if SKIP_REQUIREMENTS_INSTALL is False:
        session.install(
            "--progress-bar=off", "coverage==5.2", silent=PIP_INSTALL_SILENT
        )
    session.run("coverage", "erase")
    python_path_env_var = os.environ.get("PYTHONPATH") or None
    if python_path_env_var is None:
        python_path_env_var = SITECUSTOMIZE_DIR
    else:
        python_path_entries = python_path_env_var.split(os.pathsep)
        if SITECUSTOMIZE_DIR in python_path_entries:
            python_path_entries.remove(SITECUSTOMIZE_DIR)
        python_path_entries.insert(0, SITECUSTOMIZE_DIR)
        python_path_env_var = os.pathsep.join(python_path_entries)

    coverage_base_env = {
        # The full path to the .coverage data file. Makes sure we always write
        # them to the same directory
        "COVERAGE_FILE": str(COVERAGE_OUTPUT_DIR / ".coverage")
    }
    if env is None:
        env = {}

    env.update(
        {
            # The updated python path so that sitecustomize is importable
            "PYTHONPATH": python_path_env_var,
            # Instruct sub processes to also run under coverage
            "COVERAGE_PROCESS_START": str(REPO_ROOT / ".coveragerc"),
        },
        **coverage_base_env,
    )

    try:
        session.run(*test_cmd, env=env)
    finally:
        # Always combine and generate the XML coverage report
        try:
            session.run("coverage", "combine", env=coverage_base_env)
        except CommandFailed:
            # Sometimes some of the coverage files are corrupt which would trigger a CommandFailed
            # exception
            pass
        # Generate report for salt code coverage
        session.run(
            "coverage",
            "xml",
            "-o",
            str(COVERAGE_OUTPUT_DIR.joinpath("salt.xml").relative_to(REPO_ROOT)),
            "--omit=tests/*",
            "--include=salt/*",
            env=coverage_base_env,
        )
        # Generate report for tests code coverage
        session.run(
            "coverage",
            "xml",
            "-o",
            str(COVERAGE_OUTPUT_DIR.joinpath("tests.xml").relative_to(REPO_ROOT)),
            "--omit=salt/*",
            "--include=tests/*",
            env=coverage_base_env,
        )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-parametrized")
@nox.parametrize("coverage", [False, True])
@nox.parametrize("transport", ["zeromq", "tcp"])
@nox.parametrize("crypto", [None, "m2crypto", "pycryptodome"])
def pytest_parametrized(session, coverage, transport, crypto):
    """
    DO NOT CALL THIS NOX SESSION DIRECTLY
    """
    # Install requirements
    if _install_requirements(session, transport):

        if crypto:
            session.run(
                "pip",
                "uninstall",
                "-y",
                "m2crypto",
                "pycrypto",
                "pycryptodome",
                "pycryptodomex",
                silent=True,
            )
            install_command = [
                "--progress-bar=off",
                "--constraint",
                _get_pip_requirements_file(session, transport, crypto=True),
            ]
            install_command.append(crypto)
            session.install(*install_command, silent=PIP_INSTALL_SILENT)

    cmd_args = [
        "--transport={}".format(transport),
    ] + session.posargs
    _pytest(session, coverage, cmd_args)


@nox.session(python=_PYTHON_VERSIONS)
@nox.parametrize("coverage", [False, True])
def pytest(session, coverage):
    """
    pytest session with zeromq transport and default crypto
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto=None,
            transport="zeromq",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-tcp")
@nox.parametrize("coverage", [False, True])
def pytest_tcp(session, coverage):
    """
    pytest session with TCP transport and default crypto
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto=None,
            transport="tcp",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-zeromq")
@nox.parametrize("coverage", [False, True])
def pytest_zeromq(session, coverage):
    """
    pytest session with zeromq transport and default crypto
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto=None,
            transport="zeromq",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-m2crypto")
@nox.parametrize("coverage", [False, True])
def pytest_m2crypto(session, coverage):
    """
    pytest session with zeromq transport and m2crypto
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto="m2crypto",
            transport="zeromq",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-tcp-m2crypto")
@nox.parametrize("coverage", [False, True])
def pytest_tcp_m2crypto(session, coverage):
    """
    pytest session with TCP transport and m2crypto
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto="m2crypto",
            transport="tcp",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-zeromq-m2crypto")
@nox.parametrize("coverage", [False, True])
def pytest_zeromq_m2crypto(session, coverage):
    """
    pytest session with zeromq transport and m2crypto
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto="m2crypto",
            transport="zeromq",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-pycryptodome")
@nox.parametrize("coverage", [False, True])
def pytest_pycryptodome(session, coverage):
    """
    pytest session with zeromq transport and pycryptodome
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto="pycryptodome",
            transport="zeromq",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-tcp-pycryptodome")
@nox.parametrize("coverage", [False, True])
def pytest_tcp_pycryptodome(session, coverage):
    """
    pytest session with TCP transport and pycryptodome
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto="pycryptodome",
            transport="tcp",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-zeromq-pycryptodome")
@nox.parametrize("coverage", [False, True])
def pytest_zeromq_pycryptodome(session, coverage):
    """
    pytest session with zeromq transport and pycryptodome
    """
    session.notify(
        find_session_runner(
            session,
            "pytest-parametrized-{}".format(session.python),
            coverage=coverage,
            crypto="pycryptodome",
            transport="zeromq",
        )
    )


@nox.session(python=_PYTHON_VERSIONS, name="pytest-cloud")
@nox.parametrize("coverage", [False, True])
def pytest_cloud(session, coverage):
    """
    pytest cloud tests session
    """
    pydir = _get_pydir(session)
    if pydir == "py3.5":
        session.error(
            "Due to conflicting and unsupported requirements the cloud tests only run on Py3.6+"
        )
    # Install requirements
    if _upgrade_pip_setuptools_and_wheel(session):
        requirements_file = os.path.join(
            "requirements", "static", "ci", pydir, "cloud.txt"
        )

        install_command = ["--progress-bar=off", "-r", requirements_file]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

    cmd_args = [
        "--run-expensive",
        "-k",
        "cloud",
    ] + session.posargs
    _pytest(session, coverage, cmd_args)


@nox.session(python=_PYTHON_VERSIONS, name="pytest-tornado")
@nox.parametrize("coverage", [False, True])
def pytest_tornado(session, coverage):
    """
    pytest tornado tests session
    """
    # Install requirements
    if _upgrade_pip_setuptools_and_wheel(session):
        _install_requirements(session, "zeromq")
        session.install(
            "--progress-bar=off", "tornado==5.0.2", silent=PIP_INSTALL_SILENT
        )
        session.install(
            "--progress-bar=off", "pyzmq==17.0.0", silent=PIP_INSTALL_SILENT
        )
    _pytest(session, coverage, session.posargs)


def _pytest(session, coverage, cmd_args):
    # Create required artifacts directories
    _create_ci_directories()

    env = {"CI_RUN": "1" if CI_RUN else "0"}

    args = [
        "--rootdir",
        str(REPO_ROOT),
        "--log-file={}".format(RUNTESTS_LOGFILE),
        "--log-file-level=debug",
        "--show-capture=no",
        "-ra",
        "-s",
        "--showlocals",
    ]
    args.extend(cmd_args)

    if CI_RUN:
        # We'll print out the collected tests on CI runs.
        # This will show a full list of what tests are going to run, in the right order, which, in case
        # of a test suite hang, helps us pinpoint which test is hanging
        session.run(
            "python", "-m", "pytest", *(args + ["--collect-only", "-qqq"]), env=env
        )

    if coverage is True:
        _run_with_coverage(
            session,
            "python",
            "-m",
            "coverage",
            "run",
            "-m",
            "pytest",
            *args,
            env=env,
        )
    else:
        session.run("python", "-m", "pytest", *args, env=env)


class Tee:
    """
    Python class to mimic linux tee behaviour
    """

    def __init__(self, first, second):
        self._first = first
        self._second = second

    def write(self, b):
        wrote = self._first.write(b)
        self._first.flush()
        self._second.write(b)
        self._second.flush()

    def fileno(self):
        return self._first.fileno()


def _lint(
    session, rcfile, flags, paths, tee_output=True, upgrade_setuptools_and_pip=True
):
    if _upgrade_pip_setuptools_and_wheel(session, upgrade=upgrade_setuptools_and_pip):
        requirements_file = os.path.join(
            "requirements", "static", "ci", _get_pydir(session), "lint.txt"
        )
        install_command = ["--progress-bar=off", "-r", requirements_file]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

    if tee_output:
        session.run("pylint", "--version")
        pylint_report_path = os.environ.get("PYLINT_REPORT")

    cmd_args = ["pylint", "--rcfile={}".format(rcfile)] + list(flags) + list(paths)

    cmd_kwargs = {"env": {"PYTHONUNBUFFERED": "1"}}

    if tee_output:
        stdout = tempfile.TemporaryFile(mode="w+b")
        cmd_kwargs["stdout"] = Tee(stdout, sys.__stdout__)

    lint_failed = False
    try:
        session.run(*cmd_args, **cmd_kwargs)
    except CommandFailed:
        lint_failed = True
        raise
    finally:
        if tee_output:
            stdout.seek(0)
            contents = stdout.read()
            if contents:
                if IS_PY3:
                    contents = contents.decode("utf-8")
                else:
                    contents = contents.encode("utf-8")
                sys.stdout.write(contents)
                sys.stdout.flush()
                if pylint_report_path:
                    # Write report
                    with open(pylint_report_path, "w") as wfh:
                        wfh.write(contents)
                    session.log("Report file written to %r", pylint_report_path)
            stdout.close()


def _lint_pre_commit(session, rcfile, flags, paths):
    if "VIRTUAL_ENV" not in os.environ:
        session.error(
            "This should be running from within a virtualenv and "
            "'VIRTUAL_ENV' was not found as an environment variable."
        )
    if "pre-commit" not in os.environ["VIRTUAL_ENV"]:
        session.error(
            "This should be running from within a pre-commit virtualenv and "
            "'VIRTUAL_ENV'({}) does not appear to be a pre-commit virtualenv.".format(
                os.environ["VIRTUAL_ENV"]
            )
        )
    from nox.virtualenv import VirtualEnv

    # Let's patch nox to make it run inside the pre-commit virtualenv
    try:
        session._runner.venv = VirtualEnv(  # pylint: disable=unexpected-keyword-arg
            os.environ["VIRTUAL_ENV"],
            interpreter=session._runner.func.python,
            reuse_existing=True,
            venv=True,
        )
    except TypeError:
        # This is still nox-py2
        session._runner.venv = VirtualEnv(
            os.environ["VIRTUAL_ENV"],
            interpreter=session._runner.func.python,
            reuse_existing=True,
        )
    _lint(
        session,
        rcfile,
        flags,
        paths,
        tee_output=False,
        upgrade_setuptools_and_pip=False,
    )


@nox.session(python="3")
def lint(session):
    """
    Run PyLint against Salt and it's test suite. Set PYLINT_REPORT to a path to capture output.
    """
    session.notify("lint-salt-{}".format(session.python))
    session.notify("lint-tests-{}".format(session.python))


@nox.session(python="3", name="lint-salt")
def lint_salt(session):
    """
    Run PyLint against Salt. Set PYLINT_REPORT to a path to capture output.
    """
    flags = ["--disable=I"]
    if session.posargs:
        paths = session.posargs
    else:
        paths = ["setup.py", "noxfile.py", "salt/", "tasks/"]
    _lint(session, ".pylintrc", flags, paths)


@nox.session(python="3", name="lint-tests")
def lint_tests(session):
    """
    Run PyLint against Salt and it's test suite. Set PYLINT_REPORT to a path to capture output.
    """
    flags = ["--disable=I"]
    if session.posargs:
        paths = session.posargs
    else:
        paths = ["tests/"]
    _lint(session, ".pylintrc", flags, paths)


@nox.session(python=False, name="lint-salt-pre-commit")
def lint_salt_pre_commit(session):
    """
    Run PyLint against Salt. Set PYLINT_REPORT to a path to capture output.
    """
    flags = ["--disable=I"]
    if session.posargs:
        paths = session.posargs
    else:
        paths = ["setup.py", "noxfile.py", "salt/"]
    _lint_pre_commit(session, ".pylintrc", flags, paths)


@nox.session(python=False, name="lint-tests-pre-commit")
def lint_tests_pre_commit(session):
    """
    Run PyLint against Salt and it's test suite. Set PYLINT_REPORT to a path to capture output.
    """
    flags = ["--disable=I"]
    if session.posargs:
        paths = session.posargs
    else:
        paths = ["tests/"]
    _lint_pre_commit(session, ".pylintrc", flags, paths)


@nox.session(python="3")
@nox.parametrize("clean", [False, True])
@nox.parametrize("update", [False, True])
@nox.parametrize("compress", [False, True])
def docs(session, compress, update, clean):
    """
    Build Salt's Documentation
    """
    session.notify("docs-html-{}(compress={})".format(session.python, compress))
    session.notify(
        find_session_runner(
            session,
            "docs-man-{}".format(session.python),
            compress=compress,
            update=update,
            clean=clean,
        )
    )


@nox.session(name="docs-html", python="3")
@nox.parametrize("clean", [False, True])
@nox.parametrize("compress", [False, True])
def docs_html(session, compress, clean):
    """
    Build Salt's HTML Documentation
    """
    if _upgrade_pip_setuptools_and_wheel(session):
        requirements_file = os.path.join(
            "requirements", "static", "ci", _get_pydir(session), "docs.txt"
        )
        install_command = ["--progress-bar=off", "-r", requirements_file]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)
    os.chdir("doc/")
    if clean:
        session.run("make", "clean", external=True)
    session.run("make", "html", "SPHINXOPTS=-W", external=True)
    if compress:
        session.run("tar", "-cJvf", "html-archive.tar.xz", "_build/html", external=True)
    os.chdir("..")


@nox.session(name="docs-man", python="3")
@nox.parametrize("clean", [False, True])
@nox.parametrize("update", [False, True])
@nox.parametrize("compress", [False, True])
def docs_man(session, compress, update, clean):
    """
    Build Salt's Manpages Documentation
    """
    if _upgrade_pip_setuptools_and_wheel(session):
        requirements_file = os.path.join(
            "requirements", "static", "ci", _get_pydir(session), "docs.txt"
        )
        install_command = ["--progress-bar=off", "-r", requirements_file]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)
    os.chdir("doc/")
    if clean:
        session.run("make", "clean", external=True)
    session.run("make", "man", "SPHINXOPTS=-W", external=True)
    if update:
        session.run("rm", "-rf", "man/", external=True)
        session.run("cp", "-Rp", "_build/man", "man/", external=True)
    if compress:
        session.run("tar", "-cJvf", "man-archive.tar.xz", "_build/man", external=True)
    os.chdir("..")


@nox.session(name="invoke", python="3")
def invoke(session):
    """
    Run invoke tasks
    """
    if _upgrade_pip_setuptools_and_wheel(session):
        _install_requirements(session, "zeromq")
        requirements_file = os.path.join(
            "requirements", "static", "ci", _get_pydir(session), "invoke.txt"
        )
        install_command = ["--progress-bar=off", "-r", requirements_file]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

    cmd = ["inv"]
    files = []

    # Unfortunately, invoke doesn't support the nargs functionality like argpase does.
    # Let's make it behave properly
    for idx, posarg in enumerate(session.posargs):
        if idx == 0:
            cmd.append(posarg)
            continue
        if posarg.startswith("--"):
            cmd.append(posarg)
            continue
        files.append(posarg)
    if files:
        cmd.append("--files={}".format(" ".join(files)))
    session.run(*cmd)


@nox.session(name="changelog", python="3")
@nox.parametrize("draft", [False, True])
@nox.parametrize("force", [False, True])
def changelog(session, draft, force):
    """
    Generate salt's changelog
    """
    if _upgrade_pip_setuptools_and_wheel(session):
        requirements_file = os.path.join(
            "requirements", "static", "ci", _get_pydir(session), "changelog.txt"
        )
        install_command = ["--progress-bar=off", "-r", requirements_file]
        session.install(*install_command, silent=PIP_INSTALL_SILENT)

    town_cmd = ["towncrier", "--version={}".format(session.posargs[0])]
    if draft:
        town_cmd.append("--draft")
    if force:
        # Do not ask, just remove news fragments
        town_cmd.append("--yes")
    session.run(*town_cmd)
