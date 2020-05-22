#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""

Zontromat - Zonal Electronic Automation

Copyright (C) [2020] [POLYGONTeam Ltd.]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import json

from plugins.monitoring.rule import Rule

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov, Zdravko Ivanov"]
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "or.dimitrov@polygonteam.com"
"""E-mail of the author.
@see or.dimitrov@polygonteam.com"""

__status__ = "Debug"
"""File status."""

#endregion

class Rules:
    """Entities collection"""

#region Attributes

    __rules = []
    """Entities for"""

    __on_event_cb = None
    """On event callback."""

#endregion

#region Private Methods

    def __call_event(self, intersections, rule: Rule):

        if not self.__on_event_cb is None:
            self.__on_event_cb(intersections, rule)

#endregion

#region Public Methods

    def on_event(self, callback):
        """On event registration.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        callback : obj
            Method handler.
        """

        if not callback is None:
            self.__on_event_cb = callback

    def add(self, rule: Rule):
        """Arr rule.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        rule : Rule
            Rule describing action.
        """

        self.__rules.append(rule)

    def from_file(self, file_name):
        """Load rules from file.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        file_name : str
            File path and name of the rules source.
        """

        # Load content from file.
        with open(file_name, "r") as json_file:
            js_rules = json.load(json_file)

        for js_rule in js_rules:
            self.add(Rule(js_rule["name"], js_rule["level"], js_rule["count"]))

    def to_file(self, file_name):
        """Save rules to file.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        file_name : str
            File path and name to the rules destination.
        """

        # Save content to file.
        js_rules = []
        for rule in self.__rules:
            js_rule = {"name": rule.name, "level": rule.level, "count": rule.count}
            js_rules.append(js_rule)

        formated_string = json.dumps(js_rules, indent=4, sort_keys=True)

        with open(file_name, "w") as json_file:
            json_file.write(formated_string)

    def exists(self, name):
        """Does the rule with resource name exists.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        name : str
            Name of the resource.

        Returns
        -------
        bool
            Exists or not.
        """

        exists = False

        for rule in self.__rules:
            if rule.name == name:
                exists = True
                break

        return exists

    def by_name(self, name):
        """Get rule with name.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        name : str
            Name of the resource.

        Returns
        -------
        Rule/None
            Rule with name.
        """

        exists = None

        for rule in self.__rules:
            if rule.name == name:
                exists = rule
                break

        return exists

    def check(self, registers=None):
        """Check for intersection of usage of resources.

        Parameters
        ----------
        self : Current class.
            Current class instance.

        registers : JSON object
            JSON objects of resources.

        Returns
        -------
        JSON object/None
            Intersections of resources.
        """

        if registers is None:
            return

        # Get keys.
        registers_keys = registers.keys()

        # Create array of registers unique contents.
        registers_values = []

        # Go trough all keys.
        for register_key in registers_keys:

            # Get register value.
            register_value = registers[register_key]

            # Check for existence.
            if not register_value in registers_values:

                # If it is list, we do not care.
                if isinstance(register_value, list):
                    continue

                # If it is string, and it is part of allowed registers, append.
                if isinstance(register_value, str):
                    formated_reg_val = register_value.replace("!", "")

                    # If it is not exiting then add it.
                    if self.exists(formated_reg_val):
                        registers_values.append(formated_reg_val)


        # Create array of intersections.
        intersections = dict.fromkeys(registers_values)

        # Fill in the cells with sum arrays.
        for intersection in intersections:
            intersections[intersection] = []

        # Go thought all registers fo find duplicates.
        for register in registers:

            reg_value = registers[register]
            reg_type = type(reg_value)

            # If type is string, remove !, it is used as inversion.
            if reg_type == type(""):
                reg_value = reg_value.replace("!", "")

            # We do not handle the list types.
            if reg_type == type([]):
                continue

            # If the value is part of the intersections, then append it.
            if reg_value in intersections:
                reg = {register: registers[register]}
                intersections[reg_value].append(reg)

        for intersection in intersections:

            count = len(intersections[intersection])
            rule = self.by_name(intersection)

            if rule is not None:
                if rule.count < count:
                    self.__call_event(intersections[intersection], rule)

#endregion
