import argparse
import logging
import logging.config
import os
import sys
import traceback
from multiprocessing import freeze_support
from pprint import pformat

# dummy import for pyinstaller
# noinspection PyUnresolvedReferences
import infection_monkey.post_breach  # noqa: F401
from common.version import get_version
from infection_monkey.config import WormConfiguration
from infection_monkey.dropper import MonkeyDrops
from infection_monkey.model import DROPPER_ARG, MONKEY_ARG
from infection_monkey.monkey import InfectionMonkey
from infection_monkey.utils.monkey_log_path import get_agent_log_path, get_dropper_log_path

logger = None

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(process)d:%(threadName)s:%(levelname)s] %(module)s.%("
            "funcName)s.%(lineno)d: %(message)s"
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "standard"},
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": None,
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}


def main():
    global logger

    if 2 > len(sys.argv):
        return True
    freeze_support()  # required for multiprocessing + pyinstaller on windows
    monkey_mode = sys.argv[1]

    if not (monkey_mode in [MONKEY_ARG, DROPPER_ARG]):
        return True

    arg_parser = argparse.ArgumentParser()
    _, monkey_args = arg_parser.parse_known_args(sys.argv[2:])

    formatted_config = pformat(WormConfiguration.hide_sensitive_info(WormConfiguration.as_dict()))
    print(f"Loaded Configuration:\n{formatted_config}")

    try:
        if MONKEY_ARG == monkey_mode:
            log_path = get_agent_log_path()
            monkey_cls = InfectionMonkey
        elif DROPPER_ARG == monkey_mode:
            log_path = get_dropper_log_path()
            monkey_cls = MonkeyDrops
        else:
            return True
    except ValueError:
        return True

    if os.path.exists(log_path):
        # If log exists but can't be removed it means other monkey is running. This usually
        # happens on upgrade
        # from 32bit to 64bit monkey on Windows. In all cases this shouldn't be a problem.
        try:
            os.remove(log_path)
        except OSError:
            pass
    LOG_CONFIG["handlers"]["file"]["filename"] = log_path
    # noinspection PyUnresolvedReferences
    LOG_CONFIG["root"]["handlers"].append("file")

    logging.config.dictConfig(LOG_CONFIG)
    logger = logging.getLogger()

    def log_uncaught_exceptions(ex_cls, ex, tb):
        logger.critical("".join(traceback.format_tb(tb)))
        logger.critical("{0}: {1}".format(ex_cls, ex))

    sys.excepthook = log_uncaught_exceptions

    logger.info(
        ">>>>>>>>>> Initializing monkey (%s): PID %s <<<<<<<<<<", monkey_cls.__name__, os.getpid()
    )

    logger.info(f"version: {get_version()}")
    logger.info(f"writing log file to {log_path}")

    monkey = monkey_cls(monkey_args)

    try:
        monkey.start()
        return True
    except Exception as e:
        logger.exception("Exception thrown from monkey's start function. More info: {}".format(e))
    finally:
        monkey.cleanup()


if "__main__" == __name__:
    if not main():
        sys.exit(1)
