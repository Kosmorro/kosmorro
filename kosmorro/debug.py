#!/usr/bin/env python3

from traceback import print_exception

show_debug_messages = False


def debug_print(what, force: bool = False):
    if not force and not show_debug_messages:
        return

    if isinstance(what, Exception):
        print_exception(type(what), value=what, tb=None)
    else:
        print("[DEBUG] %s" % what)
