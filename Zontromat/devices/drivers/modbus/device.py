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

from struct import pack, unpack

from devices.drivers.modbus.parameter_type import ParameterType

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

class Device():
    """Base class MODBUS devices."""

    #region Attributes

    _parameters = []
    """Device parameters."""

    #endregion

    #region Getters and Setters

    @property
    def parameters(self):
        """Returns device parameters.

        Returns
        -------
        float
            Parameter value.
        """

        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets device parameters.

        Parameters
        ----------
        registers : array
            Device parameters.
        """

        self._parameters = parameters

    #endregion

    #region Public Methods

    def get_registers_ids(self):
        """Get registers IDs.

        Returns
        -------
        array
            Registers IDs.
        """

        registers_ids = []

        reg_count = len(self._parameters)

        for reg_index in range(0, reg_count):
            addresses = self._parameters[reg_index].addresses
            adr_count = len(addresses)
            for adr_index in range(0, adr_count):
                registers_ids.append(addresses[adr_index])

        return registers_ids

    def get_parameters_names(self):
        """Get parameters names.

        Returns
        -------
        array
            Parameters names.
        """

        parameters = []

        reg_count = len(self._parameters)

        for reg_index in range(0, reg_count):
            parameter_name = self._parameters[reg_index].parameter_name
            parameters.append(parameter_name)

        return parameters

    def get_parameter_value(self, parameter, registers):
        """Returns parameter value.

        Parameters
        ----------
        parameter : str
            Parameter name.
        registers : array
            Registers data.

        Returns
        -------
        float
            Parameter value.
        """

        if parameter is None:
            raise Exception('Invalid parameter name.')

        if not self._parameters:
            raise Exception('Missing parameter.')

        reg_count = len(self._parameters)
        value = None

        for reg_index in range(0, reg_count):
            parameter_name = self._parameters[reg_index].parameter_name

            if parameter == parameter_name:
                parameter_type = self._parameters[reg_index].data_type
                addresses = self._parameters[reg_index].addresses
                value = Device.converts_to_parameter(parameter_type, addresses, registers)
                break

        return value

    def get_parameters_mous(self):
        """Returns parameters measuring units.

        Returns
        -------
        array
            Array of parametterses masuring units.
        """

        registers_mous = []

        reg_count = len(self._parameters)

        for reg_index in range(0, reg_count):
            mou = self._parameters[reg_index].get_mou()
            registers_mous[reg_index] = mou

        return registers_mous

    def get_parameters_values(self, registers):
        """Returns parameters valus.

        Parameters
        ----------
        registers : array
            Registers data.

        Returns
        -------
        array
            Array of parametters values.
        """

        if registers is None:
            raise Exception('Invalid registers.')

        #/** @var array Parameters parameters */
        parameters = self.get_parameters_names()

        #/** @var array Values values */
        values = {}

        for parameter in parameters:
            values[parameter] = self.get_parameter_value(parameter, registers)

        return values

    #endregion

    #region Private Methods

    @staticmethod
    def converts_to_parameter(parameter_type, registers, registers_data):
        """Convert registers data to a single parameter.

        Parameters
        ----------
        parameter_type : ParameterType
            Data type.
        registers : array
            Registers addresses.
        registers_data : array
            Registers data.

        Returns
        -------
        float
            Parameter value.
        """

        if ParameterType.is_valid_type(parameter_type) is not True:
            raise Exception('Modbus data type missmatch.')

        if not registers:
            raise Exception('Invalid registers length.')

        #/** @var object Unpacked float value. value */
        value = None

        if parameter_type == ParameterType.INT16_T:
            value = registers_data[registers[0]]

        elif parameter_type == ParameterType.UINT16_T:
            value = registers_data[registers[0]]

        elif parameter_type == ParameterType.INT32_T:
            raise Exception('Not implemented')

        elif parameter_type == ParameterType.UINT32_T:
            raise Exception('Not implemented')

        elif parameter_type == ParameterType.FLOAT:
            #/** @var array Packet binary data. bin_data */
            bin_data = None
            bin_data = pack(
                '<HH',
                registers_data[registers[1]],
                registers_data[registers[0]])
            value = unpack('f', bin_data)[0]

        return value

    #endregion
