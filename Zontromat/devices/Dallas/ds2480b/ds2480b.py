#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Zontromat - Zonal Electronic Automation

Copyright (C) [2021] [POLYGONTeam Ltd.]

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
import traceback
from enum import Enum

import serial

from devices.base_device import BaseDevice
from devices.Dallas.ds2480b.commands import Commands
from devices.Dallas.ds2480b.slew_rate_controll import PulldownSlewRateControl
from devices.Dallas.ds2480b.low_time import Write1LowTime
from devices.Dallas.ds2480b.data_sample import DataSampleOffsetAndWrite0RecoveryTime

from utils.logger import get_logger

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2021, POLYGON Team Ltd."
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

class DS2480B(BaseDevice):
    """DS2480B UART to 1W media convertor.
    """

#region Attributes

    __serial_port = None
    """Communication port.
    """

    __logger = None
    """Logger
    """

    __timeout = 5
    """Timeout
    """

#endregion

#region Constructor

    def __init__(self, **config):
        """Constructor
        """

        super().__init__(config)

        self.__logger = get_logger(__name__)

        # Create port.
        self.__serial_port = serial.Serial(\
            port=self._config["port_name"],\
            baudrate=self._config["baudrate"],
            timeout=1)

        if "timeout" in self._config:
            self.__timeout = self._config["timeout"]

#endregion

#region Private Methods

    def __make_buffer(self, frame):
        """Make human readable the buffer."""

        debug_string = ""

        for item in frame:
            debug_string += " {:02x}".format(item).upper()

        return debug_string

    def __send(self, frame):
        """Send request."""

        msg = "TX > {}".format(self.__make_buffer(frame))
        self.__logger.debug(msg)
        self.__serial_port.write(frame)

    def __receive(self):
        """Receive response.
        """

        frame = None
        wait = 0.1
        times = 0

        while True:
            size = self.__serial_port.inWaiting()
            if size > 0:
                frame = self.__serial_port.read(size)
                break

            times += wait
            time.sleep(wait)

            if times > self.__timeout:
                raise TimeoutError("Time out has ocurred in Communicator.")

        msg = "RX < {}".format(self.__make_buffer(frame))
        self.__logger.debug(msg)
        return frame

    def __send_request(self, data):
        """Send request.

        Args:
            data (byte array): Request package.

        Returns:
            byte array: Response package.
        """

        req_frame = None
        res_frame = None

        req_frame = bytearray(data)

        if self.__serial_port.isOpen() is False:
            raise FileNotFoundError("Port is not opened on level Communicator.")

        #self._open()
        self.__send(req_frame)
        res_frame = self.__receive()
        #self._close()
        return res_frame

    def __decode_search_response(self, response):

        bytes_count = len(response)
        if bytes_count < 17:
            raise ValueError("Invalid response length.") 

        last_zero = 0

        rom_code_temp_buffer = []

        for index in range(21):
            rom_code_temp_buffer.append(0x00)

        BitsInByte = 8

        def read_bit(buffer, location):

            buf_len = len(buffer)
            if location >= buf_len * BitsInByte:
                # nameof(location), $"buffer.Count = {buffer.Count}  location={location}"
                raise IndexError("Location {}".format(location))

            n_byte = int(location / BitsInByte)
            n_bit = int(location - (n_byte * BitsInByte))

            b = buffer[n_byte]
            for index in range(n_bit):
                b = b >> 1

            return b & 0x01

        def write_bit(buffer, location, value):

            buf_len = len(buffer)
            if location >= buf_len * BitsInByte:
                # nameof(location), $"buffer.Count = {buffer.Count}  location={location}"
                raise IndexError("Location {}".format(location))


            if not ((value == 0) or (value == 1)):
                raise ValueError("value should be 0 or 1, not {}".format(value))

            n_byte = int(location / BitsInByte)
            n_bit = int(location - (n_byte * BitsInByte))

            mask = 0x01
            for index in range(n_bit):
                mask = mask << 1

            if value == 1:
                buffer[n_byte] = (buffer[n_byte] | mask)

            else:
                buffer[n_byte] = (buffer[n_byte] & (~mask))


        for index in range(64):
            if index == 59:
                print("STOP")
            print(index)
            write_bit(rom_code_temp_buffer, index, read_bit(response, index * 2 + 1 + 8 + 8))

            print("Buffer: {}".format(self.__make_buffer(rom_code_temp_buffer)))
            if (read_bit(response, index * 2 + 8 + 8) == 1) and (read_bit(response, index * 2 + 1 + 8 + 8) == 0):

                last_zero = (index + 1)

        '''
        for (byte i = 0; i < 64; i++)
        {
            BitUtility.WriteBit(this.romCodeTempBuffer, i, BitUtility.ReadBit(this.receiveBuffer, i * 2 + 1 + 8 + 8));

            if ((BitUtility.ReadBit(this.receiveBuffer, i * 2 + 8 + 8) == 1) && (BitUtility.ReadBit(this.receiveBuffer, i * 2 + 1 + 8 + 8) == 0))
            {
                lastZero = (byte)(i + 1);
            }
        }
        '''

        print(response)

        return None

