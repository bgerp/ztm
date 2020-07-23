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

# Room
from plugins.sys.sys import Sys
from plugins.tamper.tamper import Tamper
from plugins.access_control.access_control import AccessControl
from plugins.blinds.blinds import Blinds
from plugins.hvac.hvac import HVAC
from plugins.lighting.lighting import Lighting
from plugins.wdt_tablet.wdt_tablet import WDTTablet

# Test plugins
from plugins.environment.environment import Environment
from plugins.monitoring.monitoring import Monitoring

# Energy center
from plugins.ec.cold_circle.cold_circle import ColdCircle
from plugins.ec.hot_circle.hot_circle import HotCircle

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

    # (ac)
    AccessControl = 28

    # (monitoring)
    Monitoring = 2


    # (env)
    Environment = 10

    # (hvac)
    HVAC = 30

    # General
    Sys = 1

    # Room
    AntiTampering = 23
    FireDetect = 24
    Blinds = 27
    MainLight = 31
    WDTTablet = 32

    # Energy center
    HotCircle = 50
    ColdCircle = 51

class PluginsManager:
    """Template class doc."""

#region Attributes

    __logger = None
    """Logger"""

    __registers = None
    """Registers"""

    __controller = None
    """Controller"""

    __erp_service = None
    """ERP system service."""

    __plugins = None
    """Plugins"""

#endregion

#region Constructor

    def __init__(self, registers, controller, erp_service):
        """Constructor

        Parameters
        ----------
        registers : Registers
            Registers class instance.
        controller : mixed
            Hardware controller.
        erp_service : mixed
            ERP service class instance.
        """

        self.__logger = get_logger(__name__)
        self.__plugins = {}
        self.__registers = registers
        self.__controller = controller
        self.__erp_service = erp_service
        self.__add_registers()

