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

from plugins.status_led import StatusLed
from plugins.tamper import Tamper
from plugins.flowmeter import Flowmeter
from plugins.power_meter import PowerMeter
from plugins.access_controll import AccessControll
from plugins.blinds import Blinds
from plugins.hvac import HVAC
from plugins.lighting import Lighting
from plugins.wdt_tablet import WDTTablet

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

    StatusLed = 1
    WindowClosed = 2
    DoorClosed = 3
    PIRDetector = 4
    AntiTampering = 5
    FireDetect = 6
    WaterCounter = 7
    PowerMeter = 8
    Blinds = 9
    AccessControll1 = 10
    AccessControll2 = 11
    HVAC = 22
    MainLight = 23
    WDTTablet = 24

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

#region General

        register = Register("general.is_empty")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 1
        self.__registers.add(register)

        register = Register("general.is_empty_timeout")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("general.drink_water_leak")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        register.value = 0
        self.__registers.add(register)

#endregion

#region Status Led

        register = Register("status_led.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "LED0"
        self.__registers.add(register)

        register = Register("status_led.blink_time")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("status_led.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__status_led_enabled
        register.value = 1
        self.__registers.add(register)

#endregion

#region Windows Closed

        register = Register("window_closed.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "!DI3"
        self.__registers.add(register)

        register = Register("window_closed.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__window_closed_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("window_closed.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Door Closed

        register = Register("door_closed.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI2"
        self.__registers.add(register)

        register = Register("door_closed.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__door_closed_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("door_closed.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region PIR Detector

        register = Register("pir_detector.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI7"
        self.__registers.add(register)

        register = Register("pir_detector.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__pir_detector_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("pir_detector.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Anti Tampering

        register = Register("anti_tampering.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = None
        self.__registers.add(register)

        register = Register("anti_tampering.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__anti_tampering_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("anti_tampering.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Fire Detect

        register = Register("fire_detect.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = None
        self.__registers.add(register)

        register = Register("fire_detect.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__fire_detect_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("fire_detect.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Water Counter

        register = Register("water_cnt.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("water_cnt.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI4"
        self.__registers.add(register)

        register = Register("water_cnt.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__water_cnt_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("water_cnt.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Blinds

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

        register = Register("blinds.input_active")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI8"
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
        register.value = 0
        self.__registers.add(register)

#endregion

#region Power Meter

        register = Register("self_current.sub_dev.uart")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("self_current.sub_dev.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "SDM120"
        self.__registers.add(register)

        register = Register("self_current.sub_dev.dev_id")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 2
        self.__registers.add(register)

        register = Register("self_current.sub_dev.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "Eastron"
        self.__registers.add(register)

        register = Register("self_current.sub_dev.current")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "Current"
        self.__registers.add(register)

        register = Register("self_current.sub_dev.total_energy")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "ExportActiveEnergy"
        self.__registers.add(register)

        register = Register("self_current.sub_dev.current_power")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "ApparentPower"
        self.__registers.add(register)

        register = Register("self_current.sub_dev.register_type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "inp"
        self.__registers.add(register)

        register = Register("self_current.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__power_meter_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("current_power.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("total_energy.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Mode Energy

        register = Register("mode.energy")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

#endregion

#region Mode Emergency

        register = Register("mode.emergency")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

#endregion

#region Meteo

        register = Register("outside.temp.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.temp.a6")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.temp.min24")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.temp.max24")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.rh")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.wind.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.wind.max12")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("outside.light")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

#endregion

#region Access Control 1

        register = Register("access_control_1.time_to_open")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("access_control_1.card_reader.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "act230"
        self.__registers.add(register)

        register = Register("access_control_1.exit_button.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI0"
        self.__registers.add(register)

        register = Register("access_control_1.card_reader.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM"
        self.__registers.add(register)

        register = Register("access_control_1.card_reader.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("access_control_1.exit_button.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("access_control_1.card_reader.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB0"
        if os.name == "nt":
            register.value = "COM4"
        self.__registers.add(register)

        register = Register("access_control_1.lock_mechanism.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DO0"
        self.__registers.add(register)

        register = Register("access_control_1.lock_mechanism.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("access_control_1.allowed_attendees")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = ["445E6046010080FF"]
        self.__registers.add(register)

        register = Register("access_control_1.card_reader.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("access_control_1.card_reader.serial_number")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "2897"
        self.__registers.add(register)

        register = Register("access_control_1.next_attendance")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("access_control_1.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__access_control_1_enabled
        register.value = 0
        self.__registers.add(register)

#endregion

#region Access Control 2

        register = Register("access_control_2.time_to_open")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("access_control_2.card_reader.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "act230"
        self.__registers.add(register)

        register = Register("access_control_2.exit_button.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI0"
        self.__registers.add(register)

        register = Register("access_control_2.card_reader.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TERACOM"
        self.__registers.add(register)

        register = Register("access_control_2.card_reader.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("access_control_2.exit_button.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("access_control_2.card_reader.port.name")
        register.scope = Scope.Global
        register.source = Source.bgERP
        if os.name == "posix":
            register.value = "/dev/ttyUSB1"
        if os.name == "nt":
            register.value = "COM5"
        self.__registers.add(register)

        register = Register("access_control_2.lock_mechanism.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DO0"
        self.__registers.add(register)

        register = Register("access_control_2.lock_mechanism.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("access_control_2.allowed_attendees")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = ["445E6046010080FF"]
        self.__registers.add(register)

        register = Register("access_control_2.card_reader.port.baudrate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 9600
        self.__registers.add(register)

        register = Register("access_control_2.card_reader.serial_number")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "2911"
        self.__registers.add(register)

        register = Register("access_control_2.next_attendance")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("access_control_2.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__access_control_2_enabled
        register.value = 0
        self.__registers.add(register)

#endregion

#region HVAC

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

        # Circulation
        register = Register("hvac.cirulation.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 25
        self.__registers.add(register)

        register = Register("hvac.cirulation.min")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("hvac.cirulation.max")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
        self.__registers.add(register)

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
        register.value = 0
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
        register.value = "DI5"
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

        # Loop 2 flowmeter
        register = Register("hvac.loop2.cnt.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.loop2.cnt.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI6"
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

        # Ventilation
        register = Register("hvac.ventilation.max")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
        self.__registers.add(register)

        register = Register("hvac.ventilation.min")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

#endregion

#region Lights

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

        register = Register("light.sensor.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "u1wtvs"
        self.__registers.add(register)

        register = Register("light.sensor.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "SEDtronic"
        self.__registers.add(register)

        register = Register("light.sensor.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "26607314020000F8"
        self.__registers.add(register)

        register = Register("light.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__light_enabled
        register.value = 0
        self.__registers.add(register)

#endregion

#region WDT Tablet

        register = Register("wdt_tablet.pulse_time")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("wdt_tablet.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DO2"
        self.__registers.add(register)

        register = Register("wdt_tablet.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__wdt_tablet_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("wdt_tablet.reset")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("wdt_tablet.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

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

    def __status_led_enabled(self, register):
        if register.value == 1:
            if Plugins.StatusLed not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Status LED", register.base_name)
                self.__plugins[Plugins.StatusLed] = StatusLed(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.StatusLed].init()

            # Add Handlers.

        elif register.value == 0:
            if Plugins.StatusLed in self.__plugins:
                self.__plugins[Plugins.StatusLed].shutdown()
                del self.__plugins[Plugins.StatusLed]

    def __window_closed_enabled(self, register):
        if register.value == 1:
            if Plugins.WindowClosed not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Windows Closed Sensor", register.base_name)
                self.__plugins[Plugins.WindowClosed] = Tamper(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.WindowClosed].init()

        elif register.value == 0:
            if Plugins.WindowClosed in self.__plugins:
                self.__plugins[Plugins.WindowClosed].shutdown()
                del self.__plugins[Plugins.WindowClosed]

    def __door_closed_enabled(self, register):
        if register.value == 1:
            if Plugins.DoorClosed not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Door Closed Sensor", register.base_name)
                self.__plugins[Plugins.DoorClosed] = Tamper(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.DoorClosed].init()

        elif register.value == 0:
            if Plugins.DoorClosed in self.__plugins:
                self.__plugins[Plugins.DoorClosed].shutdown()
                del self.__plugins[Plugins.DoorClosed]

    def __pir_detector_enabled(self, register):
        if register.value == 1:
            if Plugins.PIRDetector not in self.__plugins:

                # Create device.
                config = self.__prepare_config("PIR Detector", register.base_name)
                self.__plugins[Plugins.PIRDetector] = Tamper(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.PIRDetector].init()

        elif register.value == 0:
            if Plugins.PIRDetector in self.__plugins:
                self.__plugins[Plugins.PIRDetector].shutdown()
                del self.__plugins[Plugins.PIRDetector]

    def __anti_tampering_enabled(self, register):
        if register.value == 1:
            if Plugins.AntiTampering not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Anti Tampering", register.base_name)
                self.__plugins[Plugins.AntiTampering] = Tamper(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AntiTampering].init()

        elif register.value == 0:
            if Plugins.AntiTampering in self.__plugins:
                self.__plugins[Plugins.AntiTampering].shutdown()
                del self.__plugins[Plugins.AntiTampering]

    def __fire_detect_enabled(self, register):
        if register.value == 1:
            if Plugins.FireDetect not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Fire detect", register.base_name)
                self.__plugins[Plugins.FireDetect] = Tamper(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.FireDetect].init()

        elif register.value == 0:
            if Plugins.FireDetect in self.__plugins:
                self.__plugins[Plugins.FireDetect].shutdown()
                del self.__plugins[Plugins.FireDetect]

    def __water_cnt_enabled(self, register):
        if register.value == 1:
            if Plugins.WaterCounter not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Water Flow Metter", register.base_name)
                self.__plugins[Plugins.WaterCounter] = Flowmeter(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.WaterCounter].init()

        elif register.value == 0:
            if Plugins.WaterCounter in self.__plugins:
                self.__plugins[Plugins.WaterCounter].shutdown()
                del self.__plugins[Plugins.WaterCounter]

    def __blinds_enabled(self, register):
        if register.value == 1:
            if Plugins.Blinds not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Blinds", register.base_name)
                self.__plugins[Plugins.Blinds] = Blinds(config)
                self.__plugins[Plugins.Blinds].init()

        if register.value == 0:
            if Plugins.Blinds in self.__plugins:
                self.__plugins[Plugins.Blinds].shutdown()
                del self.__plugins[Plugins.Blinds]

    def __power_meter_enabled(self, register):
        if register.value == 1:
            if Plugins.PowerMeter not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Power Meter", register.base_name)
                self.__plugins[Plugins.PowerMeter] = PowerMeter(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.PowerMeter].init()

        if register.value == 0:
            if Plugins.PowerMeter in self.__plugins:
                self.__plugins[Plugins.PowerMeter].shutdown()
                del self.__plugins[Plugins.PowerMeter]

    def __access_control_1_enabled(self, register):
        if register.value == 1:
            if Plugins.AccessControll1 not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Access control 1", register.base_name)
                self.__plugins[Plugins.AccessControll1] = AccessControll(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AccessControll1].init()

        elif register.value == 0:
            if Plugins.AccessControll1 in self.__plugins:
                self.__plugins[Plugins.AccessControll1].shutdown()
                del self.__plugins[Plugins.AccessControll1]

    def __access_control_2_enabled(self, register):
        if register.value == 1:
            if Plugins.AccessControll2 not in self.__plugins:

                # Create device.
                config = self.__prepare_config("Access control 2", register.base_name)
                self.__plugins[Plugins.AccessControll2] = AccessControll(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AccessControll2].init()

        elif register.value == 0:
            if Plugins.AccessControll2 in self.__plugins:
                self.__plugins[Plugins.AccessControll2].shutdown()
                del self.__plugins[Plugins.AccessControll2]

    def __hvac_enabled(self, register):
        if register.value == 1:
            if Plugins.HVAC not in self.__plugins:

                # Create device.
                config = self.__prepare_config("HVAC", register.base_name)
                self.__plugins[Plugins.HVAC] = HVAC(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.HVAC].init()

        if register.value == 0:
            if Plugins.HVAC in self.__plugins:
                self.__plugins[Plugins.HVAC].shutdown()
                del self.__plugins[Plugins.HVAC]

    def __light_enabled(self, register):
        if register.value == 1:
            if Plugins.MainLight not in self.__plugins:
                key = register.base_name

                sensor_enabled = self.__registers.by_name(key + ".sensor.enabled").value
                sensor_dev = self.__registers.by_name(key + ".sensor.dev").value
                sensor_circuit = self.__registers.by_name(key + ".sensor.circuit").value
                sensor_vendor = self.__registers.by_name(key + ".sensor.vendor").value
                sensor_model = self.__registers.by_name(key + ".sensor.model").value
                v1_output = self.__registers.by_name(key + ".v1.output").value
                v2_output = self.__registers.by_name(key + ".v2.output").value

                config = {
                    "name": "Lamps",
                    "sensor_enabled": sensor_enabled,
                    "sensor_dev": sensor_dev,
                    "sensor_circuit": sensor_circuit,
                    "sensor_vendor": sensor_vendor,
                    "sensor_model": sensor_model,
                    "v1_output": v1_output,
                    "v2_output": v2_output,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.MainLight] = Lighting(config)
                self.__plugins[Plugins.MainLight].init()

        if register.value == 0:
            if Plugins.MainLight in self.__plugins:
                self.__plugins[Plugins.MainLight].shutdown()
                del self.__plugins[Plugins.MainLight]

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

#endregion

#region Public Methods

    def update(self):
        """Update plugins."""

        for key in self.__plugins:
            self.__plugins[key].update()

        # # JSON output
        # import json
        # bgerp_regs = self.__registers.by_source(Source.bgERP)
        # dict_regs = bgerp_regs.to_dict()
        # text = json.dumps(dict_regs, indent=4, sort_keys=True)
        # with open("bgerp_registers.json", "w") as f:
        #     f.write(text)

        # ztm_regs = self.__registers.by_source(Source.Zontromat)
        # dict_regs = ztm_regs.to_dict()
        # text = json.dumps(dict_regs, indent=4, sort_keys=True)
        # with open("ztm_registers.json", "w") as f:
        #     f.write(text)

        # # CSV output
        # bgerp_regs = self.__registers.by_source(Source.bgERP)
        # with open("bgerp_registers.csv", "w") as f:
        #     for register in bgerp_regs:
        #         print(register)
        #         f.write("{}\t{}\n".format(register.name, register.value))

        # ztm_regs = self.__registers.by_source(Source.Zontromat)
        # with open("ztm_registers.csv", "w") as f:
        #     for register in ztm_regs:
        #         f.write("{}\t{}\n".format(register.name, register.value))

    def shutdown(self):
        """Shutdown plugins."""

        for key in self.__plugins:
            self.__plugins[key].shutdown()

#endregion
