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

from devices.factories.valve.valve_factory import ValveFactory

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
            registers = Registers.from_CSV(file_path)

        elif os.name == "nt":
            registers = Registers.from_CSV("registers.csv")

        return registers

    def test_valve(self):

        settings = ApplicationSettings.get_instance()

        controller = ControllerFactory.create(settings.controller)

        controller.init()

        registers = self.__load_registers()
        

        params = ["Flowx", "FLX-05F", "U1:ID6:R16:DO0", "U1:ID6:R17:DO0", "U1:ID6:R32:DI1", "U1:ID6:R32:DI0"]
        valve = ValveFactory.create(
            name="FLOWX_DIN65",
            controller=controller,
            params=params)
        
        # Initialise the object.
        valve.init()

        # Set to calibrate state.
        self.assertFalse(valve.is_calibrating)
        valve.calibrate()
        self.assertTrue(valve.is_calibrating)

        # Calibarate
        while valve.is_calibrating:
            controller.update()
            valve.update()

        # Test the valve in several positions.
        # positions = [0, 25, 50, 75, 100, 75, 50, 25, 0, 100]
        # positions = [0, 50, 0, 50, 0, 50, 0, 50, 0]
        # positions = [100]
        # positions = [0]
        # positions = [0, 50, 0, 50, 0]
        positions = [0, 100, 0]
        for position in positions:

            # Go to position.
            valve.target_position = position
            while valve.current_position != valve.target_position:
                controller.update()
                valve.update()
            
            # Assert position.
            self.assertTrue(valve.target_position == position)

            # Wait...
            time.sleep(1)

        # Shutdown the valve.
        valve.shutdown()

if __name__ == "__main__":
    unittest.main()