#region Private Methods

    def __prepare_config(self, name, key):
        config = {
            "name": name,
            "key": key,
            "registers": self.__registers,
            "controller": self.__controller,
            "erp_service": self.__erp_service
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

        register = Register("ac.last30_attendees")
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
        register.value = verbal_const.NO # 1595322860
        self.__registers.add(register)

        # Entry card reader.
        register = Register("ac.entry_reader.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("ac.entry_reader.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM"
        self.__registers.add(register)

        register = Register("ac.entry_reader.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "act230"
        self.__registers.add(register)

        register = Register("ac.entry_reader.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.entry_reader.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM5"
        self.__registers.add(register)

        register = Register("ac.entry_reader.serial_number")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "2897"
        self.__registers.add(register)

        # Exit card reader.
        register = Register("ac.exit_reader.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("ac.exit_reader.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM"
        self.__registers.add(register)

        register = Register("ac.exit_reader.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "act230"
        self.__registers.add(register)

        register = Register("ac.exit_reader.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.exit_reader.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM11"
        self.__registers.add(register)

        register = Register("ac.exit_reader.serial_number")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "2911"
        self.__registers.add(register)

        # 
        register = Register("ac.exit_button.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.lock_mechanism.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DO2"
        self.__registers.add(register)

        register = Register("ac.time_to_open")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("ac.door_closed.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI2"
        self.__registers.add(register)

        register = Register("ac.door_closed.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)
        
        # Entry card reader 2.
        register = Register("ac.entry_reader2.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("ac.entry_reader2.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM"
        self.__registers.add(register)

        register = Register("ac.entry_reader2.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "act230"
        self.__registers.add(register)

        register = Register("ac.entry_reader2.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.entry_reader2.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM5"
        self.__registers.add(register)

        register = Register("ac.entry_reader2.serial_number")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "2897"
        self.__registers.add(register)

        # Exit card reader.
        register = Register("ac.exit_reader2.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("ac.exit_reader2.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM"
        self.__registers.add(register)

        register = Register("ac.exit_reader2.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "act230"
        self.__registers.add(register)

        register = Register("ac.exit_reader2.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("ac.exit_reader2.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM11"
        self.__registers.add(register)

        register = Register("ac.exit_reader2.serial_number")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "2911"
        self.__registers.add(register)

        # 
        register = Register("ac.exit_button2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.lock_mechanism2.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DO2"
        self.__registers.add(register)

        register = Register("ac.time_to_open2")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("ac.door_closed2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI2"
        self.__registers.add(register)

        register = Register("ac.door_closed2.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        #
        register = Register("ac.pir.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.pir.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("ac.pir2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "DI0"
        self.__registers.add(register)

        register = Register("ac.pir2.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        #
        register = Register("ac.window_closed.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "!DI3"
        self.__registers.add(register)

        register = Register("ac.window_closed.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("ac.window_closed2.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = verbal_const.OFF # "!DI3"
        self.__registers.add(register)

        register = Register("ac.window_closed2.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Anti Tampering (atamp)

        register = Register("at.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI1"
        self.__registers.add(register)

        register = Register("at.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__anti_tampering_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("at.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
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

        # colision detector.
        register = Register("monitoring.info_message")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        self.__registers.add(register)

        register = Register("monitoring.warning_message")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        self.__registers.add(register)

        register = Register("monitoring.error_message")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = ""
        self.__registers.add(register)

        register = Register("monitoring.clear_errors")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

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
        register = Register("monitoring.pa.uart")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("monitoring.pa.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "SDM630"
        self.__registers.add(register)

        register = Register("monitoring.pa.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "Eastron"
        self.__registers.add(register)

        register = Register("monitoring.pa.dev_id")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 2
        self.__registers.add(register)

        register = Register("monitoring.pa.l1")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("monitoring.pa.l2")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

        register = Register("monitoring.pa.l3")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
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
        register = Register("hvac.air_temp_cent.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hvac.air_temp_cent.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("hvac.air_temp_cent.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFFCD0001703AE"
        self.__registers.add(register)

        register = Register("hvac.air_temp_cent.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Air temp lower
        register = Register("hvac.air_temp_lower.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hvac.air_temp_lower.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("hvac.air_temp_lower.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFC4EE00170349"
        self.__registers.add(register)

        register = Register("hvac.air_temp_lower.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Air temp upper.
        register = Register("hvac.air_temp_upper.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hvac.air_temp_upper.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("hvac.air_temp_upper.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FF2B70C11604B7"
        self.__registers.add(register)

        register = Register("hvac.air_temp_upper.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # # Circulation
        # register = Register("hvac.circulation.actual")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = 25
        # self.__registers.add(register)

        # register = Register("hvac.circulation.min")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = 0
        # self.__registers.add(register)

        # register = Register("hvac.circulation.max")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = 100
        # self.__registers.add(register)

        # Convector
        register = Register("hvac.convector.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # register = Register("hvac.convector.model")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "klimafan"
        # self.__registers.add(register)

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

        register = Register("hvac.convector.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "silpa"
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

        register = Register("hvac.loop1.cnt.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Loop 1 fan
        register = Register("hvac.loop1.fan.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # register = Register("hvac.loop1.fan.model")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "f3p146ec072600"
        # self.__registers.add(register)

        register = Register("hvac.loop1.fan.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO3"
        self.__registers.add(register)

        register = Register("hvac.loop1.fan.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "HangzhouAirflowElectricApplications"
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
        register = Register("hvac.loop1.temp.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hvac.loop1.temp.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("hvac.loop1.temp.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FF2B70C11604B7"
        self.__registers.add(register)

        register = Register("hvac.loop1.temp.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Loop 1 valve.
        register = Register("hvac.loop1.valve.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # register = Register("hvac.loop1.valve.model")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "a20m15b2c"
        # self.__registers.add(register)

        register = Register("hvac.loop1.valve.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO4"
        self.__registers.add(register)

        register = Register("hvac.loop1.valve.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TONHE"
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

        register = Register("hvac.loop2.cnt.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Loop 2 fan
        register = Register("hvac.loop2.fan.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # register = Register("hvac.loop2.fan.model")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "f3p146ec072600"
        # self.__registers.add(register)

        register = Register("hvac.loop2.fan.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO4"
        self.__registers.add(register)

        register = Register("hvac.loop2.fan.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "HangzhouAirflowElectricApplications"
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
        register = Register("hvac.loop2.temp.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hvac.loop2.temp.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("hvac.loop2.temp.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFC4EE00170349"
        self.__registers.add(register)

        register = Register("hvac.loop2.temp.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # Loop 2 valve.
        register = Register("hvac.loop2.valve.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        # register = Register("hvac.loop2.valve.model")
        # register.scope = Scope.Global
        # register.source = Source.bgERP
        # register.value = "a20m15b2c"
        # self.__registers.add(register)

        register = Register("hvac.loop2.valve.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO3"
        self.__registers.add(register)

        register = Register("hvac.loop2.valve.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TONHE"
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

        register = Register("light.sensor.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("light.sensor.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "1wdevice"
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

        register = Register("light.sensor.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "26607314020000F8"
        self.__registers.add(register)

        register = Register("light.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__light_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#region System (sys)

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

        register = Register("sys.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__sys_enabled
        # Run the plugin before others.
        register.value = verbal_const.YES
        self.__registers.add(register)

#endregion


#region WDT Tablet

        register = Register("wt.pulse_time")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("wt.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DO3"
        self.__registers.add(register)

        register = Register("wt.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__wdt_tablet_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

        register = Register("wt.reset")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("wt.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Hot Circle

        register = Register("hc.tank_temp.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FF2B70C11604B7"
        self.__registers.add(register)

        register = Register("hc.tank_temp.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hc.tank_temp.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("hc.tank_temp.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hc.goal_temp")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 20
        self.__registers.add(register)

        register = Register("hc.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__hot_circle_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#region Cold Circle

        register = Register("cc.tank_temp.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFFCD0001703AE"
        self.__registers.add(register)

        register = Register("cc.tank_temp.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("cc.tank_temp.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("cc.tank_temp.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("cc.goal_temp")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 8
        self.__registers.add(register)

        register = Register("cc.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__cold_circle_enabled
        register.value = verbal_const.NO
        self.__registers.add(register)

#endregion

#endregion

#region Private Methods (ac)

    def __access_control_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.AccessControl not in self.__plugins:
            config = self.__prepare_config("Access control", register.base_name)
            self.__plugins[Plugins.AccessControl] = AccessControl(config)
            self.__plugins[Plugins.AccessControl].init()

        elif register.value == verbal_const.NO and Plugins.AccessControl in self.__plugins:
            self.__plugins[Plugins.AccessControl].shutdown()
            del self.__plugins[Plugins.AccessControl]

#endregion

#region Anti tampering (atamp)

    def __anti_tampering_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.AntiTampering not in self.__plugins:
            config = self.__prepare_config("Anti Tampering", register.base_name)
            self.__plugins[Plugins.AntiTampering] = Tamper(config)
            self.__plugins[Plugins.AntiTampering].init()

        elif register.value == verbal_const.NO and Plugins.AntiTampering in self.__plugins:
            self.__plugins[Plugins.AntiTampering].shutdown()
            del self.__plugins[Plugins.AntiTampering]

#endregion

#region Private Methods (blinds)

    def __blinds_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.Blinds not in self.__plugins:
            config = self.__prepare_config("Blinds", register.base_name)
            self.__plugins[Plugins.Blinds] = Blinds(config)
            self.__plugins[Plugins.Blinds].init()

        if register.value == verbal_const.NO and Plugins.Blinds in self.__plugins:
            self.__plugins[Plugins.Blinds].shutdown()
            del self.__plugins[Plugins.Blinds]

#endregion

#region Private Methods (mon)

    def __monitoring_enabled(self, register):
        # Create monitoring.

        if register.value == verbal_const.YES and Plugins.Monitoring not in self.__plugins:
            config = self.__prepare_config("Monitoring", register.base_name)
            self.__plugins[Plugins.Monitoring] = Monitoring(config)
            self.__plugins[Plugins.Monitoring].init()

        if register.value == verbal_const.NO and Plugins.Monitoring in self.__plugins:
            self.__plugins[Plugins.Monitoring].shutdown()
            del self.__plugins[Plugins.Monitoring]

#endregion

#region Private Methods (env)

    def __env_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.Environment not in self.__plugins:
            config = self.__prepare_config("Environment", register.base_name)
            self.__plugins[Plugins.Environment] = Environment(config)
            self.__plugins[Plugins.Environment].init()

        if register.value == verbal_const.NO and Plugins.Environment in self.__plugins:
            self.__plugins[Plugins.Environment].shutdown()
            del self.__plugins[Plugins.Environment]

#endregion

#region Private Methods (hvac)

    def __hvac_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.HVAC not in self.__plugins:
            config = self.__prepare_config("HVAC", register.base_name)
            self.__plugins[Plugins.HVAC] = HVAC(config)
            self.__plugins[Plugins.HVAC].init()

        if register.value == verbal_const.NO and Plugins.HVAC in self.__plugins:
            self.__plugins[Plugins.HVAC].shutdown()
            del self.__plugins[Plugins.HVAC]

#endregion

#region Private Methods (lights)

    def __light_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.MainLight not in self.__plugins:
            config = self.__prepare_config("Lamps", register.base_name)
            self.__plugins[Plugins.MainLight] = Lighting(config)
            self.__plugins[Plugins.MainLight].init()

        if register.value == verbal_const.NO and Plugins.MainLight in self.__plugins:
            self.__plugins[Plugins.MainLight].shutdown()
            del self.__plugins[Plugins.MainLight]

#endregion

#region Private Methods (sys)

    def __sys_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.Sys not in self.__plugins:
            config = self.__prepare_config("System", register.base_name)
            self.__plugins[Plugins.Sys] = Sys(config)
            self.__plugins[Plugins.Sys].init()

        elif register.value == verbal_const.NO and Plugins.Sys in self.__plugins:
            self.__plugins[Plugins.Sys].shutdown()
            del self.__plugins[Plugins.Sys]

#endregion


    def __wdt_tablet_enabled(self, register):
        if register.value == 1:
            if Plugins.WDTTablet not in self.__plugins:
                key = register.base_name

                pulse_time = self.__registers.by_name(key + ".pulse_time").value
                output = self.__registers.by_name(key + ".output").value

                config = {
                    "name": "WDT Tablet",
                    "pulse_time": pulse_time,
                    "output": output,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.WDTTablet] = WDTTablet(config)
                self.__plugins[Plugins.WDTTablet].init()

        if register.value == 0:
            if Plugins.WDTTablet in self.__plugins:
                self.__plugins[Plugins.WDTTablet].shutdown()
                del self.__plugins[Plugins.WDTTablet]

    def __hot_circle_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.HotCircle not in self.__plugins:
            config = self.__prepare_config("HotCircle", register.base_name)
            self.__plugins[Plugins.HotCircle] = HotCircle(config)
            self.__plugins[Plugins.HotCircle].init()

        if register.value == verbal_const.NO and Plugins.HotCircle in self.__plugins:
            self.__plugins[Plugins.HotCircle].shutdown()
            del self.__plugins[Plugins.HotCircle]

    def __cold_circle_enabled(self, register):
        if register.value == verbal_const.YES and Plugins.ColdCircle not in self.__plugins:
            config = self.__prepare_config("ColdCircle", register.base_name)
            self.__plugins[Plugins.ColdCircle] = ColdCircle(config)
            self.__plugins[Plugins.ColdCircle].init()

        if register.value == verbal_const.NO and Plugins.ColdCircle in self.__plugins:
            self.__plugins[Plugins.ColdCircle].shutdown()
            del self.__plugins[Plugins.ColdCircle]


#region Public Methods

    def update(self):
        """Update plugins."""

        for key in self.__plugins:
            self.__plugins[key].update()

        # doc_generator.reg_to_json(self.__registers)
        # doc_generator.reg_to_md(self.__registers)

    def shutdown(self):
        """Shutdown plugins."""

        for key in self.__plugins:
            self.__plugins[key].shutdown()

#endregion
