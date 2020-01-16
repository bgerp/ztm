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

import time
import os

from enum import Enum

from utils.logger import get_logger

from register import Scope
from register import Source
from register import Register

from plugins.status_led import StatusLed
from plugins.tamper import Tamper
from plugins.flowmeter import Flowmeter
from plugins.thermometer import Thermometer
from plugins.light_sensor import LightSensor
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
    Loop1Counter = 8
    Loop2Counter = 9
    AirTempUpper = 10
    AirTempLower = 11
    AirTempCentral = 12
    RoomLight = 13
    Loop1Temperature = 14
    Loop2Temperature = 15
    PowerMeter = 16
    Blinds = 17
    AccessControll1 = 18
    AccessControll2 = 19
    HVAC = 20
    MainLight = 21
    WDTTablet = 22

class PluginsManager:
    """Template class doc."""

#region Attributes

    __logger = None
    """Logger"""

    __registers = None
    """Registers"""

    __instance = None
    """Instance of the singelton."""

    __controller_model = None
    """Controller model."""

    __gpio_map = None
    """GPIO map."""

#endregion

#region Constructor

    def __init__(self, registers, controller, erp_service):
        """Constructor

        Parameters
        ----------
        self : Template
            Current class instance.
        """

        self.__logger = get_logger(__name__)
        self.__plugins = {}
        self.__registers = registers
        self.__controller = controller
        self.__erp_service = erp_service

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