#endregion

#region Methods

    def connect(self):
        """Connect to the device.
        """

        if self.__serial_port.isOpen() is False:

            self.__serial_port.timeout = self.__timeout
            self.__serial_port.setDTR(False)
            self.__serial_port.setRTS(False)
            self.__serial_port.open()

    def disconnect(self):
        """Disconnect from device.
        """

        if self.__serial_port.isOpen() is True:

            self.__serial_port.setDTR(False)
            self.__serial_port.setRTS(False)
            self.__serial_port.close()

    def sync_the_uart(self):
        """Sync the bus.
        """

        self.reset_the_bus()

    def reset_the_bus(self, **config):
        """Reset the bus.
        """

        request = []

        mode = Commands.CommandResetAtFlexSpeed.value
        if "mode" in config:
            mode = config["mode"].value

        request.append(Commands.SwitchToCommandMode.value)
        request.append(mode)

        response = self.__send_request(request)

        return response

    def configure_the_bus(self, **config):
        """Configure the bus.
        """

        request = []

        slew_rate = PulldownSlewRateControl.V1p37.value
        if "slew_rate" in config:
            slew_rate = config["slew_rate"].value

        low_time = Write1LowTime.US11.value
        if "low_time" in config:
            low_time = config["low_time"].value

        sample_offset = DataSampleOffsetAndWrite0RecoveryTime.US10.value
        if "sample_offset" in config:
            sample_offset = config["sample_offset"].value

        request.append(slew_rate)
        request.append(low_time)
        request.append(sample_offset)

        response = self.__send_request(request)

        return response

    def search_the_bus(self, **config):
        """Search the 1W bus.
        """

        request = []

        request.append(Commands.SwitchToDataMode.value)

        commands = []
        if "commands" in config:
            commands = config["commands"]
        for command in commands:
            request.append(command)

        request.append(Commands.SwitchToCommandMode.value)
        request.append(Commands.CommandSearchAcceleratorControlOnAtRegularSpeed.value)
        request.append(Commands.SwitchToDataMode.value)
        for item in range(16):
            request.append(0x00)
        request.append(Commands.SwitchToCommandMode.value)
        request.append(Commands.CommandSearchAcceleratorControlOffAtRegularSpeed.value)

        response = self.__send_request(request)

        decoded_response = self.__decode_search_response(response)

        return decoded_response

    def read_device(self, **config):
        """Read device.
        """

        request = []

        request.append(Commands.SwitchToDataMode.value)

        commands = []
        if "commands" in config:
            commands = config["commands"]
        for command in commands:
            request.append(command)

        request.append(Commands.SwitchToCommandMode.value)
        request.append(Commands.CommandSingleBitReadDataAtFlexSpeed.value)

        response = self.__send_request(request)

        return response

    def read_device_param(self, **config):
        """[summary]
        """

        request = []

        request.append(Commands.SwitchToDataMode.value)

        commands = []
        if "commands" in config:
            commands = config["commands"]
        for command in commands:
            request.append(command)

        response = self.__send_request(request)

        return response

    def read_scratchpad(self, **config):
        """[summary]
        """

        request = []

        request.append(Commands.SwitchToDataMode.value)

        commands = []
        if "commands" in config:
            commands = config["commands"]
        for command in commands:
            request.append(command)

        response = self.__send_request(request)

        return response

#endregion
