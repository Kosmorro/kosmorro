#!/bin/sh

# Move to the MacOS folder
cd $(dirname "$0")

source .venv/bin/activate
.venv/bin/python kosmorro --gui
