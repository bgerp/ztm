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
import json
import os

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

"""

 U1:ID1:R0:DO0
 |  |   |  |
 |  |   |  \----> Bit from the register.
 |  |   \-------> Register type.
 |  \-----------> Modbus identifier.
 \--------------> UART interface.

"""

#region Variables

__parser = None
"""Create parser.
"""

__registers = None
"""Registers
"""

__range = {
    "NONE": "",
    "DI": "off|DI0|DI1|DI2|DI3|DI4|DI5|DI6|DI7|DI8|!DI0|!DI1|!DI2|!DI3|!DI4|!DI5|!DI6|!DI7|!DI8",
    "DO": "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8|!DO0|!DO1|!DO2|!DO3|!DO4|!DO5|!DO6|!DO7|!DO8",
    "RO": "off|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8|!RO0|!RO1|!RO2|!RO3|!RO4|!RO5|!RO6|!RO7|!RO8",
    "DO|RO": "off|DO0|DO1|DO2|DO3|DO4|DO5|DO6|DO7|DO8|!DO0|!DO1|!DO2|!DO3|!DO4|!DO5|!DO6|!DO7|!DO8|RO0|RO1|RO2|RO3|RO4|RO5|RO6|RO7|RO8|!RO0|!RO1|!RO2|!RO3|!RO4|!RO5|!RO6|!RO7|!RO8",
    "AO": "off|AO0|AO1|AO2|AO3|AO4|AO5|AO6|AO7|AO8",
    "AI": "off|AI0|AI1|AI2|AI3|AI4|AI5|AI6|AI7|AI8",
    "LED": "off|LED0|LED1|LED2|LED3|!LED0|!LED1|!LED2|!LED3",
    "BAUD": "300|600|1200|2400|4800|9600|19200|38400|57600|115200",
    "BOOL": "true|false",
    "PERCENTAGE_F": "0.0/100.0",
    "PERCENTAGE_I": "0/100",
    "PERCENTAGE_0_100": "0.0|100.0",
    "PERCENTAGE_-100_100": "-100.0|100.0",
}

#endregion

def __set_parser():
    global __parser

    # Add arguments.
    __parser.add_argument("--action", type=str, default="w_json", help="Export JSON file.")
    # __parser.add_argument("--action", type=str, default="w_csv", help="Export CSV file.")
    # __parser.add_argument("--action", type=str, default="list_gpio", help="Export type.")
    # __parser.add_argument("--action", type=str, default="w_md", help="Export MD file.")
    # __parser.add_argument("--path", type=str, default=file_name, help="Target file path.")

    # Add args parameters
    __parser.add_argument("--pa", type=int, default=1, help="Power analyzer modbus ID.")
    __parser.add_argument("--hw", type=int, default=-1, help="How water flow meter modbus ID.")
    __parser.add_argument("--cw", type=int, default=-1, help="Cold water flow meter modbus ID.")
    __parser.add_argument("--fl_1_hm", type=int, default=-1, help="Floor loop 1 heat meter modbus ID.")
    __parser.add_argument("--fl_2_hm", type=int, default=-1, help="Floor loop 2 heat meter modbus ID.")
    __parser.add_argument("--fl_3_hm", type=int, default=-1, help="Floor loop 3 heat meter modbus ID.")
    __parser.add_argument("--cl_1_hm", type=int, default=-1, help="Convector loop 1 heat meter modbus ID.")
    __parser.add_argument("--cl_2_hm", type=int, default=-1, help="Convector loop 2 heat meter modbus ID.")
    __parser.add_argument("--cl_3_hm", type=int, default=-1, help="Convector loop 3 heat meter modbus ID.")
    __parser.add_argument("--temp_upper", type=int, default=4, help="Upper thermometer modbus ID.")
    __parser.add_argument("--temp_lower", type=int, default=5, help="Lower thermometer modbus ID.") 
    __parser.add_argument("--temp_cent", type=int, default=3, help="Central thermometer modbus ID.")
    __parser.add_argument("--pir_1", type=int, default=16, help="PIR 1 modbus ID.")
    __parser.add_argument("--blinds_1", type=int, default=11, help="Blinds mechanism 1 modbus ID.")
    __parser.add_argument("--blinds_2", type=int, default=-1, help="Blinds mechanism 2 modbus ID.")
    __parser.add_argument("--blinds_3", type=int, default=-1, help="Blinds mechanism 3 modbus ID.")
    __parser.add_argument("--blinds_4", type=int, default=-1, help="Blinds mechanism 4 modbus ID.")
    __parser.add_argument("--bi_1", type=int, default=2, help="Black island 1 modbus ID.")
    __parser.add_argument("--conv_1", type=int, default=6, help="Convector 1 modbus ID.")
    __parser.add_argument("--conv_2", type=int, default=-1, help="Convector 2 modbus ID.")
    __parser.add_argument("--conv_3", type=int, default=-1, help="Convector 3 modbus ID.")
    __parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address of the device")
    __parser.add_argument("--fl_vlv_1", type=str, default="off", help="Floor loop 1 GPIO.")
    __parser.add_argument("--fl_vlv_2", type=str, default="off", help="Floor loop 2 GPIO.")
    __parser.add_argument("--fl_vlv_3", type=str, default="off", help="Floor loop 3 GPIO.")
    __parser.add_argument("--cl_vlv_1", type=str, default="off", help="Convector loop 1 GPIO.")
    __parser.add_argument("--cl_vlv_2", type=str, default="off", help="Convector loop 2 GPIO.")
    __parser.add_argument("--cl_vlv_3", type=str, default="off", help="Convector loop 3 GPIO.")
    __parser.add_argument("--conv_1_s1", type=str, default="off", help="Convector loop 1 GPIO.")
    __parser.add_argument("--conv_1_s2", type=str, default="off", help="Convector loop 2 GPIO.")
    __parser.add_argument("--conv_1_s3", type=str, default="off", help="Convector loop 3 GPIO.")
    __parser.add_argument("--conv_2_s1", type=str, default="off", help="Convector loop 1 GPIO.")
    __parser.add_argument("--conv_2_s2", type=str, default="off", help="Convector loop 2 GPIO.")
    __parser.add_argument("--conv_2_s3", type=str, default="off", help="Convector loop 3 GPIO.")
    __parser.add_argument("--conv_3_s1", type=str, default="off", help="Convector loop 1 GPIO.")
    __parser.add_argument("--conv_3_s2", type=str, default="off", help="Convector loop 2 GPIO.")
    __parser.add_argument("--conv_3_s3", type=str, default="off", help="Convector loop 3 GPIO.")
    __parser.add_argument("--pa_model", type=str, default="SDM120", help="Model of the power analyzer.")

    # Take arguments.
    args = __parser.parse_args()

    return args

