import sys


def proper_exit() -> None:
    try:
        exit(0)
    except SystemExit:
        sys.exit(0)
