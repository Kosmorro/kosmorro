#!/usr/bin/env python3

from termcolor import colored as do_color

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

KOSMORRO_VERSION = version("kosmorro")
KOSMORROLIB_VERSION = version("kosmorrolib")


global _COLORS_ACTIVATED


def set_colors_activated(activated: bool):
    global _COLORS_ACTIVATED
    _COLORS_ACTIVATED = activated


def colored(text, color=None, on_color=None, attrs=None):
    """Decorator to use colors only when they are activated"""
    if not _COLORS_ACTIVATED:
        return text

    return do_color(text, color, on_color, attrs)