def __add_registers(args):

    global __registers, __range

#region Access Control (ac)

    register = Register("ac.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

    register = Register("ac.allowed_attendees")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Allowed attendees"
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
    register.value = [] # {"card_id": "445E6046010080FF", "ts":"1595322860"}
    __registers.append(register)

    register = Register("ac.last_update_attendees")
    register.scope = Scope.Device
    register.plugin_name = "Access Control"
    register.description = "Last update attendee"
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
    register.value = {} # "Teracom/act230/2911"
    __registers.append(register)

    # Exit card reader.
    register = Register("ac.exit_reader_1.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader enabled"
    register.range = __range["NONE"]
    register.value = {} # "Teracom/act230/2897"
    __registers.append(register)

    #
    register = Register("ac.exit_button_1.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Exit button 1 input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF
    __registers.append(register)

    register = Register("ac.lock_mechanism_1.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock mechanism output"
    register.range = __range["DO"]
    register.value = verbal_const.OFF
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
    register.range = __range["NONE"]
    register.value = {} # "Teracom/act230/2486"
    __registers.append(register)

    # Exit card reader.
    register = Register("ac.exit_reader_2.enabled")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Card reader settings"
    register.range = __range["NONE"]
    register.value = {} # "Teracom/act230/1208"
    __registers.append(register)

    #
    register = Register("ac.exit_button_2.input")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Exit button 2 input"
    register.range = __range["DI"]
    register.value = verbal_const.OFF
    __registers.append(register)

    register = Register("ac.lock_mechanism_2.output")
    register.scope = Scope.System
    register.plugin_name = "Access Control"
    register.description = "Lock 2 mechanism output"
    register.range = __range["DO"]
    register.value = verbal_const.OFF
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
    register.value = verbal_const.OFF
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
    register.value = verbal_const.OFF
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

    register = Register("blinds.blind_1.mechanism")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Window 1 blinds mechanism"
    register.range = __range["NONE"]
    if args.blinds_1 > -1:
        register.value = {
            "vendor": "Yihao",
            "model": "BlindsV2",
            "options":
            {
                "uart": 0,
                "mb_id": args.blinds_1
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("blinds.blind_1.position")
    register.scope = Scope.Device
    register.plugin_name = "Blinds"
    register.description = "Position [deg]"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.blind_1.object_height")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Object height [m]."
    register.range = "0.0/"
    register.value = 2.0
    __registers.append(register)

    register = Register("blinds.blind_1.sunspot_limit")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Sun spot limit [m]."
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)


    register = Register("blinds.blind_2.mechanism")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Window 2 blinds mechanism"
    register.range = __range["NONE"]
    if args.blinds_2 > -1:
        register.value = {
            "vendor": "Yihao",
            "model": "BlindsV2",
            "options":
            {
                "uart": 0,
                "mb_id": args.blinds_2
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("blinds.blind_2.position")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Position [deg]"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.blind_2.object_height")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Object height [m]."
    register.range = "0.0/"
    register.value = 2.0
    __registers.append(register)

    register = Register("blinds.blind_2.sunspot_limit")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Sun spot limit [m]."
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)


    register = Register("blinds.blind_3.mechanism")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Window 3 blinds mechanism"
    register.range = __range["NONE"]
    if args.blinds_3 > -1:
        register.value = {
            "vendor": "Yihao",
            "model": "BlindsV2",
            "options":
            {
                "uart": 0,
                "mb_id": args.blinds_3
            }
        }
    else:
        register.valve = {}
    __registers.append(register)

    register = Register("blinds.blind_3.position")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Position [deg]"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.blind_3.object_height")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Object height [m]."
    register.range = "0.0/"
    register.value = 2.0
    __registers.append(register)

    register = Register("blinds.blind_3.sunspot_limit")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Sun spot limit [m]."
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)


    register = Register("blinds.blind_4.mechanism")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Window 4 blinds mechanism"
    register.range = __range["NONE"]
    if args.blinds_4 > -1:
        register.value = {
            "vendor": "Yihao",
            "model": "BlindsV2",
            "options":
            {
                "uart": 0,
                "mb_id": args.blinds_4
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("blinds.blind_4.position")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Position [deg]"
    register.range = "0.0/180.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("blinds.blind_4.object_height")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Object height [m]."
    register.range = "0.0/"
    register.value = 2.0
    __registers.append(register)

    register = Register("blinds.blind_4.sunspot_limit")
    register.scope = Scope.Both
    register.plugin_name = "Blinds"
    register.description = "Sun spot limit [m]."
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)


    register = Register("blinds.count")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Number of blind controllers"
    register.range = "1/"
    register.value = 1
    __registers.append(register)

    register = Register("blinds.enabled")
    register.scope = Scope.System
    register.plugin_name = "Blinds"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

#endregion

#region Monitoring (mon)

    # Enable flag.
    register = Register("monitoring.enabled")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # Cold water flow meter.
    register = Register("monitoring.cw.flowmeter_settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Cold water flow meter"
    register.range = __range["NONE"]
    if args.cw > -1:
        register.value = {
            "model": "mw_uml_15",
            "options": {
                "mb_id": args.cw,
                "uart": 1
            },
            "vendor": "smii"
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.cw.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Cold water liters"
    register.range = __range["NONE"]
    register.value = []
    __registers.append(register)

    register = Register("monitoring.cw.leak")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Cold water leaked liters"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)


    # Hot water flow meter.
    register = Register("monitoring.hw.flowmeter_settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Hot water input flow meter"
    register.range = __range["NONE"]
    if args.hw > -1:
        register.value = {
            "model": "mw_uml_15",
            "options": {
                "mb_id": args.hw,
                "uart": 1
            },
            "vendor": "smii"
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.hw.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Hot water liters"
    register.range = __range["NONE"]
    register.value = []
    __registers.append(register)

    register = Register("monitoring.hw.leak")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Hot water leaked liters"
    register.range = "0.0/"
    register.value = 1.0
    __registers.append(register)


    # Power analyzer.
    register = Register("monitoring.pa.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Power analyzer settings"
    register.range = __range["NONE"]
    if args.pa > -1:
        register.value = {
            "vendor": "Eastron",
            "model": args.pa_model,
            "options":
            {
                "uart": 0,
                "mb_id": args.pa,
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.pa.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Power analyzer measurements"
    register.range = __range["NONE"]
    register.value = []
    __registers.append(register)

    # ====================== NEW ======================

    register = Register("monitoring.demand_time")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Measuring demand"
    register.range = "0.0/"
    register.value = 3600.0 # Every hour to measure the consumed electricity.
    __registers.append(register)


    register = Register("monitoring.fl_1.hm.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Floor loop 1 heat meter settings."
    register.range = __range["NONE"]
    if args.fl_1_hm > -1:
        register.value = {
            "vendor": "mainone",
            "model": "flowmeter_dn20",
            "options":
            {
                "uart": 1,
                "mb_id": args.fl_1_hm,
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.fl_1.hm.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Floor loop 1 heat meter measurements."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)


    register = Register("monitoring.fl_2.hm.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Floor loop 2 heat meter settings."
    register.range = __range["NONE"]
    if args.fl_2_hm > -1:
        register.value = {
            "vendor": "mainone",
            "model": "flowmeter_dn20",
            "options":
            {
                "uart": 1,
                "mb_id": args.fl_2_hm,
            }
        }
    else:
        register.value = {}
    __registers.append(register)


    register = Register("monitoring.fl_2.hm.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Floor loop 2 heat meter measurements."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)


    register = Register("monitoring.fl_3.hm.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Floor loop 3 heat meter settings."
    register.range = __range["NONE"]
    if args.fl_3_hm > -1:
        register.value = {
            "vendor": "mainone",
            "model": "flowmeter_dn20",
            "options":
            {
                "uart": 1,
                "mb_id": args.fl_3_hm,
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.fl_3.hm.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Floor loop 3 heat meter measurements."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)


    register = Register("monitoring.cl_1.hm.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Convector loop 1 heat meter settings."
    register.range = __range["NONE"]
    if args.cl_1_hm > -1:
        register.value = {
            "vendor": "mainone",
            "model": "flowmeter_dn20",
            "options":
            {
                "uart": 1,
                "mb_id": args.cl_1_hm,
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.cl_1.hm.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Convector loop 1 heat meter measurements."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)


    register = Register("monitoring.cl_2.hm.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Convector loop 2 heat meter settings."
    register.range = __range["NONE"]
    if args.cl_2_hm > -1:
        register.value = {
            "vendor": "mainone",
            "model": "flowmeter_dn20",
            "options":
            {
                "uart": 1,
                "mb_id": args.cl_2_hm,
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.cl_2.hm.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Convector loop 2 heat meter measurements."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)


    register = Register("monitoring.cl_3.hm.settings")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Convector loop 3 heat meter settings."
    register.range = __range["NONE"]
    if args.cl_3_hm > -1:
        register.value = {
            "vendor": "mainone",
            "model": "flowmeter_dn20",
            "options":
            {
                "uart": 1,
                "mb_id": args.cl_3_hm,
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("monitoring.cl_3.hm.measurements")
    register.scope = Scope.Device
    register.plugin_name = "Monitoring"
    register.description = "Convector loop 3 heat meter measurements."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)


    # ====================== DEPRICATED ======================

    register = Register("monitoring.pa.demand_time")
    register.scope = Scope.System
    register.plugin_name = "Monitoring"
    register.description = "Power analyzer measuring demand"
    register.range = "0.0/"
    register.value = 3600.0 # Every hour to measure the consumed electricity.
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

    register = Register("envm.forecast.icon_0")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual weather icon."
    register.range = __range["NONE"]
    register.value = ""
    __registers.append(register)

    register = Register("envm.forecast.rh_0")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside relative humidity [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.temp_0")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature [*C]"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.wind_0")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside wind speed [m/s]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.icon_3")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside weather icon for 3 hours."
    register.range = __range["NONE"]
    register.value = ""
    __registers.append(register)

    register = Register("envm.forecast.rh_3")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside relative humidity for 3 hours.[%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.temp_3")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature for 3 hours. [*C]"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.wind_3")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside wind speed for 3 hours. [m/s]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.icon_6")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside weather icon for 6 hours."
    register.range = __range["NONE"]
    register.value = ""
    __registers.append(register)

    register = Register("envm.forecast.rh_6")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside relative humidity for 6 hours.[%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.temp_6")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside temperature for 6 hours. [*C]"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    register = Register("envm.forecast.wind_6")
    register.scope = Scope.System
    register.plugin_name = "Environment"
    register.description = "Actual outside wind speed for 6 hours. [m/s]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
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
    register.range = __range["NONE"]
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
    register.plugin_name = "Environment"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = True
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

    # HVAC Enabled.
    register = Register("hvac.enabled")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Plugin enabled"
    register.range = __range["BOOL"]
    register.value = True
    __registers.append(register)

    # Zones count.
    register = Register("hvac.zones_count")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Count of the HVAC zones."
    register.range = "0/"
    register.value = 1
    __registers.append(register)

    # Air temp central.
    register = Register("hvac.air_temp_cent_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor center settings."
    register.range = __range["NONE"]
    if args.temp_cent > -1:
        register.value = {
            "vendor": "Gemho",
            "model": "Envse",
            "options":
            {
                "uart": 0,
                "mb_id": args.temp_cent
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("hvac.air_temp_cent_1.value")
    register.scope = Scope.Device
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor center value."
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    # Air temp lower
    register = Register("hvac.air_temp_lower_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor lower settings"
    register.range = __range["NONE"]
    if  args.temp_lower > -1:
        register.value = {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "uart": 0,
                "mb_id": args.temp_lower
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("hvac.air_temp_lower_1.value")
    register.scope = Scope.Device
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor lower value"
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    # Air temp upper.
    register = Register("hvac.air_temp_upper_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor upper settings"
    register.range = __range["NONE"]
    if args.temp_upper > -1:
        register.value = {
            "vendor": "Donkger",
            "model": "XY-MD02",
            "options":
            {
                "uart": 0,
                "mb_id": args.temp_upper
            }
        }
    else:
        register.value = {}
    __registers.append(register)

    register = Register("hvac.air_temp_upper_1.value")
    register.scope = Scope.Device
    register.plugin_name = "HVAC"
    register.description = "Air temperature sensor upper value"
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    register = Register("hvac.floor_loop_1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Floor loop 1 valve"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": 
            [
                args.fl_vlv_1 #"U0:ID2:FC5:R0:RO0",
            ]
        }
    }
    __registers.append(register)

    register = Register("hvac.floor_loop_2.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Floor loop 2 valve"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": 
            [
                args.fl_vlv_2 #"U0:ID2:FC5:R0:RO1",
            ]
        }
    }
    __registers.append(register)

    register = Register("hvac.floor_loop_3.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Floor loop 3 valve"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": 
            [
                args.fl_vlv_3 #"U0:ID2:FC5:R0:RO2",
            ]
        }
    }
    __registers.append(register)

    # Convector loop 1
    register = Register("hvac.convector_1.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector 1"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Silpa",
        "model": "Klimafan",
        "options":
        {
            "stage1": 
            [
                args.conv_1_s1 #"U0:ID6:FC5:R0:RO0",
            ],
            "stage2":
            [
                args.conv_1_s2 #"U0:ID6:FC5:R0:RO1",
            ],
            "stage3": 
            [
                args.conv_1_s3 #"U0:ID6:FC5:R0:RO2",
            ]
        }
    }
    __registers.append(register)

    register = Register("hvac.conv_loop_1.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector loop 1 valve"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": 
            [
                args.cl_vlv_1 #"U0:ID2:FC5:R0:RO0",
            ]
        }
    }
    __registers.append(register)

    # Convector loop 2
    register = Register("hvac.convector_2.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector 2"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Silpa",
        "model": "Klimafan",
        "options":
        {
            "stage1": 
            [
                args.conv_2_s1 #"U0:ID7:FC5:R0:RO0",
            ],
            "stage2":
            [
                args.conv_2_s2 #"U0:ID7:FC5:R0:RO1",
            ],
            "stage3": 
            [
                args.conv_2_s3 #"U0:ID7:FC5:R0:RO2",
            ]
        }
    }
    __registers.append(register)

    register = Register("hvac.conv_loop_2.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector loop 2 valve"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": 
            [
                args.cl_vlv_2 #"U0:ID7:FC5:R0:RO4",
            ]
        }
    }
    __registers.append(register)

    # Convector loop 3 flowmeter.
    register = Register("hvac.convector_3.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector 3"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Silpa",
        "model": "Klimafan",
        "options":
        {
            "stage1": 
            [
                args.conv_3_s1 #"U0:ID8:FC5:R0:RO0",
            ],
            "stage2":
            [
                args.conv_3_s2 #"U0:ID8:FC5:R0:RO1",
            ],
            "stage3": 
            [
                args.conv_3_s3 #"U0:ID8:FC5:R0:RO2",
            ]
        }
    }
    __registers.append(register)

    register = Register("hvac.conv_loop_3.valve.settings")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Convector loop 3 valve"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Tonhe",
        "model": "a20t20b2c",
        "options":
        {
            "output": 
            [
                args.cl_vlv_3 #"U0:ID8:FC5:R0:RO4",
            ]
        }
    }
    __registers.append(register)

    # Loop 1 Down Limit Temperature # Request: Eml6419
    register = Register("hvac.floor_loop_1.temp.down_limit")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature down limit."
    register.range = "0.0/"
    register.value = 15
    __registers.append(register)

    register = Register("hvac.conv_loop_1.temp.down_limit")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Loop 1 temperature sensor value."
    register.range = "/"
    register.value = 0.0
    __registers.append(register)

    register = Register("hvac.temp_1.adjust")
    register.scope = Scope.Device
    register.plugin_name = "HVAC"
    register.description = "Adjust temperature"
    register.range = "-50.0/50.0"
    register.value = 0.0
    __registers.append(register)

    # Delta time.
    register = Register("hvac.delta_time_1")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Measuring delta time"
    register.range = "0.0/"
    register.value = 5.0
    __registers.append(register)

    # Goal building temp.
    register = Register("hvac.goal_building_temp")
    register.scope = Scope.System
    register.plugin_name = "HVAC"
    register.description = "Goal of the building temperature"
    register.range = "-50.0/50.0"
    register.value = 20.0
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
    register.value = 1.0
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
    register.description = "Analog output 0. U0:ID2:FC16:R0:AO0"
    register.range = __range["NONE"]
    register.value = "U0:ID2:FC16:R0:AO0"
    __registers.append(register)

    register = Register("light.v2.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Analog output 1. U0:ID2:FC16:R0:AO1"
    register.range = __range["NONE"]
    register.value = "U0:ID2:FC16:R0:AO1"
    __registers.append(register)

    register = Register("light.r1.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Digital output 6. U0:ID2:FC5:R0:DO6"
    register.range = __range["NONE"]
    register.value = "U0:ID2:FC5:R0:DO6"
    __registers.append(register)

    register = Register("light.r2.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Digital output 7. U0:ID2:FC5:R0:DO7"
    register.range = __range["NONE"]
    register.value = "U0:ID2:FC5:R0:DO7"
    __registers.append(register)

    register = Register("light.hallway_lighting.output")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Hallway lighting digital output. U1:ID2:R0:DO3"
    register.range = __range["NONE"]
    register.value = verbal_const.OFF # U1:ID2:R0:DO3
    __registers.append(register)

    register = Register("light.hallway_lighting.time")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Hallway lighting wait time."
    register.range = "0.0/"
    register.value = 60.0
    __registers.append(register)

    register = Register("light.sensor.settings")
    register.scope = Scope.System
    register.plugin_name = "Light"
    register.description = "Sensor settings"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "PT",
        "model": "light_sensor",
        "options":
        {
            "input": "AI2",
        }
    }
    __registers.append(register)

    register = Register("light.target_illum")
    register.scope = Scope.Device
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
    register.value = True
    __registers.append(register)

#endregion

#region System (sys)

    # Last 60 seconds
    register = Register("sys.last_update_errs")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Last update cycle error"
    register.range = __range["NONE"]
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

    register = Register("sys.time.boot")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "OS boot time."
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    register = Register("sys.time.uptime")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "OS uptime."
    register.range = "0.0/"
    register.value = 0.0
    __registers.append(register)

    register = Register("sys.time.startup")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Application startup time."
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
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)

    register = Register("sys.col.warning_message")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Collision warning message"
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)

    register = Register("sys.col.error_message")
    register.scope = Scope.Device
    register.plugin_name = "System"
    register.description = "Collision error message"
    register.range = __range["NONE"]
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
    register.value = True
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

    # ECD / Pool air heating valves settings.
    register = Register("ecd.pool_air_heating.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO6",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI0",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID6:FC5:R0:RO7",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI2",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ]
    }
    __registers.append(register)

    # ECD / Pool air heating valves mode.
    register = Register("ecd.pool_air_heating.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Pool air heating valves state.
    register = Register("ecd.pool_air_heating.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Pool air heating pump settings.
    register = Register("ecd.pool_air_heating.pump.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating pump settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "vendor": "Grundfos",
        "model": "MAGNA1_80_100_F_360_1x230V_PN6",
        "options":
        {
            "uart": 1,
            "mb_id": 1,
            "start_stop": "U0:ID2:FC5:R0:RO8" 
        }
    }
    __registers.append(register)

    # ECD / Pool air heating pump mode.
    register = Register("ecd.pool_air_heating.pump.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating pump mode."
    register.range = __range["PERCENTAGE_I"]
    register.value = 0
    __registers.append(register)


    # ECD / Pool air heating pump state.
    register = Register("ecd.pool_air_heating.pump.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating pump state."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)

    # ECD / Convectors kitchen valves settings.
    register = Register("ecd.conv_kitchen.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors kitchen valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO4",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI0",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO5",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI2",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Convectors kitchen valves mode.
    register = Register("ecd.conv_kitchen.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors kitchen valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Convectors kitchen valves state.
    register = Register("ecd.conv_kitchen.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors kitchen valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)


    # ECD / AHU conference hall valves settings.
    register = Register("ecd.ahu_conf_hall.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU conference hall valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO2",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI0",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO3",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI2",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / AHU conference hall valves mode.
    register = Register("ecd.ahu_conf_hall.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU conference hall valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / AHU conference hall valves state.
    register = Register("ecd.ahu_conf_hall.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU Warehouse Position"
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor west valves settings.
    register = Register("ecd.floor_west.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor west valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO0",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI0",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO1",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI2",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Floor west valves mode.
    register = Register("ecd.floor_west.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor west valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor west valves state.
    register = Register("ecd.floor_west.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU Warehouse Position"
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Convectors west valves settings.
    register = Register("ecd.conv_west.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors west valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO6",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI0",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO7",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI2",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Convectors west valves mode.
    register = Register("ecd.conv_west.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors west valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Convectors west valves state.
    register = Register("ecd.conv_west.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors west valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / AHU roof floor valves settings.
    register = Register("ecd.ahu_roof_floor.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU roof floor valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO4",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI0",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO5",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI2",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / AHU roof floor valves mode.
    register = Register("ecd.ahu_roof_floor.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU roof floor valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / AHU roof floor valves state.
    register = Register("ecd.ahu_roof_floor.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU roof floor valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / AHU fitness valves settings.
    register = Register("ecd.ahu_fitness.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "# ECD / AHU fitness valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO2",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI0",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO3",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI2",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / AHU fitness valves mode.
    register = Register("ecd.ahu_fitness.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU fitness valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / AHU fitness valves state.
    register = Register("ecd.ahu_fitness.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / AHU fitness valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor east valves settings.
    register = Register("ecd.floor_east.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor east valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO0",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI0",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID7:FC5:R0:RO1",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID7:FC2:R0:DI2",
                    "limit_ccw": "U0:ID7:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Floor east valves mode.
    register = Register("ecd.floor_east.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor east valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor east valves state.
    register = Register("ecd.floor_east.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor east valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Convectors east valves settings.
    register = Register("ecd.conv_east.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors east valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO6",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI0",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO7",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI2",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Convectors east valves mode.
    register = Register("ecd.conv_east.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors east valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Convectors east valves state.
    register = Register("ecd.conv_east.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Convectors east valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Pool air cooling valves settings.
    register = Register("ecd.pool_air_cooling.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air cooling valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID6:FC5:R0:RO6",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID6:FC5:R0:RO7",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI2",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Pool air cooling valves mode.
    register = Register("ecd.pool_air_cooling.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air cooling valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Pool air cooling valves state.
    register = Register("ecd.pool_air_cooling.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air cooling valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Pool air heating valves settings.
    register = Register("ecd.pool_heating.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO0",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO0",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI2",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Pool air heating valves mode.
    register = Register("ecd.pool_heating.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Pool air heating valves state.
    register = Register("ecd.pool_heating.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Pool air heating valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor entrance valves settings.
    register = Register("ecd.floor_entrance.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor entrance valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO1",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO1",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID6:FC2:R0:DI2",
                    "limit_ccw": "U0:ID6:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Floor entrance valves mode.
    register = Register("ecd.floor_entrance.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor entrance valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor entrance valves state.
    register = Register("ecd.floor_entrance.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor entrance valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor pool valves settings.
    register = Register("ecd.pool_floor.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor pool valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO2",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO2",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI2",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Floor pool valves mode.
    register = Register("ecd.pool_floor.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor pool valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Floor pool valves state.
    register = Register("ecd.pool_floor.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Floor pool valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Ground drilling valves settings.
    register = Register("ecd.ground_drilling.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO2",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO3",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI2",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Ground drilling valves mode.
    register = Register("ecd.ground_drilling.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Ground drilling valves state.
    register = Register("ecd.ground_drilling.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Air tower green valves settings.
    register = Register("ecd.air_tower_green.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO2",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO4",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI2",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Air tower green valves mode.
    register = Register("ecd.air_tower_green.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Air tower green valves state.
    register = Register("ecd.air_tower_green.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Air tower green valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Air tower green valves settings.
    register = Register("ecd.air_tower_purple.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO2",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO5",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI2",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Air tower green valves mode.
    register = Register("ecd.air_tower_purple.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Air tower green valves state.
    register = Register("ecd.air_tower_purple.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Air tower green valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Generators valves settings.
    register = Register("ecd.generators.valves.settings")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Generators valves settings."
    register.range = __range["NONE"]
    register.value = \
    {
        "hot":
        [
            # {
            #     "vendor": "Flowx",
            #     "model": "FLX-05F",
            #     "options":
            #     {
            #         "close_on_shutdown": True,
            #         "wait_on_shutdown": False,
            #         "io_mode": 1, # 1: "single_out", 2: "dual_out"
            #         "output_cw": "U0:ID2:FC5:R0:RO2",
            #         "output_ccw": "off",
            #         "limit_cw": "U0:ID6:FC2:R0:DI0",
            #         "limit_ccw": "U0:ID6:FC2:R0:DI1"
            #     }
            # }
        ],
        "cold":
        [
            {
                "vendor": "Flowx",
                "model": "FLX-05F",
                "options":
                {
                    "close_on_shutdown": True,
                    "wait_on_shutdown": False,
                    "io_mode": 1, # 1: "single_out", 2: "dual_out"
                    "output_cw": "U0:ID2:FC5:R0:RO11",
                    "output_ccw": "off",
                    "limit_cw": "U0:ID2:FC2:R0:DI2",
                    "limit_ccw": "U0:ID2:FC2:R0:DI1"
                }
            }
        ]
    }
    __registers.append(register)

    # ECD / Generators valves mode.
    register = Register("ecd.generators.valves.mode")
    register.scope = Scope.System
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Ground drilling valves mode."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
    __registers.append(register)

    # ECD / Generators valves state.
    register = Register("ecd.generators.valves.state")
    register.scope = Scope.Device
    register.plugin_name = "Energy Center Distribution"
    register.description = "ECD / Generators valves state."
    register.range = __range["PERCENTAGE_-100_100"]
    register.value = 0.0
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
    register.range = __range["NONE"]
    register.value = 0
    __registers.append(register)

    register = Register("echp.hp.run")
    register.scope = Scope.Device
    register.plugin_name = "ECHP"
    register.description = "The state of the machine"
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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

    # Heat Pump Control Group / VCG / Cold Buffer / Output
    register = Register("echp.hpcg.vcg_cold_buf.output")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Buffer / Output"
    register.range = __range["NONE"]
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

    # Heat Pump Control Group / VCG / Cold Buffer / Short
    register = Register("echp.hpcg.vcg_cold_buf.short")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Buffer / Short"
    register.range = __range["NONE"]
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

    # Heat Pump Control Group / VCG / Cold Geo / Input
    register = Register("echp.hpcg.vcg_cold_geo.input")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / VCG / Cold Geo / Input"
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
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
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Grundfos",
        "model": "MAGNA1_80_100_F_360_1x230V_PN6",
        "options":
        {
            "uart": 0,
            "mb_id": 2
        }
    }
    __registers.append(register)

    # Heat Pump Control Group / Water Pump / Hot
    register = Register("echp.hpcg.wp_hot.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Hot"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Grundfos",
        "model": "MAGNA1_80_100_F_360_1x230V_PN6",
        "options":
        {
            "uart": 0,
            "mb_id": 3
        }
    }
    __registers.append(register)

    # Heat Pump Control Group / Water Pump / Warm
    register = Register("echp.hpcg.wp_warm_p.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Warm"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Grundfos",
        "model": "MAGNA1_80_100_F_360_1x230V_PN6",
        "options":
        {
            "uart": 0,
            "mb_id": 0
        }
    }
    __registers.append(register)

    # Heat Pump Control Group / Water Pump / Warm
    register = Register("echp.hpcg.wp_warm_g.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Water Pump / Warm"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "Grundfos",
        "model": "MAGNA1_80_100_F_360_1x230V_PN6",
        "options":
        {
            "uart": 0,
            "mb_id": 0
        }
    }
    __registers.append(register)

    # -================================================================================-

    # Heat Pump Control Group / Water Pump / Warm
    register = Register("echp.hpcg.hp.settings")
    register.scope = Scope.System
    register.plugin_name = "ECHP"
    register.description = "Heat Pump Control Group / Heat Pump"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "HstarsGuangzhouRefrigeratingEquipmentGroup",
        "model": "40STD-N420WHSB4",
        "options":
        {
            "uart": 0,
            "mb_id": 0
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
    register.scope = Scope.Device
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

    register = Register("vent.power_gpio_1")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Fans power GPIO."
    register.range = __range["NONE"]
    register.value = "U0:ID6:FC5:R0:RO3"
    __registers.append(register)

    # Upper fan
    register = Register("vent.lower_1.fan.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Lower fan settings"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "HangzhouAirflowElectricApplications",
        "model": "f3p146ec072600",
        "options":
        {
            "output": "U0:ID2:FC16:R0:AO3",
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
    register.value = 100.0
    __registers.append(register)

    register = Register("vent.lower_1.fan.speed")
    register.scope = Scope.Device
    register.plugin_name = "Ventilation"
    register.description = "Lower fan speed [%]"
    register.range = __range["PERCENTAGE_F"]
    register.value = 0.0
    __registers.append(register)

    # Upper fan
    register = Register("vent.upper_1.fan.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper fan settings"
    register.range = __range["NONE"]
    register.value = {
        "vendor": "HangzhouAirflowElectricApplications",
        "model": "f3p146ec072600",
        "options":
        {
            "output": "U0:ID2:FC16:R0:AO2",
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
    register.scope = Scope.Device
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
    register.value = 100.0
    __registers.append(register)

    # Upper valve settings
    register = Register("vent.upper_1.air_damper.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Lower air damper settings"
    register.range = __range["NONE"]
    register.value = verbal_const.OFF
    __registers.append(register)

    # Lower valve settings
    register = Register("vent.lower_1.air_damper.settings")
    register.scope = Scope.System
    register.plugin_name = "Ventilation"
    register.description = "Upper air damper settings"
    register.range = __range["NONE"]
    register.value = verbal_const.OFF
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
    register.range = __range["NONE"]
    register.value = True
    __registers.append(register)

#endregion

#region Alarm (alarm)

    # Visual signal device.
    register = Register("alarm.device.sound.settings")
    register.scope = Scope.System
    register.plugin_name = "Alarm"
    register.description = "Alarm module sound device settings."
    register.range = __range["NONE"]
    register.value = {}
    __registers.append(register)

    # Visual signal device.
    register = Register("alarm.device.visual.settings")
    register.scope = Scope.System
    register.plugin_name = "Alarm"
    register.description = "Alarm module visual device settings."
    register.range = __range["NONE"]
    register.value = {}
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
    register.value = False
    __registers.append(register)

#endregion

#region Office Conference Hall (oc_hall)

    # Enable
    register = Register("oc_hall.enabled")
    register.scope = Scope.System
    register.plugin_name = "Office Conference Hall"
    register.description = "Office conference hall module enable flag."
    register.range = __range["BOOL"]
    register.value = False
    __registers.append(register)

#endregion

def main():
    global __registers, __range, __parser

    __parser = argparse.ArgumentParser()

    __registers = Registers()

    # File extetion.
    __f_ext = ""

    args = __set_parser()
    __add_registers(args)


    if args.action.endswith("json"):
        __f_ext = "json"
    if args.action.endswith("csv"):
        __f_ext = "csv"
    if args.action.endswith("md"):
        __f_ext = "md"

    # Current file path. & Go to file.
    cwf = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(cwf, "..", f"registers.{__f_ext}")


    if args.action == "w_json":
        Registers.to_json(__registers, file_name)

    elif args.action == "r_json":
        registers = Registers.from_json(file_name)

        for register in registers:
            print(register)

    elif args.action == "w_csv":
        Registers.to_csv(__registers, file_name)

    elif args.action == "r_csv":
        registers = Registers.from_csv(file_name)

        for register in registers:
            print(register)

    elif args.action == "list_gpio":
        for register in __registers:
            if isinstance(register.value, dict):
                if "options" in register.value.keys():
                    print("Register: {} -> {}".format(register.name, register.value["options"]))                    

    elif args.action == "w_md":
        Registers.to_md(__registers, file_name) #"../Zontromat/plugins/registers.md")

if __name__ == "__main__":
    main()
