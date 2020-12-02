#!/usr/bin/env python3

from setuptools import setup
from datetime import date

from kosmorrolib.version import VERSION


APP_DARWIN_IDENTIFIER = 'space.kosmorro.darwin'
EXECUTABLE_NAME = 'kosmorro'
APP_NAME = 'Kosmorro'
APP_COPYRIGHT = 'Jérôme Deuchnord © 2019-%d - GNU Affero General Public License' % date.today().year

APP = ['kosmorro-gui']
DATA_FILES = []
OPTIONS = {
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleExecutable': EXECUTABLE_NAME,
        'CFBundleIdentifier': APP_DARWIN_IDENTIFIER,
        'CFBundleShortVersionString': VERSION,
        'NSHumanReadableCopyright': APP_COPYRIGHT
    },
    'iconfile': 'build/distrib/darwin/icon.icns',
    'packages': ','.join(['wx'])
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
