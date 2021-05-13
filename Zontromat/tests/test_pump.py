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

import unittest
import os

from devices.vendors.no_vendor_4.pump import Pump

from controllers.dummy.dummy import Dummy
from data.registers import Registers

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

    def __init__(self, methodName):
        super().__init__(methodName)

    def __load_registers(self):

        registers = None

        # Create registers.
        if os.name == "posix":
            file_path = os.path.join("..", "registers.csv")
            registers = Registers.from_CSV(file_path)

        elif os.name == "nt":
            registers = Registers.from_CSV("registers.csv")

        return registers

    def test_valve(self):

        cases = {}
        plc_cfg = {"test": self, "cases": cases}

        controller = Dummy(plc_cfg)
        registers = self.__load_registers()

        # Create test object.
        Pump.create()
        valve = Pump(name="vlv", controller=controller, registers=registers)

        # Initialise the object.
        valve.init()

        # Go to position 5.
        valve.target_position = 5
        while valve.current_position != valve.target_position:
            valve.update()

        # Go to position 0.
        valve.target_position = 0
        while valve.current_position != valve.target_position:
            valve.update()

        # Shutdown the valve.
        valve.shutdown()


    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):

        # cases = {}
        # plc_cfg = {"test": self, "cases": cases}

        # config = {}
        # config["controller"] = Dummy(plc_cfg)
        # config["key"] = "ec"
        # config["name"] = "EnergyCenter"
        # config["registers"] = []

        # plugin = EnergyCenter(config)
        # plugin.init()

        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()