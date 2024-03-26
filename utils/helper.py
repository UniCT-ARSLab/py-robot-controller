import sys


def proper_exit() -> None:
    try:
        exit(0)  # pylint: disable=consider-using-sys-exit
    except SystemExit:
        sys.exit(0)
