import argparse
import logging
import os
import time
from typing import NamedTuple

import Quartz

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# one of required parameters for `CGGetActiveDisplayList()`, change if needed
MAX_DISPLAYS = 16
DEFAULT_SLEEP_TIME_SECONDS = 1


class DisplayInfo(NamedTuple):
    """ """
    id: int
    is_builtin: bool


def _get_all_displays() -> list[DisplayInfo]:
    """ """
    display_ids = Quartz.CGGetActiveDisplayList(16, None, None)[1]

    display_info = []
    for display_id in display_ids:
        is_builtin = bool(Quartz.CGDisplayIsBuiltin(display_id))

        display_info.append(DisplayInfo(id=display_id, is_builtin=is_builtin))
    return display_info


def get_display_info() -> list[bool, bool]:
    """Returns [is_external, is_lid_closed]"""
    all_displays = _get_all_displays()
    logger.debug(f"Got list of displays: {all_displays}")

    is_external = any(not display.is_builtin for display in all_displays)
    is_lid_closed = not any(display.is_builtin for display in all_displays)

    logger.debug(
        f"External display connected: {is_external}, Lid closed: {is_lid_closed}"
    )
    return is_external, is_lid_closed


def hide_dock():
    """ """
    os.system(
        "osascript -e 'tell application \"System Events\" to set the autohide of the dock preferences to true'"
    )


def show_dock():
    """ """
    os.system(
        "osascript -e 'tell application \"System Events\" to set the autohide of the dock preferences to false'"
    )


def main():
    """ """
    logger.info("Starting...")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=DEFAULT_SLEEP_TIME_SECONDS,
        help="Interval between checks",
    )
    parser.add_argument(
        "-l",
        "--closed-lid",
        action="store_true",
        default=False,
        help="Show dock only when the lid is closed",
    )
    args = parser.parse_args()

    last_state = None
    while True:
        is_external, is_lid_closed = get_display_info()

        if (is_external, is_lid_closed) != last_state:
            logger.info(f"External display state changed to is_external={is_external}")
            if is_external:
                if args.closed_lid:
                    if is_lid_closed:
                        show_dock()
                    else:
                        hide_dock()
                else:
                    show_dock()
            else:
                hide_dock()

        last_state = (is_external, is_lid_closed)
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
