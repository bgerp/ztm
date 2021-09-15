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
import json

from data.register import Register
from data.register import Scope
from data.registers import Registers
from data import verbal_const

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

#region Variables

__registers = None
"""Registers"""

__range = {
    "NONE": "",
    "DI": "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8|!DI0|!DI1|!DI2|!DI3|!DI4|!DI5|!DI6|!DI7|!DI8",
    "DO": "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8|!DO0|!DO1|!DO2|!DO3|!DO4|!DO5|!DO6|!DO7|!DO8",
    "RO": "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8|!RO0|!RO1|!RO2|!RO3|!RO4|!RO5|!RO6|!RO7|!RO8",
    "AO": "off|AO0|AO1|AO2|AO3|AO4|AO5|AO6|AO7|AO8",
    "AI": "off|AI0|AI1|AI2|AI3|AI4|AI5|AI6|AI7|AI8",
    "LED": "off|LED0|LED1|LED2|LED3|!LED0|!LED1|!LED2|!LED3",
    "BAUD": "300|600|1200|2400|4800|9600|19200|38400|57600|115200",
    "BOOL": "true|false",
    "PERCENTAGE_F": "0.0/100.0",
    "PERCENTAGE_I": "0/100",
    "PERCENTAGE_0_100": "0.0|100.0",
}

#endregion

def __add_registers():

    global __registers, __range

