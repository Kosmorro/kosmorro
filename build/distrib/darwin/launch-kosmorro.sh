#!/bin/sh

# Move to the MacOS folder
cd $(dirname "$0")

source .venv/bin/activate
./python/bin/python3 kosmorro --gui
