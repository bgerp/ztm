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
import unittest

from monitoring.monitoring_level import MonitoringLevel
from monitoring.rule import Rule
from monitoring.rules import Rules

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov"]
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

class TestStringMethods(unittest.TestCase):
    """Unit test of the system that is responsible for resource intersection detection."""

#region Attributes

    __rules = Rules()
    """Rules"""

    __rules_file_name = ""
    """Rules filename."""

#endregion

#region Private Methods

    def __on_event(self, intersections, rule):

        level = MonitoringLevel(rule.level)

        if level == MonitoringLevel.Debug:
            print("Debug")

        if level == MonitoringLevel.Info:
            print("Info")

        if level == MonitoringLevel.Warning:
            print("Warning")

        if level == MonitoringLevel.Error:
            print("Error")

        print(intersections)

#endregion

#region Unit Tests

    def test_export_rules(self):

        # GPIOs
        for index in range(9):
            self.__rules.add(Rule("DO{}".format(index), MonitoringLevel.Error))
            self.__rules.add(Rule("DI{}".format(index), MonitoringLevel.Warning))
            self.__rules.add(Rule("AO{}".format(index), MonitoringLevel.Error))
            self.__rules.add(Rule("AI{}".format(index), MonitoringLevel.Warning))
            self.__rules.add(Rule("RO{}".format(index), MonitoringLevel.Error))

        # 1 Wire devices
        self.__rules.add(Rule("26607314020000F8", MonitoringLevel.Info))
        self.__rules.add(Rule("28FFFCD0001703AE", MonitoringLevel.Info))
        self.__rules.add(Rule("28FFC4EE00170349", MonitoringLevel.Info))
        self.__rules.add(Rule("28FF2B70C11604B7", MonitoringLevel.Info))

        # Serial Ports
        self.__rules.add(Rule("COM4", MonitoringLevel.Error))
        self.__rules.add(Rule("COM5", MonitoringLevel.Error))

        self.__rules.to_file("C://Users//POLYGONTeam//Documents//Python//json//out_rules.json")

        self.assertEqual("foo".upper(), "FOO")

    def test_load_rules(self):

        self.__rules.from_file("C://Users//POLYGONTeam//Documents//Python//json//rules.json")

        self.assertTrue("FOO".isupper())

    def test_split(self):

        self.__rules.on_event(self.__on_event)

        registers = None

        # Load content from file.
        with open("C://Users//POLYGONTeam//Documents//Python//json//data.json", "r") as json_file:
            registers = json.load(json_file)

        self.__rules.check(registers)

        self.assertFalse("Foo".isupper())

#endregion

if __name__ == "__main__":
    unittest.main()
