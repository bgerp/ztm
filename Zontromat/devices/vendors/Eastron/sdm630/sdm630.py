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

from devices.drivers.modbus.device import ModbusDevice
from devices.drivers.modbus.parameter import Parameter
from devices.drivers.modbus.parameter_type import ParameterType
from devices.drivers.modbus.register_type import RegisterType

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

class SDM630(ModbusDevice):
    """This class is dedicated to read data from SDM630 energy meter.

    See https://bg-etech.de/download/manual/SDM630Register1-5.pdf"""

#region Constructor

    def __init__(self, **config):
        """Constructor"""

        super().__init__(config)

        self._vendor = "Eastron"

        self._model = "SDM630"

        self._parameters.append(\
            Parameter("Phase1LineToNeutralVolts", "V",\
            ParameterType.FLOAT, [0, 1], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2LineToNeutralVolts", "V",\
            ParameterType.FLOAT, [2, 3], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3LineToNeutralVolts", "V",\
            ParameterType.FLOAT, [4, 5], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1Current", "A",\
            ParameterType.FLOAT, [6, 7], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2Current", "A",\
            ParameterType.FLOAT, [8, 9], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3Current", "A",\
            ParameterType.FLOAT, [10, 11], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1Power", "W",\
            ParameterType.FLOAT, [12, 13], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2Power", "W",\
            ParameterType.FLOAT, [14, 15], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3Power", "W",\
            ParameterType.FLOAT, [16, 17], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1VoltAmps", "VA",\
            ParameterType.FLOAT, [18, 19], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2VoltAmps", "VA",\
            ParameterType.FLOAT, [20, 21], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3VoltAmps", "VA",\
            ParameterType.FLOAT, [22, 23], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1VoltAmpsReactive", "VAr",\
            ParameterType.FLOAT, [24, 25], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2VoltAmpsReactive", "VAr",\
            ParameterType.FLOAT, [26, 27], RegisterType.ReadInputRegisters))

        self._parameters.append\
            (Parameter("Phase3VoltAmpsReactive", "VAr",\
            ParameterType.FLOAT, [28, 29], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1PowerFactor", "Deg",\
            ParameterType.FLOAT, [30, 31], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2PowerFactor", "Deg",\
            ParameterType.FLOAT, [32, 33], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3PowerFactor", "Deg",\
            ParameterType.FLOAT, [34, 35], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1PhaseAngle", "Deg",\
            ParameterType.FLOAT, [36, 37], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2PhaseAngle", "Deg",\
            ParameterType.FLOAT, [38, 39], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3PhaseAngle", "Deg",\
            ParameterType.FLOAT, [40, 41], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("AverageLineToNeutralVolts", "V",\
            ParameterType.FLOAT, [42, 43], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("AverageLineCurrent", "A",\
            ParameterType.FLOAT, [46, 47], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("SumOfLineCurrents", "A",\
            ParameterType.FLOAT, [48, 49], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemPower", "W",\
            ParameterType.FLOAT, [52, 53], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemVoltAmps", "VA",\
            ParameterType.FLOAT, [56, 57], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemVAr", "VA",\
            ParameterType.FLOAT, [60, 61], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemPowerFactor", "Deg",\
            ParameterType.FLOAT, [62, 63], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemPhaseAngle", "Deg",\
            ParameterType.FLOAT, [66, 67], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("FrequencyOfSupplyVoltages", "Hz",\
            ParameterType.FLOAT, [70, 71], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalImportkWh", "kWh",\
            ParameterType.FLOAT, [72, 73], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalExportkWh", "kWh",\
            ParameterType.FLOAT, [74, 75], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalImportkVAarh", "kVArh",\
            ParameterType.FLOAT, [76, 77], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalExportkVAarh", "kVArh",\
            ParameterType.FLOAT, [78, 79], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalVAh", "kVAh",\
            ParameterType.FLOAT, [80, 81], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Ah", "Ah",\
            ParameterType.FLOAT, [82, 83], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemPowerDemand", "VA",\
            ParameterType.FLOAT, [84, 85], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumTotalSystemPowerDemand", "VA",\
            ParameterType.FLOAT, [86, 87], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalSystemVaDemand", "VA",\
            ParameterType.FLOAT, [100, 101], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumTotalSystemVADemand", "VA",\
            ParameterType.FLOAT, [102, 103], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("NeutralCurrentDemand", "A",\
            ParameterType.FLOAT, [104, 105], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumNeutralCurrentDemand", "A",\
            ParameterType.FLOAT, [106, 107], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Line1ToLine2Volts", "V",\
            ParameterType.FLOAT, [200, 201], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Line2ToLine3Volts", "V",\
            ParameterType.FLOAT, [202, 203], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Line3ToLine1Volts", "V",\
            ParameterType.FLOAT, [204, 205], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("AverageLineToLineVolts", "V",\
            ParameterType.FLOAT, [206, 207], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("NeutralCurrent", "A",\
            ParameterType.FLOAT, [224, 225], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1L/NVoltsThd", "%",\
            ParameterType.FLOAT, [234, 235], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2L/NVoltsThd", "%",\
            ParameterType.FLOAT, [236, 237], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3L/NVoltsThd", "%",\
            ParameterType.FLOAT, [238, 239], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1CurrentThd", "%",\
            ParameterType.FLOAT, [240, 241], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2CurrentThd", "%",\
            ParameterType.FLOAT, [242, 243], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3CurrentThd", "%",\
            ParameterType.FLOAT, [244, 245], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("AverageLineToNeutralVoltsTHD", "%",\
            ParameterType.FLOAT, [248, 249], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("AverageLineCurrentTHD", "%",\
            ParameterType.FLOAT, [250, 251], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase1CurrentDemand", "A",\
            ParameterType.FLOAT, [258, 259], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase2CurrentDemand", "A",\
            ParameterType.FLOAT, [260, 261], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Phase3CurrentDemand", "A",\
            ParameterType.FLOAT, [262, 263], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumPhase1CurrentDemand", "A",\
            ParameterType.FLOAT, [264, 265], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumPhase2CurrentDemand", "A",\
            ParameterType.FLOAT, [266, 267], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("MaximumPhase3CurrentDemand", "A",\
            ParameterType.FLOAT, [268, 269], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Line1ToLine2VoltsTHD", "%",\
            ParameterType.FLOAT, [334, 335], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Line2ToLine3VoltsTHD", "%",\
            ParameterType.FLOAT, [336, 337], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("Line3ToLine1VoltsTHD", "%",\
            ParameterType.FLOAT, [338, 339], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("AverageLineToLineVoltsTHD", "%",\
            ParameterType.FLOAT, [340, 341], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalkWh", "kWh",\
            ParameterType.FLOAT, [342, 343], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("TotalkVArh", "kVArh",\
            ParameterType.FLOAT, [344, 345], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L1ImportkWh", "kWh",\
            ParameterType.FLOAT, [346, 347], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L2ImportkWh", "kWh",\
            ParameterType.FLOAT, [348, 349], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L3ImportkWh", "kWh",\
            ParameterType.FLOAT, [350, 351], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L1ExportkWh", "kWh",\
            ParameterType.FLOAT, [352, 353], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L2ExportkWh", "kWh",\
            ParameterType.FLOAT, [354, 355], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L3ExportkWh", "kWh",\
            ParameterType.FLOAT, [356, 357], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L1TotalkWh", "kWh",\
            ParameterType.FLOAT, [358, 359], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L2TotalkWh", "kWh",\
            ParameterType.FLOAT, [360, 361], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L3TotalkWh", "kWh",\
            ParameterType.FLOAT, [362, 363], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L1ImportkVArh", "kVArh",\
            ParameterType.FLOAT, [364, 365], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L2ImportkVArh", "kVArh",\
            ParameterType.FLOAT, [366, 367], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L3ImportkVArh", "kVArh",\
            ParameterType.FLOAT, [368, 369], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L1ExportkVArh", "kVArh",\
            ParameterType.FLOAT, [370, 371], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L2ExportkVArh", "kVArh",\
            ParameterType.FLOAT, [372, 373], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L3ExportkVArh", "kVArh",\
            ParameterType.FLOAT, [374, 375], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L1TotalkVArh", "kVArh",\
            ParameterType.FLOAT, [376, 377], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L2TotalkVArh", "kVArh",\
            ParameterType.FLOAT, [378, 379], RegisterType.ReadInputRegisters))

        self._parameters.append(\
            Parameter("L3TotalkVArh", "kVArh",\
            ParameterType.FLOAT, [380, 381], RegisterType.ReadInputRegisters))

    #endregion
