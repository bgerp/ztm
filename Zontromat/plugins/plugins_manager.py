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

import os

from enum import Enum

from utils.logger import get_logger

from data.register import Scope
from data.register import Source
from data.register import Register
from data import verbal_const 
from data import doc_generator

# Plugins
from plugins.access_control.access_control import AccessControl
from plugins.blinds.blinds import Blinds
from plugins.monitoring.monitoring import Monitoring
from plugins.environment.environment import Environment
from plugins.hvac.hvac import HVAC
from plugins.lighting.lighting import Lighting
from plugins.sys.sys import Sys

from services.global_error_handler.global_error_handler import GlobalErrorHandler

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

class Plugins(Enum):
    """Zone device enumerator."""

    AccessControl = 1
    Blinds = 2
    Monitoring = 3
    Environment = 4
    HVAC = 5
    MainLight = 6
    Sys = 7

class PluginsManager:
    """Template class doc."""

#region Attributes

    __logger = None
    """Logger"""

    __registers = None
    """Registers"""

    __controller = None
    """Controller"""

    __plugins = None
    """Plugins"""

#endregion

#region Constructor

    def __init__(self, registers, controller):
        """Constructor

        Parameters
        ----------
        registers : Registers
            Registers class instance.
        controller : mixed
            Hardware controller.
        """

        self.__logger = get_logger(__name__)
        self.__plugins = {}
        self.__registers = registers
        self.__controller = controller
        self.__add_registers()

#endregion

#region Private Methods

    def __prepare_config(self, name, key):

        config = {
            "name": name,
            "key": key,
            "registers": self.__registers,
            "controller": self.__controller,
        }

        return config

    def __add_registers(self):

