#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import toml


class Dependency:
    def __init__(self, package: str, required_version: [str] = None):
        self.package = package
        self.required_version = required_version

    def get_setup_format(self):
        return '%s%s%s' % (self.package,
                           '=' if self.required_version is not None and len(self.required_version) == 1 else '',
                           ','.join(self.required_version) if self.required_version is not None else '')

    def __str__(self):
        return '%s%s' % (self.package,
                         (' (%s)' % ', '.join(self.required_version)) if self.required_version is not None else '')


def get_dependencies(dev: bool = False) -> [Dependency]:
    """
    Read the Pipfile and return a dictionary with the project dependencies

    :param bool dev: if true, return the development dependencies instead of the production ones. False by default.
    :return: a dictionary where the key is the name of the dependency package, and the value is the version(s) accepted.
    """
    with open('%s/../Pipfile' % os.path.dirname(__file__), mode='r') as file:
        pipfile = ''.join(file.readlines())

    packages = toml.loads(pipfile)['packages' if not dev else 'dev-packages']
    dependencies = []

    for package in packages:
        version = packages[package].split(',')
        dependencies.append(Dependency(package,
                                       version if version != ['*'] else None))

    return dependencies
