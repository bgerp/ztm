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

import argparse
import os
import csv

from Zontromat.data.register import Register
from Zontromat.data.register import Scope
from Zontromat.data.registers import Registers
from Zontromat.data import verbal_const

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

#region Variables

__registers = None
"""Registers"""

#endregion

def __add_registers():
    global __registers

#region Access Control (ac)

    register = Register("ac.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Plugin enabled"
    register.range = "True/False"
    # register.update_handler = self.__access_control_enabled
    register.value = False
    __registers.append(register)

    register = Register("ac.allowed_attendees")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Allowed attendees"
    register.range = ""
    register.value = [] # {"card_id": "445E6046010080FF", "pin": "159753", "valid_until": "1595322860"}
    __registers.append(register)

    register = Register("ac.nearby_attendees")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Nearby attendees"
    register.range = ""
    register.value = [] # {"card_id": "445E6046010080FF", "ts":"1595322860"}
    __registers.append(register)

    register = Register("ac.last_minute_attendees")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Last minute attendee"
    register.range = ""
    register.value = []
    __registers.append(register)

    register = Register("ac.next_attendance")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Next attendance"
    register.range = "0.0/"
    register.value = 0.0 # 1595322860
    __registers.append(register)

    register = Register("ac.zone_occupied")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Zone occupied flag"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    # Entry card reader.
    register = Register("ac.entry_reader_1.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader enabled"
    register.range = ""
    register.value = "TERACOM/act230/2897"
    __registers.append(register)

    register = Register("ac.entry_reader_1.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port baud rate"
    register.range = "300|600|1200|2400|4800|9600|19200|38400|57600|115200"
    register.value = 9600
    __registers.append(register)

    register = Register("ac.entry_reader_1.port.name")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port name"
    register.range = ""
    if os.name == "posix":
        register.value = "/dev/ttyUSB0"
    if os.name == "nt":
        register.value = "COM5"
    __registers.append(register)

    # Exit card reader.
    register = Register("ac.exit_reader_1.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader enabled"
    register.range = ""
    register.value = "TERACOM/act230/2911"
    __registers.append(register)

    register = Register("ac.exit_reader_1.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader 1 port baud rate"
    register.range = "300|600|1200|2400|4800|9600|19200|38400|57600|115200"
    register.value = 9600
    __registers.append(register)

    register = Register("ac.exit_reader_1.port.name")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader 1 port name"
    register.range = ""
    if os.name == "posix":
        register.value = "/dev/ttyUSB0"
    if os.name == "nt":
        register.value = "COM11"
    __registers.append(register)

    #
    register = Register("ac.exit_button_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Exit button 1 input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.lock_mechanism_1.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock mechanism output"
    register.range = "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8"
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)

    register = Register("ac.time_to_open_1")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock mechanism time to open [s]"
    register.range = "0/60"
    register.value = 10
    __registers.append(register)

    register = Register("ac.door_closed_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door closed input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI2"
    __registers.append(register)

    register = Register("ac.door_closed_1.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door closed input state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    # Entry card reader 2.
    register = Register("ac.entry_reader_2.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader settings"
    register.range = ""
    register.value = "TERACOM/act230/2897"
    __registers.append(register)


    register = Register("ac.entry_reader_2.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port baud rate"
    register.range = "300|600|1200|2400|4800|9600|19200|38400|57600|115200"
    register.value = 9600
    __registers.append(register)

    register = Register("ac.entry_reader_2.port.name")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port name"
    register.range = ""
    if os.name == "posix":
        register.value = "/dev/ttyUSB0"
    if os.name == "nt":
        register.value = "COM5"
    __registers.append(register)

    # Exit card reader.
    register = Register("ac.exit_reader_2.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader settings"
    register.range = ""
    register.value = "TERACOM/act230/2911"
    __registers.append(register)

    register = Register("ac.exit_reader_2.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port baud rate"
    register.range = "300|600|1200|2400|4800|9600|19200|38400|57600|115200"
    register.value = 9600
    __registers.append(register)

    register = Register("ac.exit_reader_2.port.name")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port name"
    register.range = ""
    if os.name == "posix":
        register.value = "/dev/ttyUSB0"
    if os.name == "nt":
        register.value = "COM11"
    __registers.append(register)

    #
    register = Register("ac.exit_button_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Exit button 2 input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.lock_mechanism_2.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock 2 mechanism output"
    register.range = "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8"
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)

    register = Register("ac.time_to_open_2")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock 2 mechanism time to open"
    register.range = "0/60"
    register.value = 10
    __registers.append(register)

    register = Register("ac.door_closed_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door 2 closed input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI2"
    __registers.append(register)

    register = Register("ac.door_closed_2.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door 2 closed input state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    #
    register = Register("ac.pir_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "PIR 1 sensor input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.pir_1.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "PIR 1 sensor input state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    register = Register("ac.pir_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "PIR 2 sensor input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.pir_2.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "PIR 2 sensor input state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    #
    register = Register("ac.window_closed_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Window 1 closed input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "!DI3"
    __registers.append(register)

    register = Register("ac.window_closed_1.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Window 1 closed input state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    register = Register("ac.window_closed_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Window 2 closed input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "!DI3"
    __registers.append(register)

    register = Register("ac.window_closed_2.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Window 2 closed input state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    # Door window blind 1.
    register = Register("ac.door_window_blind_1.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door window blind 1 output"
    register.range = "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8"
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)


    register = Register("ac.door_window_blind_1.value")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door window blind 1 value"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    # Door window blind 2.
    register = Register("ac.door_window_blind_2.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door window blind 2 output"
    register.range = "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8"
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)


    register = Register("ac.door_window_blind_2.value")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door window blind 2 value"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

#endregion

#region Blinds (blinds)

    register = Register("blinds.sun.azimuth.value")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Sun azimuth value"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.sun.azimuth.mou")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "MOU"
    register.range = "deg|rad"
    register.value = "deg"
    __registers.append(register)

    register = Register("blinds.sun.elevation.value")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Sun elevation value"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.sun.elevation.mou")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "MOU"
    register.range = "deg|rad"
    register.value = "deg"
    __registers.append(register)

    register = Register("blinds.input_fb")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Feedback input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8|AI0|AI1|AI2|AI3|AI4|AI5|AI6|AI7|AI8"
    register.value = "AI0" # "DI8"
    __registers.append(register)

    register = Register("blinds.output_ccw")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "CCW output"
    register.range = "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8"
    register.value = "DO0"
    __registers.append(register)

    register = Register("blinds.output_cw")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "CW output"
    register.range = "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8"
    register.value = "DO1"
    __registers.append(register)

    register = Register("blinds.position")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Position"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.enabled")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Plugin enabled"
    register.range = "True/False"
    # register.update_handler = self.__blinds_enabled
    register.value = False
    __registers.append(register)

#endregion

#region Monitoring (mon)

    # Cold water flow meter.
    register = Register("monitoring.cw.input")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Cold water input flow meter"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI6"
    __registers.append(register)

    register = Register("monitoring.cw.tpl")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Cold water tics per liter"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("monitoring.cw.value")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Cold water liters"
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    register = Register("monitoring.cw.leak")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Cold water leaked liters"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    # Hot water flow meter.
    register = Register("monitoring.hw.input")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Hot water input flow meter"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = verbal_const.OFF # "DI7"
    __registers.append(register)

    register = Register("monitoring.hw.tpl")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Hot water tics per liter"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("monitoring.hw.value")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Hot water liters"
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    register = Register("monitoring.hw.leak")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Hot water leaked liters"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    # Power analyser.
    register = Register("monitoring.pa.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Power analyser settings"
    register.range = ""
    register.value = "mb-rtu/Eastron/SDM630/2/3"
    __registers.append(register)

    register = Register("monitoring.pa.l1")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Power analyser L1 parameters"
    register.range = ""
    register.value = []
    __registers.append(register)

    register = Register("monitoring.pa.l2")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Power analyser L2 parameters"
    register.range = ""
    register.value = []
    __registers.append(register)

    register = Register("monitoring.pa.l3")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Power analyser L3 parameters"
    register.range = ""
    register.value = []
    __registers.append(register)

    # Enable flag.
    register = Register("monitoring.enabled")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Plugin enabled"
    register.range = "True/False"
    # register.update_handler = self.__monitoring_enabled
    register.value = False
    __registers.append(register)

#endregion

#region Environment (env)

    register = Register("env.is_empty")
    register.scope = Scope.Device
    register.plugin_name = "Environment"
    register.description = "Is empty flag"
    register.range = "0/1"
    register.value = 1
    __registers.append(register)

    register = Register("env.is_empty_timeout")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Is empty time out [s]"
    register.range = "0/"
    register.value = 3600
    __registers.append(register)

    register = Register("env.temp.actual")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature [C]"
    register.range = "-50/50"
    register.value = 29.0
    __registers.append(register)

    register = Register("env.temp.a6")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature for 6 hours [C]"
    register.range = "-50/50"
    register.value = 30.0
    __registers.append(register)

    register = Register("env.temp.min24")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Minimum outside temperature for 24 hours [C]"
    register.range = "-50/50"
    register.value = 20.0
    __registers.append(register)

    register = Register("env.temp.max24")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Maximum outside temperature for 24 hours [C]"
    register.range = "-50/50"
    register.value = 36.0
    __registers.append(register)

    register = Register("env.rh")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside relative humidity [%]"
    register.range = "0.0/100.0"
    register.value = 60.0
    __registers.append(register)

    register = Register("env.wind.actual")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual wind [m/sec]"
    register.range = "0.0/"
    register.value = 3.0
    __registers.append(register)

    register = Register("env.wind.max12")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Maximum wind for 12 hours [m/sec]"
    register.range = "0.0/"
    register.value = 6.0
    __registers.append(register)

    register = Register("env.light")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Outside light [lux]"
    register.range = "0.0/"
    register.value = 1000.0
    __registers.append(register)

    register = Register("env.energy") # Energy mode of the building.
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Energy mode of the building"
    register.range = ""
    register.value = 0
    __registers.append(register)

    register = Register("env.emergency") # Emergency bit coded flags of the building.
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency flags of the building"
    register.range = ""
    register.value = 0
    __registers.append(register)

    register = Register("env.sunpos.enabled")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Enable software calculation of the sun position"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    register = Register("env.enabled")
    register.scope = Scope.System
    # register.update_handler = self.__env_enabled
    register.plugin_name = "Environment"
    register.description = "Plugin enabled"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

#endregion

#region HVAC (hvac)

    register = Register("hvac.adjust_temp")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Adjust temperature"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    # Air temp central.
    register = Register("hvac.air_temp_cent.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor center settings"
    register.range = ""
    register.value = "temp/DS18B20/28FFFCD0001703AE"
    __registers.append(register)

    # Air temp lower
    register = Register("hvac.air_temp_lower.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor lower settings"
    register.range = ""
    register.value = "temp/DS18B20/28FFC4EE00170349"
    __registers.append(register)

    # Air temp upper.
    register = Register("hvac.air_temp_upper.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor upper settings"
    register.range = ""
    register.value = "temp/DS18B20/28FF2B70C11604B7"
    __registers.append(register)

    # Convector
    register = Register("hvac.convector.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector settings"
    register.range = ""
    register.value = "silpa/klimafan"
    __registers.append(register)

    register = Register("hvac.convector.stage_1.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector stage 1 output"
    register.range = "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8"
    register.value = "RO0"
    __registers.append(register)

    register = Register("hvac.convector.stage_2.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector stage 2 output"
    register.range = "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8"
    register.value = "RO1"
    __registers.append(register)

    register = Register("hvac.convector.stage_3.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector stage 3 output"
    register.range = "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8"
    register.value = "RO2"
    __registers.append(register)

    # Delta time.
    register = Register("hvac.delta_time")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Measuring delta time"
    register.range = "0.0/"
    register.value = 5.0
    __registers.append(register)

    # HVAC Enabled.
    register = Register("hvac.enabled")
    register.scope = Scope.System
    # register.update_handler = self.__hvac_enabled
    register.plugin_name = "HVAC"
    register.description = "Plugin enabled"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    # Goal building temp.
    register = Register("hvac.goal_building_temp")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Goal of the building temperature"
    register.range = "-50.0/50.0"
    register.value = 20.0
    __registers.append(register)

    # Loop 1 flowmeter.
    register = Register("hvac.loop1.cnt.tpl")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 water flow meter ticks per liter scale"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("hvac.loop1.cnt.input")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 water flow meter signal input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = "DI4"
    __registers.append(register)

    # Loop 1 fan
    register = Register("hvac.loop1.fan.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 fan settings"
    register.range = ""
    register.value = "HangzhouAirflowElectricApplications/f3p146ec072600"
    __registers.append(register)

    register = Register("hvac.loop1.fan.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 fan output"
    register.range = "off|AI0|AI1|AI2|AI3|AI4|AI5|AI6|AI7|AI8"
    register.value = "AO3"
    __registers.append(register)

    register = Register("hvac.loop1.fan.min_speed")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 fan minimum speed [%]"
    register.range = "0.0/100.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("hvac.loop1.fan.max_speed")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 fan maximum speed [%]"
    register.range = "0.0/100.0"
    register.value = 30.0
    __registers.append(register)

    # Loop 1 Temperature
    register = Register("hvac.loop1.temp.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature sensor settings"
    register.range = ""
    register.value = "temp/DS18B20/28FF2B70C11604B7"
    __registers.append(register)

    # Loop 1 valve.
    register = Register("hvac.loop1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 valve settings"
    register.range = ""
    register.value = "TONHE/a20m15b2c"
    __registers.append(register)

    register = Register("hvac.loop1.valve.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 valve output"
    register.range = "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8"
    register.value = "RO4"
    __registers.append(register)

    register = Register("hvac.loop1.valve.feedback")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 valve feedback"
    register.range = "off|AI0|AI1|AI2|AI3|AI4|AI5|AI6|AI7|AI8"
    register.value = "AI1"
    __registers.append(register)

    register = Register("hvac.loop1.valve.max_pos")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 valve maximum position"
    register.range = "0.0/100.0"
    register.value = 100.0
    __registers.append(register)

    register = Register("hvac.loop1.valve.min_pos")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 valve minimum position"
    register.range = "0.0/100.0"
    register.value = 0.0
    __registers.append(register)

    # Loop 2 flowmeter
    register = Register("hvac.loop2.cnt.tpl")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 water flow meter ticks per liter scale"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("hvac.loop2.cnt.input")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 water flow meter signal input"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = "DI5"
    __registers.append(register)

    # Loop 2 fan
    register = Register("hvac.loop2.fan.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 fan settings"
    register.range = ""
    register.value = "HangzhouAirflowElectricApplications/f3p146ec072600"
    __registers.append(register)

    register = Register("hvac.loop2.fan.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 fan output"
    register.range = "off|AO0|AO1|AO2|AO3|AO4|AO5|AO6|AO7|AO8"
    register.value = "AO4"
    __registers.append(register)

    register = Register("hvac.loop2.fan.min_speed")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 fan minimum speed [%]"
    register.range = "0.0/100.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("hvac.loop2.fan.max_speed")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 fan maximum speed [%]"
    register.range = "0.0/100.0"
    register.value = 30.0
    __registers.append(register)

    # Loop 2 Temperature
    register = Register("hvac.loop2.temp.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 temperature sensor settings"
    register.range = ""
    register.value = "temp/DS18B20/28FFC4EE00170349"
    __registers.append(register)

    # Loop 2 valve.
    register = Register("hvac.loop2.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 valve settings"
    register.range = ""
    register.value = "TONHE/a20m15b2c"
    __registers.append(register)

    register = Register("hvac.loop2.valve.output")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 valve output"
    register.range = "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8"
    register.value = "RO3"
    __registers.append(register)

    register = Register("hvac.loop2.valve.feedback")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 valve feedback"
    register.range = "off|AI0|AI1|AI2|AI3|AI4|AI5|AI6|AI7|AI8"
    register.value = "AI2"
    __registers.append(register)

    register = Register("hvac.loop2.valve.max_pos")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 valve maximum position"
    register.range = "0.0/100.0"
    register.value = 100.0
    __registers.append(register)

    register = Register("hvac.loop2.valve.min_pos")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 valve minimum position"
    register.range = "0.0/100.0"
    register.value = 0.0
    __registers.append(register)

    # Temperature actual
    register = Register("hvac.temp.actual")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Actual temperature"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("hvac.temp.max")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Maximum achievable"
    register.range = "-50.0/50.0"
    register.value = 30.0
    __registers.append(register)

    register = Register("hvac.temp.min")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Minimum achievable"
    register.range = "-50.0/50.0"
    register.value = 20.0
    __registers.append(register)

    # Thermal force limit
    register = Register("hvac.thermal_force_limit")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Thermal force limit"
    register.range = "0.0/100.0"
    register.value = 100.0
    __registers.append(register)

    # Thermal mode
    register = Register("hvac.thermal_mode")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Thermal mode"
    register.range = "1|2|3|4"
    register.value = 2
    __registers.append(register)

    # Update rate.
    register = Register("hvac.update_rate")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Update rate of the plugin [s]"
    register.range = "0.0/"
    register.value = 3.0
    __registers.append(register)

#endregion

#region Light (light)

    register = Register("light.min")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Minimum limit"
    register.range = "0.0/10000.0"
    register.value = 800.0
    __registers.append(register)

    register = Register("light.max")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Maximum limit"
    register.range = "0.0/10000.0"
    register.value = 10000.0
    __registers.append(register)

    register = Register("light.v1.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Analog output 1"
    register.range = "off|AO0|AO1|AO2|AO3|AO4|AO5|AO6|AO7|AO8"
    register.value = "AO1"
    __registers.append(register)

    register = Register("light.v2.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Analog output 2"
    register.range = "off|AO0|AO1|AO2|AO3|AO4|AO5|AO6|AO7|AO8"
    register.value = "AO2"
    __registers.append(register)

    register = Register("light.sensor.settings")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Sensor settings"
    register.range = ""
    register.value = "1wdevice/26607314020000F8"
    __registers.append(register)

    # register = Register("light.sensor.model")
    # register.scope = Scope.Global
    # register.scope = Scope.System
    # register.plugin_name = "Light"
    # register.scope = "system"
    # register.description = ""
    # register.range = ""
    # register.value = "u1wtvs"
    # __registers.append(register)

    # register = Register("light.sensor.vendor")
    # register.scope = Scope.Global
    # register.scope = Scope.System
    # register.plugin_name = "Light"
    # register.scope = "system"
    # register.description = ""
    # register.range = ""
    # register.value = "SEDtronic"
    # __registers.append(register)

    register = Register("light.enabled")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Plugin enabled"
    register.range = "True/False"
    # register.update_handler = self.__light_enabled
    register.value = False
    __registers.append(register)

#endregion

#region System (sys)

    # Last 60 seconds
    register = Register("sys.last_minute_errs")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Last minute error"
    register.range = ""
    register.value = []
    # GlobalErrorHandler.set_register(register)
    __registers.append(register)

    # Systrem resources
    register = Register("sys.ram.current")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Current consumed RAM"
    register.range = "0/"
    register.value = 0
    __registers.append(register)

    register = Register("sys.ram.peak")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Peek of consumed RAM"
    register.range = "0/"
    register.value = 0
    __registers.append(register)

    register = Register("sys.time.usage")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Application time cycle"
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    # Status LED
    register = Register("sys.sl.output")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Status LED"
    register.range = "off|LED0|LED1|LED2|LED3"
    register.value = "LED0"
    __registers.append(register)

    register = Register("sys.sl.blink_time")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Blink time"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    # Anti tampering
    register = Register("sys.at.input")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Anti tamper"
    register.range = "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8"
    register.value = "DI1"
    __registers.append(register)

    register = Register("sys.at.state")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Anti tampering state"
    register.range = "True/False"
    register.value = False
    __registers.append(register)

    # Colision detector
    register = Register("sys.col.info_message")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Collision info message"
    register.range = ""
    register.value = {}
    __registers.append(register)

    register = Register("sys.col.warning_message")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Collision warning message"
    register.range = ""
    register.value = {}
    __registers.append(register)

    register = Register("sys.col.error_message")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Collision error message"
    register.range = ""
    register.value = {}
    __registers.append(register)

    register = Register("sys.col.clear_errors")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Clear messages"
    register.range = "0|1"
    register.value = 0
    __registers.append(register)

    # Enable disable plugin.
    register = Register("sys.enabled")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Plugin enabled"
    register.range = "True/False"
    # register.update_handler = self.__sys_enabled
    register.value = False
    __registers.append(register)

#endregion

def main():
    global __registers

    __registers = Registers()

    __add_registers()

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--typ", type=str, default="csv", help="Export type.")

    # Take arguments.
    args = parser.parse_args()

    if args.typ == "json":
        Registers.to_JSON(__registers, "registers.json")

    elif args.typ == "csv":
        Registers.to_CSV(__registers, "registers.csv")

    elif args.typ == "read":

        registers = Registers.from_CSV("registers.csv")

        for register in registers:
            print(register)

if __name__ == "__main__":
    main()