#!/usr/bin/env python3

import os
import re
from pathlib import Path

CACHE_FOLDER = str(Path.home()) + "/.kosmorro-cache"


class Environment:
    def __init__(self):
        self._vars = {}

    def __set__(self, key, value):
        self._vars[key] = value

    def __getattr__(self, key):
        return self._vars[key] if key in self._vars else None

    def __str__(self):
        return self._vars.__str__()

    def __len__(self):
        return len(self._vars)


def get_env_vars() -> Environment:
    environment = Environment()

    for var in os.environ:
        if not re.search("^KOSMORRO_", var):
            continue

        [_, env] = var.split("_", 1)
        environment.__set__(env.lower(), os.getenv(var))

    return environment