#region Access Control (ac)

    register = Register("ac.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    # register.update_handlers = self.__access_control_enabled
    register.value = False
    __registers.append(register)

    register = Register("ac.allowed_attendees")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Allowed attendees"
    register.range = ""
    register.value = [] # {"card_id": "445E6046010080FF", "pin": "159753", "valid_until": "1595322860"}
    __registers.append(register)

    register = Register("ac.zones_count")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Number of security zones"
    register.range = "1/"
    register.value = 2
    __registers.append(register)

    register = Register("ac.nearby_attendees")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Nearby attendees"
    register.range = ""
    register.value = [] # {"card_id": "445E6046010080FF", "ts":"1595322860"}
    __registers.append(register)

    register = Register("ac.last_update_attendees")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Last update attendee"
    register.range = ""
    register.value = [] # {"card_id": "445E6046010080FF", "ts":"1595322860"}
    __registers.append(register)

    register = Register("ac.next_attendance")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Next attendance"
    register.range = "0.0/"
    register.value = 0.0 # 1595322860
    __registers.append(register)

    # Entry card reader.
    register = Register("ac.entry_reader_1.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader enabled"
    register.range = ""
    register.value = verbal_const.OFF # "Teracom/act230/2911"
    __registers.append(register)

    register = Register("ac.entry_reader_1.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port baud rate"
    register.range = __range["BAUD"]
    register.value = 9600
    __registers.append(register)

    register = Register("ac.entry_reader_1.port.name")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port name"
    register.range = ""
    if os.name == "posix":
        register.value = "/dev/ttyUSB1"
    if os.name == "nt":
        register.value = "COM11"
    __registers.append(register)

    # Exit card reader.
    register = Register("ac.exit_reader_1.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader enabled"
    register.range = ""
    register.value = verbal_const.OFF # "Teracom/act230/2897"
    __registers.append(register)

    register = Register("ac.exit_reader_1.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader 1 port baud rate"
    register.range = __range["BAUD"]
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
        register.value = "COM5"
    __registers.append(register)

    #
    register = Register("ac.exit_button_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Exit button 1 input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.lock_mechanism_1.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock mechanism output"
    register.range = __range["DO"]
    register.value = "DO2"
    __registers.append(register)

    register = Register("ac.time_to_open_1")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock mechanism time to open [s]"
    register.range = "0/60"
    register.value = 3
    __registers.append(register)

    register = Register("ac.door_closed_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door closed input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI5"
    __registers.append(register)

    register = Register("ac.door_closed_1.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door closed input state"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # Entry card reader 2.
    register = Register("ac.entry_reader_2.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader settings"
    register.range = ""
    register.value = verbal_const.OFF # "Teracom/act230/2486"
    __registers.append(register)


    register = Register("ac.entry_reader_2.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port baud rate"
    register.range = __range["BAUD"]
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
        register.value = "COM8"
    __registers.append(register)

    # Exit card reader.
    register = Register("ac.exit_reader_2.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader settings"
    register.range = ""
    register.value = verbal_const.OFF # "Teracom/act230/1208"
    __registers.append(register)

    register = Register("ac.exit_reader_2.port.baudrate")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader port baud rate"
    register.range = __range["BAUD"]
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
        register.value = "COM9"
    __registers.append(register)

    #
    register = Register("ac.exit_button_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Exit button 2 input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.lock_mechanism_2.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock 2 mechanism output"
    register.range = __range["DO"]
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)

    register = Register("ac.time_to_open_2")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock 2 mechanism time to open"
    register.range = "0/60"
    register.value = 3
    __registers.append(register)

    register = Register("ac.door_closed_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door 2 closed input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI2"
    __registers.append(register)

    register = Register("ac.door_closed_2.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door 2 closed input state"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    #
    register = Register("ac.pir_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "PIR 1 sensor input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI6"
    __registers.append(register)

    register = Register("ac.pir_1.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "PIR 1 sensor input state"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    register = Register("ac.pir_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "PIR 2 sensor input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    register = Register("ac.pir_2.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "PIR 2 sensor input state"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    #
    register = Register("ac.window_closed_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Window 1 closed input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "!DI4"
    __registers.append(register)

    register = Register("ac.window_closed_1.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Window 1 closed input state"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    register = Register("ac.window_closed_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Window 2 closed input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "!DI3"
    __registers.append(register)

    register = Register("ac.window_closed_2.state")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Window 2 closed input state"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    # Door window blind 1.
    register = Register("ac.door_window_blind_1.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door window blind 1 output"
    register.range = __range["DO"]
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)


    register = Register("ac.door_window_blind_1.value")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door window blind 1 value"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    # Door window blind 2.
    register = Register("ac.door_window_blind_2.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Door window blind 2 output"
    register.range = __range["DO"]
    register.value = verbal_const.OFF # "DO2"
    __registers.append(register)

    register = Register("ac.door_window_blind_2.value")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Door window blind 2 value"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    # Occupation
    register = Register("ac.zone_1_occupied")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Zone occupied flag"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    register = Register("ac.zone_2_occupied")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Zone occupied flag"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

#endregion

#region Blinds (blinds)

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
    register.range = __range["DO"]
    register.value = "DO0"
    __registers.append(register)

    register = Register("blinds.output_cw")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "CW output"
    register.range = __range["DO"]
    register.value = "DO1"
    __registers.append(register)

    register = Register("blinds.position")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Position [deg]"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.deg_per_sec")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Degrees pre seconds ratio."
    register.range = "0.0/"
    register.value = 10.0
    __registers.append(register)

    register = Register("blinds.feedback_treshold")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Feedback treshold level in [V]."
    register.range = "0.0/"
    register.value = 0.093
    __registers.append(register)

    register = Register("blinds.sunspot_limit")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Sun spot limit [m]."
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("blinds.object_height")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Object height [m]."
    register.range = "0.0/"
    register.value = 2.0
    __registers.append(register)

    register = Register("blinds.enabled")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    # register.update_handlers = self.__blinds_enabled
    register.value = False
    __registers.append(register)

#endregion

#region Monitoring (mon)

    # Cold water flow meter.
    register = Register("monitoring.cw.input")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Cold water input flow meter"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI3"
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
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI2"
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
    register.value = "Eastron/SDM630/0/2" # "Eastron/SDM120/2/3"
    __registers.append(register)

    register = Register("monitoring.pa.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Power analyser measurements"
    register.range = ""
    register.value = []
    __registers.append(register)

    register = Register("monitoring.pa.demand_time")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Power analyser measuring demand"
    register.range = "0.0/"
    register.value = 3600.0 # Every hour to measure the consumed electricity.
    __registers.append(register)

    # Enable flag.
    register = Register("monitoring.enabled")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    # register.update_handlers = self.__monitoring_enabled
    register.value = False
    __registers.append(register)

#endregion

#region Environment (envm)

    register = Register("envm.is_empty")
    register.scope = Scope.Device
    register.plugin_name = "Environment"
    register.description = "Is empty flag"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    register = Register("envm.is_empty_timeout")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Is empty time out [s]"
    register.range = "0/"
    register.value = 3600
    __registers.append(register)

    register = Register("envm.temp.actual")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature [C]"
    register.range = "-50/50"
    register.value = 20.0
    __registers.append(register)

    register = Register("envm.temp.a6")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature for 6 hours [C]"
    register.range = "-50/50"
    register.value = 30.0
    __registers.append(register)

    register = Register("envm.temp.min24")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Minimum outside temperature for 24 hours [C]"
    register.range = "-50/50"
    register.value = 20.0
    __registers.append(register)

    register = Register("envm.temp.max24")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Maximum outside temperature for 24 hours [C]"
    register.range = "-50/50"
    register.value = 36.0
    __registers.append(register)

    register = Register("envm.rh")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside relative humidity [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 60.0
    __registers.append(register)

    register = Register("envm.wind.actual")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual wind [m/sec]"
    register.range = "0.0/"
    register.value = 3.0
    __registers.append(register)

    register = Register("envm.wind.max12")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Maximum wind for 12 hours [m/sec]"
    register.range = "0.0/"
    register.value = 6.0
    __registers.append(register)

    register = Register("envm.light")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Outside light [lux]"
    register.range = "0.0/"
    register.value = 1000.0
    __registers.append(register)

    register = Register("envm.energy") # Energy mode of the building.
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Energy mode of the building"
    register.range = ""
    register.value = 0
    __registers.append(register)

    register = Register("envm.flag_fire")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency index for the fire."
    register.range = "0/3"
    register.value = 0
    __registers.append(register)

    register = Register("envm.flag_storm")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency index for the storm."
    register.range = "0/3"
    register.value = 0
    __registers.append(register)

    register = Register("envm.flag_earthquake")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency index for the earthquake."
    register.range = "0/3"
    register.value = 0
    __registers.append(register)

    register = Register("envm.flag_gassing")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency index for the gassing."
    register.range = "0/3"
    register.value = 0
    __registers.append(register)

    register = Register("envm.flag_flooding")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency index for the flooding."
    register.range = "0/3"
    register.value = 0
    __registers.append(register)

    register = Register("envm.flag_blocked")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Emergency index for the blocking."
    register.range = "0/3"
    register.value = 0
    __registers.append(register)

    register = Register("envm.sunpos.enabled")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Enable software calculation of the sun position"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    register = Register("envm.building.location.lat")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Latitude of the target building."
    register.range = "0.0/360.0"
    register.value = 43.07779
    __registers.append(register)

    register = Register("envm.building.location.lon")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Longitude of the target building."
    register.range = "0.0/360.0"
    register.value = 25.59549
    __registers.append(register)

    register = Register("envm.building.location.elv")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Longitude of the target building."
    register.range = "/"
    register.value = 210
    __registers.append(register)

    register = Register("envm.building.location.time_zone")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Longitude of the target building."
    register.range = "0/23"
    register.value = 2
    __registers.append(register)

    register = Register("envm.enabled")
    register.scope = Scope.System
    # register.update_handlers = self.__env_enabled
    register.plugin_name = "Environment"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    register = Register("envm.sun.azimuth")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Sun azimuth value"
    register.range = "0.0/360.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.sun.elevation")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Sun elevation value"
    register.range = "0.0/360.0"
    register.value = 0.0
    __registers.append(register)

#endregion

#region HVAC (hvac)

    register = Register("hvac.zones_count")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Count of the HVAC zones."
    register.range = "0/"
    register.value = 1
    __registers.append(register)

    register = Register("hvac.adjust_temp_1")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Adjust temperature"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    # Air temp central.
    register = Register("hvac.air_temp_cent_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor center settings"
    register.range = ""
    register.value = {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "mb_id": 4,
            }
        } # Dallas/DS18B20/28FFFCD0001703AE # temp/DS18B20/28FFFCD0001703AE
    __registers.append(register)

    register = Register("hvac.air_temp_cent_1.value")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor center value"
    register.range = "/"
    register.value = 0.0
    __registers.append(register)

    # Air temp lower
    register = Register("hvac.air_temp_lower_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor lower settings"
    register.range = ""
    register.value = {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "mb_id": 3,
            }
        } # "Dallas/DS18B20/28FFC4EE00170349" # temp/DS18B20/28FFC4EE00170349
    __registers.append(register)

    register = Register("hvac.air_temp_lower_1.value")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor lower value"
    register.range = "/"
    register.value = 0.0
    __registers.append(register)

    # Air temp upper.
    register = Register("hvac.air_temp_upper_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor upper settings"
    register.range = ""
    register.value =         {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "mb_id": 5,
            }
        } # Dallas/DS18B20/28FF2B70C11604B7 # "Dallas/DS18B20/28FF2B70C11604B7" # "temp/DS18B20/28FF2B70C11604B7"
    __registers.append(register)

    register = Register("hvac.air_temp_upper_1.value")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor upper value"
    register.range = "/"
    register.value = 0.0
    __registers.append(register)

    # Convector
    register = Register("hvac.convector_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector settings"
    register.range = ""
    register.value = {
            "vendor": "Silpa",
            "model": "Klimafan",
            "options":
            {
                "stage1": "RO4",
                "stage2": "RO5",
                "stage3": "RO6",
            }
        }
    __registers.append(register)

    # Delta time.
    register = Register("hvac.delta_time_1")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Measuring delta time"
    register.range = "0.0/"
    register.value = 5.0
    __registers.append(register)

    # HVAC Enabled.
    register = Register("hvac.enabled")
    register.scope = Scope.System
    # register.update_handlers = self.__hvac_enabled
    register.plugin_name = "HVAC"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
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
    register = Register("hvac.loop1_1.cnt.tpl")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 water flow meter ticks per liter scale"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("hvac.loop1_1.cnt.input")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 water flow meter signal input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI1"
    __registers.append(register)

    # Loop 1 Temperature
    register = Register("hvac.loop1_1.temp.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature sensor settings"
    register.range = ""
    register.value = {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "mb_id": 3,
            }
        } # "Dallas/DS18B20/28FF2B70C11604B7" # temp/DS18B20/28FF2B70C11604B7
    __registers.append(register)

    register = Register("hvac.loop1_1.temp.value")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature sensor value"
    register.range = "/"
    register.value = 0.0
    __registers.append(register)

    # Loop 1 Down Limit Temperature # Request: Eml6419
    register = Register("hvac.loop1_1.temp.down_limit")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature down limit"
    register.range = "0.0/"
    register.value = 15
    __registers.append(register)

    # Loop 1 valve.
    register = Register("hvac.loop1_1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 valve settings"
    register.range = ""
    register.value = "Tonhe/a20m15b2c/RO2/off/0/100"
    __registers.append(register)

    # Loop 2 flowmeter
    register = Register("hvac.loop2_1.cnt.tpl")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 water flow meter ticks per liter scale"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)

    register = Register("hvac.loop2_1.cnt.input")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 water flow meter signal input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI0"
    __registers.append(register)

    # Loop 2 Temperature
    register = Register("hvac.loop2_1.temp.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 temperature sensor settings"
    register.range = ""
    register.value = {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "mb_id": 5,
            }
        } # "Dallas/DS18B20/28FFC4EE00170349" # temp/DS18B20/28FFC4EE00170349
    __registers.append(register)

    register = Register("hvac.loop2_1.temp.value")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature sensor value"
    register.range = "/"
    register.value = 0.0
    __registers.append(register)

    # Loop 2 valve.
    register = Register("hvac.loop2_1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 2 valve settings"
    register.range = ""
    register.value = "Tonhe/a20m15b2c/RO3/off/0/100"
    __registers.append(register)

    # Temperature actual
    register = Register("hvac.temp_1.actual")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Actual temperature"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("hvac.temp_1.max")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Maximum achievable"
    register.range = "-50.0/50.0"
    register.value = 30.0
    __registers.append(register)

    register = Register("hvac.temp_1.min")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Minimum achievable"
    register.range = "-50.0/50.0"
    register.value = 20.0
    __registers.append(register)

    # Thermal force limit
    register = Register("hvac.thermal_force_limit_1")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Thermal force limit"
    register.range = __range["PERCENTAGE_F"]
    register.value = 100.0
    __registers.append(register)

    # Thermal mode
    register = Register("hvac.thermal_mode_1")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Thermal mode"
    register.range = "1|2|3|4"
    register.value = 2
    __registers.append(register)

    # Update rate.
    register = Register("hvac.update_rate_1")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Update rate of the plugin [s]"
    register.range = "0.0/"
    register.value = 5.0
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
    register.range = __range["AO"]
    register.value = "AO2"
    __registers.append(register)

    register = Register("light.v2.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Analog output 2"
    register.range = __range["AO"]
    register.value = "AO3"
    __registers.append(register)

    register = Register("light.sensor.settings")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Sensor settings"
    register.range = ""
    register.value = {
            "vendor": "PT",
            "model": "light_sensor",
            "options":
            {
                "input": "AI2",
            }
        }
    # ""SEDtronic/u1wtvs/1wdevice/26607314020000F8"
    # SEDtronic/u1wtvs/1wdevice/26607314020000F8
    # PT/light_sensor/AI2
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

    register = Register("light.target_illum")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Target illumination"
    register.range = "0.0/10000.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("light.error_gain")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Error gain"
    register.range = "/"
    register.value = 0.01
    __registers.append(register)


    register = Register("light.enabled")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    # register.update_handlers = self.__light_enabled
    register.value = False
    __registers.append(register)

#endregion

#region System (sys)

    # Last 60 seconds
    register = Register("sys.last_update_errs")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Last update cycle error"
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

    register = Register("sys.disc.total")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Total disc space"
    register.range = "0/"
    register.value = 0
    __registers.append(register)

    register = Register("sys.disc.used")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Used disc space"
    register.range = "0/"
    register.value = 0
    __registers.append(register)

    register = Register("sys.disc.free")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Free disc space"
    register.range = "0/"
    register.value = 0
    __registers.append(register)

    # Status LED
    register = Register("sys.sl.output")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Status LED"
    register.range = __range["LED"]
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
    register.range = __range["DI"]
    register.value = verbal_const.OFF # "DI7"
    __registers.append(register)

    register = Register("sys.at.state")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Anti tampering state"
    register.range = __range["BOOL"]
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
    register.range = __range["BOOL"]
    # register.update_handlers = self.__sys_enabled
    register.value = False
    __registers.append(register)


    # Enable info messages.
    register = Register("sys.col.info_message.enable")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Enable info messages"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # Enable warning messages.
    register = Register("sys.col.warning_message.enable")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Enable warning messages"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # Enable error messages.
    register = Register("sys.col.error_message.enable")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Enable error messages"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # Software update register.
    register = Register("sys.software.target_version")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Target software version"
    register.range = __range["NONE"]
    register.value = json.loads("{\"repo\": \"http:\/\/github.com\/bgerp\/ztm\/\", \"branch\": \"master\", \"commit\":\"3462828\"}")
    __registers.append(register)

    # Current software version.
    register = Register("sys.software.current_version")
    register.scope = Scope.System
    register.plugin_name = "System"
    register.description = "Current software version."
    register.range = __range["NONE"]
    register.value = json.loads("{\"repo\": \"http:\/\/github.com\/bgerp\/ztm\/\", \"branch\": \"master\", \"commit\":\"e0c1dda\"}")
    __registers.append(register)

#endregion

#region Energy Center Common (ecc)

    register = Register("ecc.enabled")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Common"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

#endregion

#region Energy Center Distribution (ecd)

    # ECD / Foyer Floor Heating Settings
    register = Register("ecd.underfloor_heating_foyer.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Foyer Floor Heating Settings"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Foyer Floor Heating Position
    register = Register("ecd.underfloor_heating_foyer.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Foyer Floor Heating Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Foyer Floor Heating Position
    register = Register("ecd.underfloor_heating_foyer.valve.calibrate")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Foyer Floor Heating Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Underfloor Heating Trestle Settings
    register = Register("ecd.underfloor_heating_trestle.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor Heating Trestle"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Underfloor Heating Trestle Position
    register = Register("ecd.underfloor_heating_trestle.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor Heating Trestle Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Underfloor Heating Trestle Calibration
    register = Register("ecd.underfloor_heating_trestle.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor Heating Trestle Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Underfloor Heating Pool Settings
    register = Register("ecd.underfloor_heating_pool.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor Heating Pool"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Underfloor Heating Pool Position
    register = Register("ecd.underfloor_heating_pool.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor Heating Pool Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Underfloor Heating Pool Calibration
    register = Register("ecd.underfloor_heating_pool.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor Heating Pool Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Air Cooling Valve Settings
    register = Register("ecd.air_cooling.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Air Cooling Valve Settings"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Air Cooling Valve Position
    register = Register("ecd.air_cooling.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Air Cooling Valve Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Air Cooling Valve Calibration
    register = Register("ecd.air_cooling.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Air Cooling Valve Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Ground Drilling Valve Settings
    register = Register("ecd.ground_drill.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Ground Drilling Valve"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Ground Drill Valve Position
    register = Register("ecd.ground_drill.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Ground Drill Valve Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Ground Drill Valve Calibration
    register = Register("ecd.ground_drill.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Ground Drill Valve Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Generators Cooling Valve Settings
    register = Register("ecd.generators_cooling.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Generators Cooling Valve / Settings"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Generators Cooling Valve Position
    register = Register("ecd.generators_cooling.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Generators Cooling Valve / Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Generators Cooling Valve Calibration
    register = Register("ecd.generators_cooling.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Generators Cooling Valve Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Short Green/Purple Valve Settings
    register = Register("ecd.short_green_purple.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Short Green/Purple Valve Settings"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Short Green/Purple Valve Position
    register = Register("ecd.short_green_purple.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Short Green/Purple Valve Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Generators Cooling Valve Calibration
    register = Register("ecd.short_green_purple.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Generators Cooling Valve Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Underfloor West Bypass Valve Settings
    register = Register("ecd.underfloor_west_bypass.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor West Bypass Valve Settings"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Underfloor West Bypass Valve Position
    register = Register("ecd.underfloor_west_bypass.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor West Bypass Valve Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Underfloor West Bypass Valve Calibration
    register = Register("ecd.underfloor_west_bypass.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor West Bypass Valve Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / Underfloor East Bypass Valve Settings
    register = Register("ecd.underfloor_east_bypass.valve.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor East Bypass Valve Settings"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / Underfloor East Bypass Valve Position
    register = Register("ecd.underfloor_east_bypass.valve.position")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor East Bypass Valve Position"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Underfloor East Bypass Valve Calibration
    register = Register("ecd.underfloor_east_bypass.valve.calibration")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / Underfloor East Bypass Valve Calibration"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)


    # ECD / VCG / Pool Heating Valve
    register = Register("ecd.vcg_pool_heating.valve")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Heating"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Pool Heating Valve Pump
    register = Register("ecd.vcg_pool_heating.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Heating"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Pool Heating Valve Pump
    register = Register("ecd.vcg_pool_heating.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Heating"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)


    # ECD / VCG / Pool Cooling In
    register = Register("ecd.vcg_tva_pool.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Cooling In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Pool Cooling Out
    register = Register("ecd.vcg_tva_pool.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Cooling In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)


    # ECD / VCG / Pool Heating In
    register = Register("ecd.vcg_tva_pool.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Heating In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Pool Heating Out
    register = Register("ecd.vcg_tva_pool.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pool Heating Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Pump
    register = Register("ecd.vcg_tva_pool.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Pump"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Enable
    register = Register("ecd.vcg_tva_pool.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Enable"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / Convectors East Cooling In
    register = Register("ecd.convectors_east.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors East Cooling In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors East Cooling Out
    register = Register("ecd.convectors_east.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors East Cooling Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)


    # ECD / VCG / Convectors East Hot In
    register = Register("ecd.convectors_east.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors East Hot In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors East Hot Out
    register = Register("ecd.convectors_east.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors East Hot Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors East Pump
    register = Register("ecd.convectors_east.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors East Pump"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors East Enable
    register = Register("ecd.convectors_east.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors East Enable"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)


    # ECD / VCG / Floor East Cooling In
    register = Register("ecd.underfloor_east.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor East Cooling In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor East Cooling Out
    register = Register("ecd.underfloor_east.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor East Cooling Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor East Hot In
    register = Register("ecd.underfloor_east.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor East Hot In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor East Hot Out
    register = Register("ecd.underfloor_east.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor East Hot Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor East Pump
    register = Register("ecd.underfloor_east.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor East Pump"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Underfloor East Enable
    register = Register("ecd.underfloor_east.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor East Enable"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)


    # ECD / VCG / Convectors West Cooling In
    register = Register("ecd.convectors_west.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors West Cooling In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors West Cooling Out
    register = Register("ecd.convectors_west.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors West Cooling Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)


    # ECD / VCG / Convectors West Hot In
    register = Register("ecd.convectors_west.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors West Hot In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors West Hot Out
    register = Register("ecd.convectors_west.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors West Hot Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors West Pump
    register = Register("ecd.convectors_west.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors West Pump"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors West Enable
    register = Register("ecd.convectors_west.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors West Enable"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / TVA Roof Floor In
    register = Register("ecd.tva_roof_floor.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Roof Floor In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Roof Floor Out
    register = Register("ecd.tva_roof_floor.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Roof Floor Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)
    
    # ECD / VCG / TVA Roof Floor In
    register = Register("ecd.tva_roof_floor.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Roof Floor In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Roof Floor Out
    register = Register("ecd.tva_roof_floor.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Roof Floor Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)


    # ECD / VCG / TVA Roof Floor Pump
    register = Register("ecd.tva_roof_floor.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Roof Floor"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Roof Floor Pump
    register = Register("ecd.tva_roof_floor.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Roof Floor"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / TVA Fitness In
    register = Register("ecd.tva_fitness.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Fitness In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Fitness Out
    register = Register("ecd.tva_fitness.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Fitness Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Fitness In
    register = Register("ecd.tva_fitness.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Fitness In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Fitness Out
    register = Register("ecd.tva_fitness.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Fitness Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Fitness
    register = Register("ecd.tva_fitness.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Fitness"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Fitness
    register = Register("ecd.tva_fitness.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Fitness"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / Floor West Cooling In
    register = Register("ecd.floor_west.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor West Cooling In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor West Cooling Out
    register = Register("ecd.floor_west.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor West Cooling Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor West Hot In
    register = Register("ecd.floor_west.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor West Hot In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor West Hot Out
    register = Register("ecd.floor_west.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor West Hot Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor West Pump
    register = Register("ecd.floor_west.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor West Pump"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Floor West Pump
    register = Register("ecd.floor_west.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Floor West Pump"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / TVA Conference Center In
    register = Register("ecd.tva_conference_center.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Conference Center In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Conference Center Out
    register = Register("ecd.tva_conference_center.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Conference Center Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Conference Center In
    register = Register("ecd.tva_conference_center.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Conference Center In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Conference Center Out
    register = Register("ecd.tva_conference_center.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Conference Center Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Conference Center Pump
    register = Register("ecd.tva_conference_center.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Conference Center"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Conference Center Pump
    register = Register("ecd.tva_conference_center.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Conference Center"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / Convectors Kitchen Cold In
    register = Register("ecd.convectors_kitchen.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors Kitchen Cold In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors Kitchen Cold Out
    register = Register("ecd.convectors_kitchen.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors Kitchen Cold Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)
    
    # ECD / VCG / Convectors Kitchen Hot In
    register = Register("ecd.convectors_kitchen.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors Kitchen Hot In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors Kitchen Hot Out
    register = Register("ecd.convectors_kitchen.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors Kitchen Hot Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)


    # ECD / VCG / Convectors Kitchen Pump
    register = Register("ecd.convectors_kitchen.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors Kitchen Pump"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / Convectors Kitchen Pump
    register = Register("ecd.convectors_kitchen.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / Convectors Kitchen Pump"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # ECD / VCG / TVA Wearhouse Cold In
    register = Register("ecd.tva_warehouse.cold_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Wearhouse Cold In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)
    
    # ECD / VCG / TVA Wearhouse Cold Out
    register = Register("ecd.tva_warehouse.cold_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Wearhouse Cold Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Wearhouse Hot In
    register = Register("ecd.tva_warehouse.hot_in")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Wearhouse Hot In"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Wearhouse Hot Out
    register = Register("ecd.tva_warehouse.hot_out")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Wearhouse Hot Out"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Wearhouse Pump
    register = Register("ecd.tva_warehouse.pump")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Wearhouse"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # ECD / VCG / TVA Wearhouse Pump
    register = Register("ecd.tva_warehouse.enabled")
    register.scope = Scope.System
    register.plugin_name = "ECD"
    register.description = "ECD / VCG / TVA Wearhouse"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    register = Register("ecd.enabled")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

#endregion

#region Energy Center Heat Pump controller (echp)

    # Input registers.

    # Count of the heat pump control groups.
    register = Register("echp.hp.count")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Energy Center Heat Pump machines count"
    register.range = "0/"
    register.value = 3
    __registers.append(register)

    # Index of the heat pump control group.
    register = Register("echp.hp.index")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Energy Center Heat Pump machine index"
    register.range = "0/"
    register.value = 0
    __registers.append(register)

    register = Register("echp.hp.power")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "The power of machine"
    register.range = "-100.0/100.0"
    register.value = 0
    __registers.append(register)

    register = Register("echp.hp.mode")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "The mode of the machine"
    register.range = ""
    register.value = 0
    __registers.append(register)

    register = Register("echp.hp.run")
    register.scope = Scope.Device
    register.plugin_name = "ECHP"
    register.description = "The state of the machine"
    register.range = ""
    register.value = 0
    __registers.append(register)

    # Cold minimum of the heat pump control group.
    register = Register("echp.hp.cold_min")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Energy Center Heat Pump cold minimum"
    register.range = "3.0/8.0"
    register.value = 5.0
    __registers.append(register)

    # Cold maximum of the heat pump control group.
    register = Register("echp.hp.cold_max")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Energy Center Heat Pump cold maximum"
    register.range = "3.0/8.0"
    register.value = 7.0
    __registers.append(register)

    # Hot minimum of the heat pump control group.
    register = Register("echp.hp.hot_min")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Energy Center Heat Pump hot minimum"
    register.range = "40.0/47.0"
    register.value = 41.0
    __registers.append(register)

    # Hot maximum of the heat pump control group.
    register = Register("echp.hp.hot_max")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Energy Center Heat Pump hot maximum"
    register.range = "40.0/47.0"
    register.value = 46.0
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / VCG / Cold Buffer / Input
    register = Register("echp.hpcg.vcg_cold_buf.input")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Buffer / Input"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Cold Buffer / Output
    register = Register("echp.hpcg.vcg_cold_buf.output")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Buffer / Output"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Cold Buffer / Short
    register = Register("echp.hpcg.vcg_cold_buf.short")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Buffer / Short"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "U1:ID1:R0:DO0",
                "output_ccw": "U1:ID1:R0:DO1",
                "limit_cw": "U1:ID1:R0:DI0",
                "limit_ccw": "U1:ID1:R0:DI1"
            }
        }
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / VCG / Cold Geo / Input
    register = Register("echp.hpcg.vcg_cold_geo.input")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Geo / Input"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Cold Geo / Output
    register = Register("echp.hpcg.vcg_cold_geo.output")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Geo / Output"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Cold Geo / Short
    register = Register("echp.hpcg.vcg_cold_geo.short")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Geo / Short"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / VCG / Warm Geo / Input
    register = Register("echp.hpcg.vcg_warm_geo.input")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Warm Geo / Input"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Warm Geo / Output
    register = Register("echp.hpcg.vcg_warm_geo.output")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Warm Geo / Output"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Warm Geo / Short
    register = Register("echp.hpcg.vcg_warm_geo.short")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Warm Geo / Short"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / VCG / Warm Geo / Input
    register = Register("echp.hpcg.vcg_warm_floor.input")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Warm Geo / Input"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Warm Geo / Output
    register = Register("echp.hpcg.vcg_warm_floor.output")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Warm Geo / Output"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / VCG / Warm Geo / Short
    register = Register("echp.hpcg.vcg_warm_floor.short")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Warm Geo / Output"
    register.range = ""
    register.value = {
            "vendor": "Flowx",
            "model": "FLX-05F",
            "options":
            {
                "output_cw": "off",
                "output_ccw": "off",
                "limit_cw": "off",
                "limit_ccw": "off"
            }
        }
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / Water Pump / Cold
    register = Register("echp.hpcg.wp_cold.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Cold"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 2,
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / Water Pump / Hot
    register = Register("echp.hpcg.wp_hot.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Hot"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 3,
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / Water Pump / Warm
    register = Register("echp.hpcg.wp_warm_p.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Warm"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 4,
            }
        }
    __registers.append(register)

    # Heat Pump Control Group / Water Pump / Warm
    register = Register("echp.hpcg.wp_warm_g.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Warm"
    register.range = ""
    register.value = {
            "vendor": "Grundfos",
            "model": "Pump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / Water Pump / Warm
    register = Register("echp.hpcg.hp.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Heat Pump"
    register.range = ""
    register.value =         {
            "vendor": "HstarsGuangzhouRefrigeratingEquipmentGroup",
            "model": "HeatPump",
            "options":
            {
                "mb_id": 5,
            }
        }
    __registers.append(register)

    # Output registers.

    register = Register("echp.enabled")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Heat Pump"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

#endregion

#region Ventilation (vent)

    # Operator panel setpoint.
    register = Register("vent.op_setpoint_1")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Operators panel set point"
    register.range = "0.0/100.0"
    register.value = 0
    __registers.append(register)

    # HVAC setpoint.
    register = Register("vent.hvac_setpoint_1")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "HVAC set point"
    register.range = "-100.0/100.0"
    register.value = 0
    __registers.append(register)

    # AC setpoint.
    register = Register("vent.ac_setpoint_1")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "AC set point"
    register.range = "0.0/100.0"
    register.value = 0
    __registers.append(register)

    # Upper fan
    register = Register("vent.lower_1.fan.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Lower fan settings"
    register.range = ""
    register.value = {
            "vendor": "HangzhouAirflowElectricApplications",
            "model": "f3p146ec072600",
            "options":
            {
                "output": "AO1",
            }
        }
    __registers.append(register)

    register = Register("vent.lower_1.fan.min_speed")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Lower fan minimum speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("vent.lower_1.fan.max_speed")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Lower fan maximum speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 30.0
    __registers.append(register)

    register = Register("vent.lower_1.fan.speed")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper fan speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # Upper fan
    register = Register("vent.upper_1.fan.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper fan settings"
    register.range = ""
    register.value = {
            "vendor": "HangzhouAirflowElectricApplications",
            "model": "f3p146ec072600",
            "options":
            {
                "output": "AO1",
            }
        }
    __registers.append(register)

    register = Register("vent.upper_1.fan.min_speed")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper fan minimum speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("vent.upper_1.fan.speed")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper fan speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("vent.upper_1.fan.max_speed")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper fan maximum speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 30.0
    __registers.append(register)

    # Upper valve settings
    register = Register("vent.upper_1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Lower valve settings"
    register.range = ""
    register.value = {
            "vendor": "FONYES",
            "model": "Model1",
            "options":
            {
                "closing": "DO8",
                "opening": "DO9",
            }
        }
    __registers.append(register)

    # Lower valve settings
    register = Register("vent.lower_1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper valve settings"
    register.range = ""
    register.value = {
            "vendor": "FONYES",
            "model": "Model1",
            "options":
            {
                "closing": "DO10",
                "opening": "DO11",
            }
        }
    __registers.append(register)

    # Zones count.
    register = Register("vent.zones_count")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Count of the ventilation zones."
    register.range = "0/"
    register.value = 1
    __registers.append(register)

    # Enable
    register = Register("vent.enabled")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Ventilation enable flag."
    register.range = ""
    register.value = False
    __registers.append(register)

#endregion

#region Alarm (alarm)

    # Visual signal device.
    register = Register("alarm.device.sound.settings")
    register.scope = Scope.System
    register.plugin_name = "Alarm"
    register.description = "Alarm module sound device settings."
    register.range = __range["NONE"]
    register.value = ""
    __registers.append(register)

    # Visual signal device.
    register = Register("alarm.device.visual.settings")
    register.scope = Scope.System
    register.plugin_name = "Alarm"
    register.description = "Alarm module visual device settings."
    register.range = __range["NONE"]
    register.value = ""
    __registers.append(register)

    # Enable
    register = Register("alarm.enabled")
    register.scope = Scope.System
    register.plugin_name = "Alarm"
    register.description = "Alarm module enable flag."
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

#endregion

#region Statistics (stat)

    # Enable
    register = Register("stat.enabled")
    register.scope = Scope.System
    register.plugin_name = "Statistics"
    register.description = "Statistics module enable flag."
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

#endregion

def main():
    global __registers, __range

    __registers = Registers()

    __add_registers()

    # Create parser.
    parser = argparse.ArgumentParser()

    # Add arguments.
    parser.add_argument("--action", type=str, default="w_csv", help="Export type.")

    # Take arguments.
    args = parser.parse_args()

    if args.action == "w_json":
        Registers.to_JSON(__registers, "registers.json")

    if args.action == "r_json":
        registers = Registers.from_JSON("registers.json")

        for register in registers:
            print(register)

    elif args.action == "w_csv":
        Registers.to_CSV(__registers, "registers.csv")

    elif args.action == "r_csv":
        registers = Registers.from_CSV("registers.csv")

        for register in registers:
            print(register)

if __name__ == "__main__":
    main()
