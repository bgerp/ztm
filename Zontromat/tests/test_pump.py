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

import sys
import unittest
import os
import time

import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.settings import ApplicationSettings

from devices.factories.pump.pump_factory import PumpFactory

from controllers.controller_factory import ControllerFactory

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
            registers = Registers.from_csv(file_path)

        elif os.name == "nt":
            registers = Registers.from_csv("registers.csv")

        return registers

    def test_valve(self):

        settings = ApplicationSettings.get_instance()

        controller = ControllerFactory.create(settings.controller)

        controller.init()

        registers = self.__load_registers()

        params = ["Grundfos", "MAGNA1_80_100_F_360_1x230V_PN6", "0"]
        pump = PumpFactory.create(
            name="GRUNFOS",
            controller=controller,
            params=params)

        # Initialise the object.
        pump.init()

        # Set to calibrate state.
        self.assertFalse(pump.is_calibrating)
        pump.calibrate()
        self.assertTrue(pump.is_calibrating)

        # Calibarate
        while pump.is_calibrating:
            controller.update()
            pump.update()

        # Test the pump in several debits.
        # debits = [0, 25, 50, 75, 100, 75, 50, 25, 0, 100]
        # debits = [0, 50, 0, 50, 0, 50, 0, 50, 0]
        # debits = [100]
        # debits = [0]
        # debits = [0, 50, 0, 50, 0]
        debits = [0, 100, 0]
        for debit in debits:

            # Go to debit.
            pump.target_position = debit
            while pump.current_position != pump.target_position:
                controller.update()
                pump.update()
            
            # Assert debit.
            self.assertTrue(pump.target_position == debit)

            # Wait...
            time.sleep(1)

        # Shutdown the pump.
        pump.shutdown()


    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

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

        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == "__main__":
    unittest.main()