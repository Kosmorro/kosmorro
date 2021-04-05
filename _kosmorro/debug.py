#!/usr/bin/env python3

from traceback import print_exc

show_debug_messages = False


def debug_print(what):
    if not show_debug_messages:
        return

    if isinstance(what, Exception):
        print_exc(what)
    else:
        print("[DEBUG] %s" % what)