#region Access Control (ac)

        register = Register("ac.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__access_control_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("ac.allowed_attendees")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = [] # {"card_id": "445E6046010080FF", "pin":"159753", "valid_until":"1595322860"}
        self.__registers.add(register)

        register = Register("ac.nearby_attendees")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = [] # {"card_id": "445E6046010080FF", "ts":"1595322860"}
        self.__registers.add(register)

        register = Register("ac.last_minute_attendees")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = [] # {"card_id": "445E6046010080FF", "ts":"1595322860", "reader_id":"2911"}
        self.__registers.add(register)

        register = Register("ac.next_attendance")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0 # 1595322860
        self.__registers.add(register)

        register = Register("ac.zone_occupied")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        # Entry card reader.
        register = Register("ac.entry_reader_1.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM/act230/2897"
        self.__registers.add(register)

        register = Register("ac.entry_reader_1.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.entry_reader_1.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM5"
        self.__registers.add(register)

        # Exit card reader.
        register = Register("ac.exit_reader_1.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM/act230/2911"
        self.__registers.add(register)

        register = Register("ac.exit_reader_1.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.exit_reader_1.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM11"
        self.__registers.add(register)

        # 
        register = Register("ac.exit_button_1.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.lock_mechanism_1.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DO2"
        self.__registers.add(register)

        register = Register("ac.time_to_open_1")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("ac.door_closed_1.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI2"
        self.__registers.add(register)

        register = Register("ac.door_closed_1.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)
        
        # Entry card reader 2.
        register = Register("ac.entry_reader_2.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM/act230/2897"
        self.__registers.add(register)


        register = Register("ac.entry_reader_2.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.entry_reader_2.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM5"
        self.__registers.add(register)

        # Exit card reader.
        register = Register("ac.exit_reader_2.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM/act230/2911"
        self.__registers.add(register)

        register = Register("ac.exit_reader_2.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.exit_reader_2.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM11"
        self.__registers.add(register)

        # 
        register = Register("ac.exit_button_2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.lock_mechanism_2.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DO2"
        self.__registers.add(register)

        register = Register("ac.time_to_open_2")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("ac.door_closed_2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI2"
        self.__registers.add(register)

        register = Register("ac.door_closed_2.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)

        #
        register = Register("ac.pir_1.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.pir_1.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)

        register = Register("ac.pir_2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.pir_2.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)

        #
        register = Register("ac.window_closed_1.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "!DI3"
        self.__registers.add(register)

        register = Register("ac.window_closed_1.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)

        register = Register("ac.window_closed_2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "!DI3"
        self.__registers.add(register)

        register = Register("ac.window_closed_2.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)

#endregion

#region Blinds (blinds)

        register = Register("blinds.sun.azimuth.value")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("blinds.sun.azimuth.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "deg"
        self.__registers.add(register)

        register = Register("blinds.sun.elevation.value")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("blinds.sun.elevation.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "deg"
        self.__registers.add(register)

        register = Register("blinds.input_fb")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AI0" # "DI8"
        self.__registers.add(register)

        register = Register("blinds.output_ccw")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DO0"
        self.__registers.add(register)

        register = Register("blinds.output_cw")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DO1"
        self.__registers.add(register)

        register = Register("blinds.position")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("blinds.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__blinds_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#region Monitoring (mon)

        # Cold water flow meter.
        register = Register("monitoring.cw.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI6"
        self.__registers.add(register)

        register = Register("monitoring.cw.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("monitoring.cw.value")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("monitoring.cw.leak")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 1
        self.__registers.add(register) 

        # Hot water flow meter.
        register = Register("monitoring.hw.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI7"
        self.__registers.add(register)

        register = Register("monitoring.hw.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("monitoring.hw.value")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("monitoring.hw.leak")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 1
        self.__registers.add(register) 

        # Power analyser.
        register = Register("monitoring.pa.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "mb-rtu/Eastron/SDM630/2/3"
        self.__registers.add(register)

        register = Register("monitoring.pa.l1")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = []
        self.__registers.add(register)

        register = Register("monitoring.pa.l2")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = []
        self.__registers.add(register)

        register = Register("monitoring.pa.l3")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = []
        self.__registers.add(register)

        # Enable flag.
        register = Register("monitoring.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__monitoring_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#region Environment (env)

        register = Register("env.is_empty")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 1
        self.__registers.add(register)

        register = Register("env.is_empty_timeout")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 3600
        self.__registers.add(register)

        register = Register("env.temp.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.temp.a6")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.temp.min24")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.temp.max24")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.rh")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.wind.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.wind.max12")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.light")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("env.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__env_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("env.energy") # Energy mode of the building.
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("env.emergency") # Emergency bit coded flags of the building.
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("env.sunpos.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#region HVAC (hvac)

        register = Register("hvac.adjust_temp")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        # Air temp central.
        register = Register("hvac.air_temp_cent.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp/DS18B20/28FFFCD0001703AE"
        self.__registers.add(register)

        # Air temp lower
        register = Register("hvac.air_temp_lower.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp/DS18B20/28FFC4EE00170349"
        self.__registers.add(register)

        # Air temp upper.
        register = Register("hvac.air_temp_upper.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp/DS18B20/28FF2B70C11604B7"
        self.__registers.add(register)

        # Convector
        register = Register("hvac.convector.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "silpa/klimafan"
        self.__registers.add(register)

        register = Register("hvac.convector.stage_1.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO0"
        self.__registers.add(register)

        register = Register("hvac.convector.stage_2.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO1"
        self.__registers.add(register)

        register = Register("hvac.convector.stage_3.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO2"
        self.__registers.add(register)

        # Delta time.
        register = Register("hvac.delta_time")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 5
        self.__registers.add(register)

        # HVAC Enabled.
        register = Register("hvac.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__hvac_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

        # Goal building temp.
        register = Register("hvac.goal_building_temp")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 20
        self.__registers.add(register)

        # Loop 1 flowmeter.
        register = Register("hvac.loop1.cnt.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.loop1.cnt.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI4"
        self.__registers.add(register)

        # Loop 1 fan
        register = Register("hvac.loop1.fan.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "HangzhouAirflowElectricApplications/f3p146ec072600"
        self.__registers.add(register)

        register = Register("hvac.loop1.fan.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO3"
        self.__registers.add(register)

        register = Register("hvac.loop1.fan.min_speed")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("hvac.loop1.fan.max_speed")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 30
        self.__registers.add(register)

        # Loop 1 Temperature
        register = Register("hvac.loop1.temp.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp/DS18B20/28FF2B70C11604B7"
        self.__registers.add(register)

        # Loop 1 valve.
        register = Register("hvac.loop1.valve.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TONHE/a20m15b2c"
        self.__registers.add(register)

        register = Register("hvac.loop1.valve.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO4"
        self.__registers.add(register)

        register = Register("hvac.loop1.valve.feedback")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AI1"
        self.__registers.add(register)

        register = Register("hvac.loop1.valve.max_pos")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
        self.__registers.add(register)

        register = Register("hvac.loop1.valve.min_pos")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        # Loop 2 flowmeter
        register = Register("hvac.loop2.cnt.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.loop2.cnt.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI5"
        self.__registers.add(register)

        # Loop 2 fan
        register = Register("hvac.loop2.fan.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "HangzhouAirflowElectricApplications/f3p146ec072600"
        self.__registers.add(register)

        register = Register("hvac.loop2.fan.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO4"
        self.__registers.add(register)

        register = Register("hvac.loop2.fan.min_speed")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("hvac.loop2.fan.max_speed")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 30
        self.__registers.add(register)

        # Loop 2 Temperature
        register = Register("hvac.loop2.temp.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp/DS18B20/28FFC4EE00170349"
        self.__registers.add(register)

        # Loop 2 valve.
        register = Register("hvac.loop2.valve.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TONHE/a20m15b2c"
        self.__registers.add(register)

        register = Register("hvac.loop2.valve.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO3"
        self.__registers.add(register)

        register = Register("hvac.loop2.valve.feedback")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AI2"
        self.__registers.add(register)

        register = Register("hvac.loop2.valve.max_pos")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
        self.__registers.add(register)

        register = Register("hvac.loop2.valve.min_pos")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        # Temperature actual
        register = Register("hvac.temp.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("hvac.temp.max")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 30
        self.__registers.add(register)

        register = Register("hvac.temp.min")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 20
        self.__registers.add(register)

        # Thermal force limit
        register = Register("hvac.thermal_force_limit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
        self.__registers.add(register)

        # Thermal mode
        register = Register("hvac.thermal_mode")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 2
        self.__registers.add(register)

        # Update rate.
        register = Register("hvac.update_rate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 3
        self.__registers.add(register)

#endregion

#region Light (light)

        register = Register("light.min")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 800
        self.__registers.add(register)

        register = Register("light.max")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10000
        self.__registers.add(register)

        register = Register("light.v1.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO1"
        self.__registers.add(register)

        register = Register("light.v2.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO2"
        self.__registers.add(register)

        register = Register("light.sensor.settings")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "1wdevice/26607314020000F8"
        self.__registers.add(register)

        # register = Register("light.sensor.model")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "u1wtvs"
        # self.__registers.add(register)

        # register = Register("light.sensor.vendor")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "SEDtronic"
        # self.__registers.add(register)

        register = Register("light.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__light_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#region System (sys)

        # Last 60 seconds
        register = Register("sys.last_minute_errs")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        GlobalErrorHandler.set_register(register)
        self.__registers.add(register)

        # Systrem resources
        register = Register("sys.ram.current")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("sys.ram.peak")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("sys.time.usage")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        # Status LED
        register = Register("sys.sl.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "LED0"
        self.__registers.add(register)

        register = Register("sys.sl.blink_time")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Anti tampering
        register = Register("sys.at.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI1"
        self.__registers.add(register)

        register = Register("sys.at.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = False
        self.__registers.add(register)

        # Colision detector
        register = Register("sys.col.info_message")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        self.__registers.add(register)

        register = Register("sys.col.warning_message")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        self.__registers.add(register)

        register = Register("sys.col.error_message")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        self.__registers.add(register)

        register = Register("sys.col.clear_errors")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        # Enable disable plugin.
        register = Register("sys.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.NO
        register.update_handler = self.__sys_enabled
        self.__registers.add(register)

#endregion

#endregion

#region Private Methods (ac)

    def __access_control_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.AccessControl not in self.__plugins:
            config = self.__prepare_config("Access control", register.base_name)
            self.__plugins[Plugins.AccessControl] = AccessControl(config)
            self.__plugins[Plugins.AccessControl].init()

        elif register.value == verbal_const.NO and Plugins.AccessControl in self.__plugins:
            self.__plugins[Plugins.AccessControl].shutdown()
            del self.__plugins[Plugins.AccessControl]

#endregion

#region Private Methods (blinds)

    def __blinds_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.Blinds not in self.__plugins:
            config = self.__prepare_config("Blinds", register.base_name)
            self.__plugins[Plugins.Blinds] = Blinds(config)
            self.__plugins[Plugins.Blinds].init()

        elif register.value == verbal_const.NO and Plugins.Blinds in self.__plugins:
            self.__plugins[Plugins.Blinds].shutdown()
            del self.__plugins[Plugins.Blinds]

#endregion

#region Private Methods (mon)

    def __monitoring_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.Monitoring not in self.__plugins:
            config = self.__prepare_config("Monitoring", register.base_name)
            self.__plugins[Plugins.Monitoring] = Monitoring(config)
            self.__plugins[Plugins.Monitoring].init()

        elif register.value == verbal_const.NO and Plugins.Monitoring in self.__plugins:
            self.__plugins[Plugins.Monitoring].shutdown()
            del self.__plugins[Plugins.Monitoring]

#endregion

#region Private Methods (env)

    def __env_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.Environment not in self.__plugins:
            config = self.__prepare_config("Environment", register.base_name)
            self.__plugins[Plugins.Environment] = Environment(config)
            self.__plugins[Plugins.Environment].init()

        elif register.value == verbal_const.NO and Plugins.Environment in self.__plugins:
            self.__plugins[Plugins.Environment].shutdown()
            del self.__plugins[Plugins.Environment]

#endregion

#region Private Methods (hvac)

    def __hvac_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.HVAC not in self.__plugins:
            config = self.__prepare_config("HVAC", register.base_name)
            self.__plugins[Plugins.HVAC] = HVAC(config)
            self.__plugins[Plugins.HVAC].init()

        elif register.value == verbal_const.NO and Plugins.HVAC in self.__plugins:
            self.__plugins[Plugins.HVAC].shutdown()
            del self.__plugins[Plugins.HVAC]

#endregion

#region Private Methods (lights)

    def __light_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.MainLight not in self.__plugins:
            config = self.__prepare_config("Lamps", register.base_name)
            self.__plugins[Plugins.MainLight] = Lighting(config)
            self.__plugins[Plugins.MainLight].init()

        elif register.value == verbal_const.NO and Plugins.MainLight in self.__plugins:
            self.__plugins[Plugins.MainLight].shutdown()
            del self.__plugins[Plugins.MainLight]

#endregion

#region Private Methods (sys)

    def __sys_enabled(self, register):

        # Check data type.
        if not register.is_str():
            GlobalErrorHandler.log_bad_register_data_type(self.__logger, register)
            return

        if register.value == verbal_const.YES and Plugins.Sys not in self.__plugins:
            config = self.__prepare_config("System", register.base_name)
            self.__plugins[Plugins.Sys] = Sys(config)
            self.__plugins[Plugins.Sys].init()

        elif register.value == verbal_const.NO and Plugins.Sys in self.__plugins:
            self.__plugins[Plugins.Sys].shutdown()
            del self.__plugins[Plugins.Sys]

        

#endregion

#region Public Methods

    def update(self):
        """Update plugins."""

        for key in self.__plugins:

            try:
                self.__plugins[key].update()

            except:
                pass

        # doc_generator.reg_to_json(self.__registers)
        # doc_generator.reg_to_md(self.__registers)

    def shutdown(self):
        """Shutdown plugins."""

        for key in self.__plugins:

            try:
                self.__plugins[key].shutdown()

            except:
                pass

#endregion
