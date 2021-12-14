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

        registers = self.__load_registers()
        
        params = ["U1:ID1:R0:DO0", "U1:ID1:R0:DO1", "U1:ID1:R0:DI0", "U1:ID1:R0:DI1"]

        controller.init()

        controller.digital_write(params[0], True)
        controller.update()
        time.sleep(1)
        controller.digital_write(params[0], False)
        controller.update()
        time.sleep(1)
        controller.digital_write(params[1], True)
        controller.update()
        time.sleep(1)
        controller.digital_write(params[1], False)
        controller.update()
        time.sleep(1)
        state = controller.digital_read(params[2])
        controller.update()
        self.assertFalse(state)
        time.sleep(1)
        state = controller.digital_read(params[3])
        controller.update()
        self.assertFalse(state)

if __name__ == "__main__":
    unittest.main()