#region Loop 1 Counter

        register = Register("loop1_cnt.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("loop1_cnt.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI5"
        self.__registers.add(register)

        register = Register("loop1_cnt.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__loop1_cnt_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("loop1_cnt.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Loop 2 Counter

        register = Register("loop2_cnt.tpl")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 10
        self.__registers.add(register)

        register = Register("loop2_cnt.input")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DI6"
        self.__registers.add(register)

        register = Register("loop2_cnt.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__loop2_cnt_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("loop2_cnt.state")
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

        register = Register("blinds.sub_dev.uart")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("blinds.sub_dev.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "M1"
        self.__registers.add(register)

        register = Register("blinds.sun.elevation")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("blinds.sub_dev.dev_id")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 3
        self.__registers.add(register)

        register = Register("blinds.sub_dev.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "PT"
        self.__registers.add(register)

        register = Register("blinds.sun.azimuth.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "deg"
        self.__registers.add(register)

        register = Register("blinds.sun.elevation.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "deg"
        self.__registers.add(register)

        register = Register("blinds.sub_dev.register_type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "inp"
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

#region Upper termometer

        register = Register("air_temp_upper.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("air_temp_upper.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "degc"
        self.__registers.add(register)

        register = Register("air_temp_upper.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("air_temp_upper.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FF2B70C11604B7"
        self.__registers.add(register)

        register = Register("air_temp_upper.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__air_temp_upper_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("air_temp_upper.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Lower termometer

        register = Register("air_temp_lower.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("air_temp_lower.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "degc"
        self.__registers.add(register)

        register = Register("air_temp_lower.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("air_temp_lower.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFC4EE00170349"
        self.__registers.add(register)

        register = Register("air_temp_lower.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__air_temp_lower_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("air_temp_lower.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Center termometer

        register = Register("air_temp_cent.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("air_temp_cent.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "degc"
        self.__registers.add(register)

        register = Register("air_temp_cent.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("air_temp_cent.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFFCD0001703AE"
        self.__registers.add(register)

        register = Register("air_temp_cent.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__air_temp_cent_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("air_temp_cent.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Loop 1 Temperature

        register = Register("loop_1_temp.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("loop_1_temp.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "degc"
        self.__registers.add(register)

        register = Register("loop_1_temp.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("loop_1_temp.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FF2B70C11604B7"
        self.__registers.add(register)

        register = Register("loop_1_temp.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__loop_1_temp_enablede
        register.value = 0
        self.__registers.add(register)

        register = Register("loop_1_temp.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Loop 2 Temperature

        register = Register("loop_2_temp.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("loop_2_temp.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "degc"
        self.__registers.add(register)

        register = Register("loop_2_temp.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
        self.__registers.add(register)

        register = Register("loop_2_temp.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFC4EE00170349"
        self.__registers.add(register)

        register = Register("loop_2_temp.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__loop_2_temp_enablede
        register.value = 0
        self.__registers.add(register)

        register = Register("loop_2_temp.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

#endregion

#region Light sensor

        register = Register("room_light.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "1wdevice"
        self.__registers.add(register)

        register = Register("room_light.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "lux"
        self.__registers.add(register)

        register = Register("room_light.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "light"
        self.__registers.add(register)

        register = Register("room_light.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "26607314020000F8"
        self.__registers.add(register)

        register = Register("room_light.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__room_light_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("room_light.state")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)


#endregion

#region Mode Energy

        register = Register("mode.energy")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__mode_energy
        register.value = 0
        self.__registers.add(register)

#endregion

#region Mode Emergency

        register = Register("mode.emergency")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__mode_emergency
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

        register = Register("sun.elevation.value")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("sun.elevation.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("sun.azimuth.value")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("sun.azimuth.mou")
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
        register.update_handler = self.__access_control_allowed_attenders_1
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

        register = Register("access_control_1.is_empty")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("access_control_1.is_empty_timeout")
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
        register.update_handler = self.__access_control_allowed_attenders_2
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

        register = Register("access_control_2.is_empty")
        register.scope = Scope.Global
        register.source = Source.Zontromat
        self.__registers.add(register)

        register = Register("access_control_2.is_empty_timeout")
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

        register = Register("hvac.delta_time")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 5
        self.__registers.add(register)

        register = Register("hvac.adjust_temp")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__hvac_adjust_temp
        register.value = 0
        self.__registers.add(register)

        register = Register("hvac.goal_building_temp")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__hvac_goal_building_temp
        register.value = 20
        self.__registers.add(register)

        register = Register("hvac.update_rate")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 3
        self.__registers.add(register)

        register = Register("hvac.thermal_mode")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 2
        self.__registers.add(register)

        register = Register("hvac.convector.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "klimafan"
        self.__registers.add(register)

        register = Register("hvac.lower_fan.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "f3p146ec072600"
        self.__registers.add(register)

        register = Register("hvac.upper_fan.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "f3p146ec072600"
        self.__registers.add(register)

        register = Register("hvac.convector.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "silpa"
        self.__registers.add(register)

        register = Register("hvac.lower_fan.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO3"
        self.__registers.add(register)

        register = Register("hvac.lower_fan.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "HangzhouAirflowElectricApplications"
        self.__registers.add(register)

        register = Register("hvac.upper_fan.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "AO4"
        self.__registers.add(register)

        register = Register("hvac.upper_fan.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "HangzhouAirflowElectricApplications"
        self.__registers.add(register)

        register = Register("hvac.convector.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.lower_fan.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.lower_valve.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "a20m15b2c"
        self.__registers.add(register)

        register = Register("hvac.upper_fan.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.upper_valve.model")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "a20m15b2c"
        self.__registers.add(register)

        register = Register("hvac.lower_valve.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO4"
        self.__registers.add(register)

        register = Register("hvac.lower_valve.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TONHE"
        self.__registers.add(register)

        register = Register("hvac.upper_valve.output")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "RO3"
        self.__registers.add(register)

        register = Register("hvac.upper_valve.vendor")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "TONHE"
        self.__registers.add(register)

        register = Register("hvac.lower_valve.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.thermal_force_limit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
        self.__registers.add(register)

        register = Register("hvac.upper_valve.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.room_theromometer.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "temp"
        self.__registers.add(register)

        register = Register("hvac.room_theromometer.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "degc"
        self.__registers.add(register)

        register = Register("hvac.room_theromometer.type")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "DS18B20"
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

        register = Register("hvac.room_theromometer.circuit")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "28FFC4EE00170349"
        self.__registers.add(register)
        
        register = Register("hvac.room_theromometer.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 1
        self.__registers.add(register)

        register = Register("hvac.enabled")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.update_handler = self.__hvac_enabled
        register.value = 0
        self.__registers.add(register)

        register = Register("hvac.temp.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

        register = Register("hvac.circ.actual")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 25
        self.__registers.add(register)

        register = Register("hvac.ventilation.min")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 0
        self.__registers.add(register)

        register = Register("hvac.ventilation.max")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 100
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

        register = Register("hvac.temp.min")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 20
        self.__registers.add(register)

        register = Register("hvac.temp.max")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = 30
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

        register = Register("light.sensor.dev")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "1wdevice"
        self.__registers.add(register)

        register = Register("light.sensor.mou")
        register.scope = Scope.Global
        register.source = Source.bgERP
        register.value = "lux"
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
        register.update_handler = self.__wdt_tablet_reset
        register.value = 0
        self.__registers.add(register)

        register = Register("wdt_tablet.state")
        register.scope = Scope.Global
        register.source = Source.bgERP
        self.__registers.add(register)

#endregion

#region Private Methods

    def __status_led_enabled(self, register):
        if register.value == 1:
            if Plugins.StatusLed not in self.__plugins:
                key = register.base_name
                blink_time = self.__registers.by_name(key + ".blink_time").value
                output = self.__registers.by_name(key + ".output").value

                config = {
                    "name": "Status LED",
                    "blink_time": blink_time,
                    "output": output,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.StatusLed] = StatusLed(config)
                self.__plugins[Plugins.StatusLed].init()

            # Add Handlers.

        elif register.value == 0:
            if Plugins.StatusLed in self.__plugins:
                self.__plugins[Plugins.StatusLed].shutdown()
                del self.__plugins[Plugins.StatusLed]

    def __window_closed_enabled(self, register):
        if register.value == 1:
            if Plugins.WindowClosed not in self.__plugins:
                key = register.base_name
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Windows Closed Sensor",
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.WindowClosed] = Tamper(config)
                self.__plugins[Plugins.WindowClosed].init()

        elif register.value == 0:
            if Plugins.WindowClosed in self.__plugins:
                self.__plugins[Plugins.WindowClosed].shutdown()
                del self.__plugins[Plugins.WindowClosed]

    def __door_closed_enabled(self, register):
        if register.value == 1:
            if Plugins.DoorClosed not in self.__plugins:
                key = register.base_name
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Door Closed Sensor",
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.DoorClosed] = Tamper(config)
                self.__plugins[Plugins.DoorClosed].init()

        elif register.value == 0:
            if Plugins.DoorClosed in self.__plugins:
                self.__plugins[Plugins.DoorClosed].shutdown()
                del self.__plugins[Plugins.DoorClosed]

    def __pir_detector_enabled(self, register):
        if register.value == 1:
            if Plugins.PIRDetector not in self.__plugins:
                key = register.base_name
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "PIR Detector",
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.PIRDetector] = Tamper(config)
                self.__plugins[Plugins.PIRDetector].init()

        elif register.value == 0:
            if Plugins.PIRDetector in self.__plugins:
                self.__plugins[Plugins.PIRDetector].shutdown()
                del self.__plugins[Plugins.PIRDetector]

    def __anti_tampering_enabled(self, register):
        if register.value == 1:
            if Plugins.AntiTampering not in self.__plugins:
                key = register.base_name
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Anti Tampering",
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.AntiTampering] = Tamper(config)
                self.__plugins[Plugins.AntiTampering].init()

        elif register.value == 0:
            if Plugins.AntiTampering in self.__plugins:
                self.__plugins[Plugins.AntiTampering].shutdown()
                del self.__plugins[Plugins.AntiTampering]

    def __fire_detect_enabled(self, register):
        if register.value == 1:
            if Plugins.FireDetect not in self.__plugins:
                key = register.base_name
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Fire detect",
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.FireDetect] = Tamper(config)
                self.__plugins[Plugins.FireDetect].init()

                # Add Handlers.

        elif register.value == 0:
            if Plugins.FireDetect in self.__plugins:
                self.__plugins[Plugins.FireDetect].shutdown()
                del self.__plugins[Plugins.FireDetect]

    def __water_cnt_enabled(self, register):
        if register.value == 1:
            if Plugins.WaterCounter not in self.__plugins:
                key = register.base_name
                tpl = self.__registers.by_name(key + ".tpl").value
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Water Flow Metter",
                    "tpl": tpl,
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.WaterCounter] = Flowmeter(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.WaterCounter].init()

        elif register.value == 0:
            if Plugins.WaterCounter in self.__plugins:
                self.__plugins[Plugins.WaterCounter].shutdown()
                del self.__plugins[Plugins.WaterCounter]

    def __loop1_cnt_enabled(self, register):
        if register.value == 1:
            if Plugins.Loop1Counter not in self.__plugins:
                key = register.base_name
                tpl = self.__registers.by_name(key + ".tpl").value
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Loop 1 Flow Metter",
                    "tpl": tpl,
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.Loop1Counter] = Flowmeter(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.Loop1Counter].init()

        elif register.value == 0:
            if Plugins.Loop1Counter in self.__plugins:
                self.__plugins[Plugins.Loop1Counter].shutdown()
                del self.__plugins[Plugins.Loop1Counter]

    def __loop2_cnt_enabled(self, register):
        if register.value == 1:
            if Plugins.Loop2Counter not in self.__plugins:
                key = register.base_name
                tpl = self.__registers.by_name(key + ".tpl").value
                input_pin = self.__registers.by_name(key + ".input").value

                config = {
                    "name": "Loop 2 Flow Metter",
                    "tpl": tpl,
                    "input": input_pin,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.Loop2Counter] = Flowmeter(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.Loop2Counter].init()

        elif register.value == 0:
            if Plugins.Loop2Counter in self.__plugins:
                self.__plugins[Plugins.Loop2Counter].shutdown()
                del self.__plugins[Plugins.Loop2Counter]

    def __blinds_enabled(self, register):
        if register.value == 1:
            if Plugins.Blinds not in self.__plugins:
                key = register.base_name
                vendor = self.__registers.by_name(key + ".sub_dev.vendor").value
                model = self.__registers.by_name(key + ".sub_dev.model").value
                uart = self.__registers.by_name(key + ".sub_dev.uart").value
                dev_id = self.__registers.by_name(key + ".sub_dev.dev_id").value
                register_type = self.__registers.by_name(key + ".sub_dev.register_type").value
                elevation_value = self.__registers.by_name(key + ".sun.elevation.value").value
                elevation_mou = self.__registers.by_name(key + ".sun.elevation.mou").value
                azimuth_value = self.__registers.by_name(key + ".sun.azimuth.value").value
                azimuth_mou = self.__registers.by_name(key + ".sun.azimuth.mou").value

                config = {
                    "name": "Blinds",
                    "vendor": vendor,
                    "model": model,
                    "uart": uart,
                    "dev_id": dev_id,
                    "register_type": register_type,
                    "elevation_value": elevation_value,
                    "elevation_mou": elevation_mou,
                    "azimuth_value": azimuth_value,
                    "azimuth_mou": azimuth_mou,
                }

                # Create device.
                self.__plugins[Plugins.Blinds] = Blinds(config)
                self.__plugins[Plugins.Blinds].init()

        if register.value == 1:
            if Plugins.Blinds in self.__plugins:
                self.__plugins[Plugins.Blinds].shutdown()
                del self.__plugins[Plugins.Blinds]

    def __power_meter_enabled(self, register):
        if register.value == 1:
            if Plugins.PowerMeter not in self.__plugins:
                key = register.base_name
                vendor = self.__registers.by_name(key + ".sub_dev.vendor").value
                model = self.__registers.by_name(key + ".sub_dev.model").value
                uart = self.__registers.by_name(key + ".sub_dev.uart").value
                dev_id = self.__registers.by_name(key + ".sub_dev.dev_id").value
                register_type = self.__registers.by_name(key + ".sub_dev.register_type").value
                total_energy = self.__registers.by_name(key + ".sub_dev.total_energy").value
                current_power = self.__registers.by_name(key + ".sub_dev.current_power").value
                current = self.__registers.by_name(key + ".sub_dev.current").value

                config = {
                    "name": "Self current",
                    "vendor": vendor,
                    "model": model,
                    "uart": uart,
                    "dev_id": dev_id,
                    "register_type": register_type,
                    "total_energy": total_energy,
                    "current_power": current_power,
                    "current": current,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.PowerMeter] = PowerMeter(config)
                self.__plugins[Plugins.PowerMeter].init()

        if register.value == 0:
            if Plugins.PowerMeter in self.__plugins:
                self.__plugins[Plugins.PowerMeter].shutdown()
                del self.__plugins[Plugins.PowerMeter]

    def __air_temp_upper_enabled(self, register):
        if register.value == 1:
            if Plugins.AirTempUpper not in self.__plugins:
                key = register.base_name
                mou = self.__registers.by_name(key + ".mou").value
                dev = self.__registers.by_name(key + ".dev").value
                dev_type = self.__registers.by_name(key + ".dev").value
                circuit = self.__registers.by_name(key + ".circuit").value

                config = {
                    "name": "Air Temperature Upper",
                    "mou": mou,
                    "dev": dev,
                    "type": dev_type,
                    "circuit": circuit,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.AirTempUpper] = Thermometer(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AirTempUpper].init()

        elif register.value == 0:
            if Plugins.AirTempUpper in self.__plugins:
                self.__plugins[Plugins.AirTempUpper].shutdown()
                del self.__plugins[Plugins.AirTempUpper]

    def __air_temp_lower_enabled(self, register):
        if register.value == 1:
            if Plugins.AirTempLower not in self.__plugins:
                key = register.base_name
                mou = self.__registers.by_name(key + ".mou").value
                dev = self.__registers.by_name(key + ".dev").value
                dev_type = self.__registers.by_name(key + ".dev").value
                circuit = self.__registers.by_name(key + ".circuit").value

                config = {
                    "name": "Air Temperature Lower",
                    "mou": mou,
                    "dev": dev,
                    "type": dev_type,
                    "circuit": circuit,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.AirTempLower] = Thermometer(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AirTempLower].init()

        elif register.value == 0:
            if Plugins.AirTempLower in self.__plugins:
                self.__plugins[Plugins.AirTempLower].shutdown()
                del self.__plugins[Plugins.AirTempLower]

    def __air_temp_cent_enabled(self, register):
        if register.value == 1:
            if Plugins.AirTempCentral not in self.__plugins:
                key = register.base_name
                mou = self.__registers.by_name(key + ".mou").value
                dev = self.__registers.by_name(key + ".dev").value
                dev_type = self.__registers.by_name(key + ".dev").value
                circuit = self.__registers.by_name(key + ".circuit").value

                config = {
                    "name": "Air Temperature Central",
                    "mou": mou,
                    "dev": dev,
                    "type": dev_type,
                    "circuit": circuit,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.AirTempCentral] = Thermometer(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AirTempCentral].init()

        elif register.value == 0:
            if Plugins.AirTempCentral in self.__plugins:
                self.__plugins[Plugins.AirTempCentral].shutdown()
                del self.__plugins[Plugins.AirTempCentral]

    def __loop_1_temp_enablede(self, register):
        if register.value == 1:
            if Plugins.Loop1Temperature not in self.__plugins:
                key = register.base_name
                mou = self.__registers.by_name(key + ".mou").value
                dev = self.__registers.by_name(key + ".dev").value
                dev_type = self.__registers.by_name(key + ".type").value
                circuit = self.__registers.by_name(key + ".circuit").value

                config = {
                    "name": "Loop 1 Temperature",
                    "mou": mou,
                    "dev": dev,
                    "type": dev_type,
                    "circuit": circuit,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.Loop1Temperature] = Thermometer(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.Loop1Temperature].init()

        elif register.value == 0:
            if Plugins.Loop1Temperature in self.__plugins:
                self.__plugins[Plugins.Loop1Temperature].shutdown()
                del self.__plugins[Plugins.Loop1Temperature]

    def __loop_2_temp_enablede(self, register):
        if register.value == 1:
            if Plugins.Loop2Temperature not in self.__plugins:
                key = register.base_name
                mou = self.__registers.by_name(key + ".mou").value
                dev = self.__registers.by_name(key + ".dev").value
                dev_type = self.__registers.by_name(key + ".type").value
                circuit = self.__registers.by_name(key + ".circuit").value

                config = {
                    "name": "Loop 2 Temperature",
                    "mou": mou,
                    "dev": dev,
                    "type": dev_type,
                    "circuit": circuit,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.Loop2Temperature] = Thermometer(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.Loop2Temperature].init()

        elif register.value == 0:
            if Plugins.Loop2Temperature in self.__plugins:
                self.__plugins[Plugins.Loop2Temperature].shutdown()
                del self.__plugins[Plugins.Loop2Temperature]

    def __room_light_enabled(self, register):
        if register.value == 1:
            if Plugins.RoomLight not in self.__plugins:
                key = register.base_name
                mou = self.__registers.by_name(key + ".mou").value
                dev = self.__registers.by_name(key + ".dev").value
                circuit = self.__registers.by_name(key + ".circuit").value

                config = {
                    "name": "Room Light Sensor",
                    "mou": mou,
                    "dev": dev,
                    "circuit": circuit,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.RoomLight] = LightSensor(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.RoomLight].init()

        elif register.value == 0:
            if Plugins.RoomLight in self.__plugins:
                self.__plugins[Plugins.RoomLight].shutdown()
                del self.__plugins[Plugins.RoomLight]

    def __mode_energy(self, register):
        pass
        #self.__logger.info("Energy mode: {} {}".format(register.name, register.value))

    def __mode_emergency(self, register):
        pass
        #self.__logger.info("Emergency mode: {} {}".format(register.name, register.value))

    def __access_control_1_enabled(self, register):
        if register.value == 1:
            if Plugins.AccessControll1 not in self.__plugins:
                key = register.base_name
                time_to_open = self.__registers.by_name(key + ".time_to_open").value

                exit_button_enabled = self.__registers.by_name(key + ".exit_button.enabled").value
                exit_button_input = self.__registers.by_name(key + ".exit_button.input").value

                lock_mechanism_enabled = self.__registers.by_name(key + ".lock_mechanism.enabled").value
                lock_mechanism_output = self.__registers.by_name(key + ".lock_mechanism.output").value

                card_reader_enabled = self.__registers.by_name(key + ".card_reader.enabled").value
                card_reader_vendor = self.__registers.by_name(key + ".card_reader.vendor").value
                card_reader_model = self.__registers.by_name(key + ".card_reader.model").value
                card_reader_serial_number = self.__registers.by_name(key + ".card_reader.serial_number").value
                card_reader_port_name = self.__registers.by_name(key + ".card_reader.port.name").value
                card_reader_port_baudrate = self.__registers.by_name(key + ".card_reader.port.baudrate").value
                card_reader_allowed_ids = self.__registers.by_name(key + ".allowed_attendees").value

                config = {
                    "name": "Access control 1",
                    "time_to_open":time_to_open,

                    "exit_button_enabled": exit_button_enabled,
                    "exit_button_input": exit_button_input,

                    "lock_mechanism_enabled": lock_mechanism_enabled,
                    "lock_mechanism_output": lock_mechanism_output,

                    "card_reader_enabled": card_reader_enabled,
                    "card_reader_vendor": card_reader_vendor,
                    "card_reader_model": card_reader_model,
                    "card_reader_serial_number": card_reader_serial_number,
                    "card_reader_port_name": card_reader_port_name,
                    "card_reader_port_baudrate": card_reader_port_baudrate,
                    "card_reader_allowed_ids": card_reader_allowed_ids,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.AccessControll1] = AccessControll(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AccessControll1].init()

        elif register.value == 0:
            if Plugins.AccessControll1 in self.__plugins:
                self.__plugins[Plugins.AccessControll1].shutdown()
                del self.__plugins[Plugins.AccessControll1]

    def __access_control_allowed_attenders_1(self, register):
        if Plugins.AccessControll1 not in self.__plugins:
            return

        self.__plugins[Plugins.AccessControll1].update_allowed_card_ids(register.value)

    def __access_control_2_enabled(self, register):
        if register.value == 1:
            if Plugins.AccessControll2 not in self.__plugins:
                key = register.base_name
                time_to_open = self.__registers.by_name(key + ".time_to_open").value

                exit_button_enabled = self.__registers.by_name(key + ".exit_button.enabled").value
                exit_button_input = self.__registers.by_name(key + ".exit_button.input").value

                lock_mechanism_enabled = self.__registers.by_name(key + ".lock_mechanism.enabled").value
                lock_mechanism_output = self.__registers.by_name(key + ".lock_mechanism.output").value

                card_reader_enabled = self.__registers.by_name(key + ".card_reader.enabled").value
                card_reader_vendor = self.__registers.by_name(key + ".card_reader.vendor").value
                card_reader_model = self.__registers.by_name(key + ".card_reader.model").value
                card_reader_serial_number = self.__registers.by_name(key + ".card_reader.serial_number").value
                card_reader_port_name = self.__registers.by_name(key + ".card_reader.port.name").value
                card_reader_port_baudrate = self.__registers.by_name(key + ".card_reader.port.baudrate").value
                card_reader_allowed_ids = self.__registers.by_name(key + ".allowed_attendees").value

                config = {
                    "name": "Access control 2",
                    "time_to_open":time_to_open,

                    "exit_button_enabled": exit_button_enabled,
                    "exit_button_input": exit_button_input,

                    "lock_mechanism_enabled": lock_mechanism_enabled,
                    "lock_mechanism_output": lock_mechanism_output,

                    "card_reader_enabled": card_reader_enabled,
                    "card_reader_vendor": card_reader_vendor,
                    "card_reader_model": card_reader_model,
                    "card_reader_serial_number": card_reader_serial_number,
                    "card_reader_port_name": card_reader_port_name,
                    "card_reader_port_baudrate": card_reader_port_baudrate,
                    "card_reader_allowed_ids": card_reader_allowed_ids,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.AccessControll2] = AccessControll(config)

                # Add Handlers.

                # Init
                self.__plugins[Plugins.AccessControll2].init()

        elif register.value == 0:
            if Plugins.AccessControll2 in self.__plugins:
                self.__plugins[Plugins.AccessControll2].shutdown()
                del self.__plugins[Plugins.AccessControll2]

    def __access_control_allowed_attenders_2(self, register):
        if Plugins.AccessControll2 not in self.__plugins:
            return

        self.__plugins[Plugins.AccessControll2].update_allowed_card_ids(register.value)

    def __hvac_enabled(self, register):
        if register.value == 1:
            if Plugins.HVAC not in self.__plugins:
                key = register.base_name

                delta_time = self.__registers.by_name(key + ".delta_time").value
                update_rate = self.__registers.by_name(key + ".update_rate").value
                thermal_mode = self.__registers.by_name(key + ".thermal_mode").value
                thermal_force_limit = self.__registers.by_name(key + ".thermal_force_limit").value
                adjust_temp = self.__registers.by_name(key + ".adjust_temp").value

                room_theromometer_enable = self.__registers.by_name(key + ".room_theromometer.enabled").value
                room_theromometer_mou = self.__registers.by_name(key + ".room_theromometer.mou").value
                room_theromometer_dev = self.__registers.by_name(key + ".room_theromometer.dev").value
                room_theromometer_dev_type = self.__registers.by_name(key + ".room_theromometer.type").value
                room_theromometer_circuit = self.__registers.by_name(key + ".room_theromometer.circuit").value

                upper_fan_enable = self.__registers.by_name(key + ".upper_fan.enabled").value
                upper_fan_vendor = self.__registers.by_name(key + ".upper_fan.vendor").value
                upper_fan_model = self.__registers.by_name(key + ".upper_fan.model").value
                upper_fan_output = self.__registers.by_name(key + ".upper_fan.output").value

                lower_fan_enable = self.__registers.by_name(key + ".lower_fan.enabled").value
                lower_fan_vendor = self.__registers.by_name(key + ".lower_fan.vendor").value
                lower_fan_model = self.__registers.by_name(key + ".lower_fan.model").value
                lower_fan_output = self.__registers.by_name(key + ".lower_fan.output").value

                upper_valve_enable = self.__registers.by_name(key + ".upper_valve.enabled").value
                upper_valve_vendor = self.__registers.by_name(key + ".upper_valve.vendor").value
                upper_valve_model = self.__registers.by_name(key + ".upper_valve.model").value
                upper_valve_output = self.__registers.by_name(key + ".upper_valve.output").value

                lower_valve_enable = self.__registers.by_name(key + ".lower_valve.enabled").value
                lower_valve_vendor = self.__registers.by_name(key + ".lower_valve.vendor").value
                lower_valve_model = self.__registers.by_name(key + ".lower_valve.model").value
                lower_valve_output = self.__registers.by_name(key + ".lower_valve.output").value

                convector_enable = self.__registers.by_name(key + ".convector.enabled").value
                convector_vendor = self.__registers.by_name(key + ".convector.vendor").value
                convector_model = self.__registers.by_name(key + ".convector.model").value
                convector_stage_1 = self.__registers.by_name(key + ".convector.stage_1.output").value
                convector_stage_2 = self.__registers.by_name(key + ".convector.stage_2.output").value
                convector_stage_3 = self.__registers.by_name(key + ".convector.stage_3.output").value


                config = {
                    "name": "HVAC",

                    "delta_time":delta_time,
                    "update_rate": update_rate,
                    "thermal_mode":thermal_mode,
                    "thermal_force_limit":thermal_force_limit,
                    "adjust_temp":adjust_temp,

                    "room_theromometer_enable": room_theromometer_enable,
                    "room_theromometer_mou": room_theromometer_mou,
                    "room_theromometer_dev": room_theromometer_dev,
                    "room_theromometer_dev_type": room_theromometer_dev_type,
                    "room_theromometer_circuit": room_theromometer_circuit,

                    "upper_fan_enable": upper_fan_enable,
                    "upper_fan_vendor": upper_fan_vendor,
                    "upper_fan_model": upper_fan_model,
                    "upper_fan_output": upper_fan_output,

                    "lower_fan_enable": lower_fan_enable,
                    "lower_fan_vendor": lower_fan_vendor,
                    "lower_fan_model": lower_fan_model,
                    "lower_fan_output": lower_fan_output,

                    "upper_valve_enable": upper_valve_enable,
                    "upper_valve_vendor": upper_valve_vendor,
                    "upper_valve_model": upper_valve_model,
                    "upper_valve_output": upper_valve_output,

                    "lower_valve_enable": lower_valve_enable,
                    "lower_valve_vendor": lower_valve_vendor,
                    "lower_valve_model": lower_valve_model,
                    "lower_valve_output": lower_valve_output,

                    "convector_enable": convector_enable,
                    "convector_vendor": convector_vendor,
                    "convector_model": convector_model,
                    "convector_stage_1": convector_stage_1,
                    "convector_stage_2": convector_stage_2,
                    "convector_stage_3": convector_stage_3,
                    "controller": self.__controller,
                    "erp_service": self.__erp_service
                }

                # Create device.
                self.__plugins[Plugins.HVAC] = HVAC(config)
                self.__plugins[Plugins.HVAC].init()

        if register.value == 0:
            if Plugins.HVAC in self.__plugins:
                self.__plugins[Plugins.HVAC].shutdown()
                del self.__plugins[Plugins.HVAC]

    def __hvac_adjust_temp(self, register):

        if Plugins.HVAC not in self.__plugins:
            return

        min_temp = 2.5
        max_temp = -2.5

        key = "hvac.temp.min"
        if self.__registers.exists(key):
            min_temp = self.__registers.by_name(key).value

        key = "hvac.temp.max"
        if self.__registers.exists(key):
            max_temp = self.__registers.by_name(key).value

        actual_temp = register.value

        if actual_temp < min_temp:
            actual_temp = min_temp

        if actual_temp > max_temp:
            actual_temp = max_temp

        self.__plugins[Plugins.HVAC].adjust_temp = actual_temp

    def __hvac_goal_building_temp(self, register):

        if Plugins.HVAC not in self.__plugins:
            return

        # @see https://experta.bg/L/S/122745/m/Fwntindd
        min_temp = 18
        max_temp = 26

        actual_temp = register.value

        if actual_temp < min_temp:
            actual_temp = min_temp

        if actual_temp > max_temp:
            actual_temp = max_temp

        self.__plugins[Plugins.HVAC].building_temp = actual_temp


    def __light_enabled(self, register):
        if register.value == 1:
            if Plugins.HVAC not in self.__plugins:
                key = register.base_name

                sensor_mou = self.__registers.by_name(key + ".sensor.mou").value
                sensor_dev = self.__registers.by_name(key + ".sensor.dev").value
                sensor_circuit = self.__registers.by_name(key + ".sensor.circuit").value
                v1_output = self.__registers.by_name(key + ".v1.output").value
                v2_output = self.__registers.by_name(key + ".v2.output").value

                config = {
                    "name": "Lamps",
                    "sensor_mou":sensor_mou,
                    "sensor_dev":sensor_dev,
                    "sensor_circuit": sensor_circuit,
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
            if Plugins.MainLight in self.__plugins:
                self.__plugins[Plugins.WDTTablet].shutdown()
                del self.__plugins[Plugins.WDTTablet]

    def __wdt_tablet_reset(self, register):
        if register.value == 1:
            if Plugins.WDTTablet in self.__plugins:
                self.__plugins[Plugins.WDTTablet].reset_device()

#endregion

#region Public Methods

    def update(self):
        """Update plugins."""

        self.__controller.update()

        for key in self.__plugins:
            self.__plugins[key].update()

        # # JSON output
        # import json
        # bgerp_regs = self.__registers.by_source(Source.bgERP)
        # print(json.dumps(bgerp_regs.to_dict(), indent=4, sort_keys=True))

        # ztm_regs = self.__registers.by_source(Source.Zontromat)
        # print(json.dumps(ztm_regs.to_dict(), indent=4, sort_keys=True))

        # # CSV output
        # bgerp_regs = self.__registers.by_source(Source.bgERP)
        # with open("bgerp_registers.csv", "w") as f:
        #     for register in bgerp_regs:
        #         f.write("{}\t{}\n".format(register.name, register.value))

        # ztm_regs = self.__registers.by_source(Source.Zontromat)
        # with open("ztm_registers.csv", "w") as f:
        #     for register in ztm_regs:
        #         f.write("{}\t{}\n".format(register.name, register.value))

        ts = int(time.time())

        if Plugins.WindowClosed in self.__plugins:
            register = self.__registers.by_name("window_closed.state")
            register.value = self.__plugins[Plugins.WindowClosed].get_state()
            register.ts = ts

        if Plugins.DoorClosed in self.__plugins:
            register = self.__registers.by_name("door_closed.state")
            register.value = self.__plugins[Plugins.DoorClosed].get_state()
            register.ts = ts

        if Plugins.PIRDetector in self.__plugins:
            register = self.__registers.by_name("pir_detector.state")
            register.value = self.__plugins[Plugins.PIRDetector].get_state()
            register.ts = ts

        if Plugins.AntiTampering in self.__plugins:
            register = self.__registers.by_name("anti_tampering.state")
            register.value = self.__plugins[Plugins.AntiTampering].get_state()
            register.ts = ts

        if Plugins.FireDetect in self.__plugins:
            register = self.__registers.by_name("fire_detect.state")
            register.value = self.__plugins[Plugins.FireDetect].get_state()
            register.ts = ts

        if Plugins.WaterCounter in self.__plugins:
            register = self.__registers.by_name("water_cnt.state")
            register.value = self.__plugins[Plugins.WaterCounter].get_state()
            register.ts = ts

        if Plugins.Loop1Counter in self.__plugins:
            register = self.__registers.by_name("loop1_cnt.state")
            register.value = self.__plugins[Plugins.Loop1Counter].get_state()
            register.ts = ts

        if Plugins.Loop2Counter in self.__plugins:
            register = self.__registers.by_name("loop2_cnt.state")
            register.value = self.__plugins[Plugins.Loop2Counter].get_state()
            register.ts = ts

        if Plugins.AirTempUpper in self.__plugins:
            register = self.__registers.by_name("air_temp_upper.state")
            register.value = self.__plugins[Plugins.AirTempUpper].get_state()
            register.ts = ts

        if Plugins.AirTempLower in self.__plugins:
            register = self.__registers.by_name("air_temp_lower.state")
            register.value = self.__plugins[Plugins.AirTempLower].get_state()
            register.ts = ts

        if Plugins.AirTempCentral in self.__plugins:
            register = self.__registers.by_name("air_temp_lower.state")
            register.value = self.__plugins[Plugins.AirTempCentral].get_state()
            register.ts = ts

        if Plugins.RoomLight in self.__plugins:
            register = self.__registers.by_name("room_light.state")
            register.value = self.__plugins[Plugins.RoomLight].get_state()
            register.ts = ts

        if Plugins.Loop1Temperature in self.__plugins:
            register = self.__registers.by_name("loop_1_temp.state")
            register.value = self.__plugins[Plugins.Loop1Temperature].get_state()
            register.ts = ts

        if Plugins.Loop2Temperature in self.__plugins:
            register = self.__registers.by_name("loop_2_temp.state")
            register.value = self.__plugins[Plugins.Loop2Temperature].get_state()
            register.ts = ts

        if Plugins.PowerMeter in self.__plugins:
            power_state = self.__plugins[Plugins.PowerMeter].get_state()

            register = self.__registers.by_name("current_power.state")
            register.value = power_state["current_power"]
            register.ts = ts

            register = self.__registers.by_name("total_energy.state")
            register.value = power_state["total_energy"]
            register.ts = ts

        if Plugins.Blinds in self.__plugins:
            stste = self.__plugins[Plugins.Blinds].get_state()

        if Plugins.AccessControll1 in self.__plugins:
            stste = self.__plugins[Plugins.AccessControll1].get_state()

        if Plugins.AccessControll2 in self.__plugins:
            stste = self.__plugins[Plugins.AccessControll2].get_state()

        if Plugins.HVAC in self.__plugins:
            stste = self.__plugins[Plugins.HVAC].get_state()

        if Plugins.MainLight in self.__plugins:
            stste = self.__plugins[Plugins.MainLight].get_state()

        if Plugins.WDTTablet in self.__plugins:
            register = self.__registers.by_name("wdt_tablet.state")
            register.value = self.__plugins[Plugins.WDTTablet].get_state()
            register.ts = ts

    def shutdown(self):
        """Shutdown plugins."""

        for key in self.__plugins:
            self.__plugins[key].shutdown()

#endregion

#region Static Methods

    @staticmethod
    def get_instance(registers, controller, erp_service):
        """Singelton instance."""

        if PluginsManager.__instance is None:
            PluginsManager.__instance = PluginsManager(registers, controller, erp_service)

        return PluginsManager.__instance

#endregion
