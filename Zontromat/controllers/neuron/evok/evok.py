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

import json
import struct

import requests

from utils.logger import get_logger

from controllers.base_controller import BaseController

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

class Evok(BaseController):
    """This class is dedicated to transfer information from and to Evok series.
        See https://evok.api-docs.io/1.0/rest
    """

#region Attributes

    __logger = None
    """Logger"""

    __json_data = None
    """JSON data container."""

    __timeout = 5
    """Communication timeout."""

    __host = ""
    """Base URI."""

    __rest_all = "/rest/all/"
    """REST path to All devices."""

    __rest_register = "/rest/register/"
    """REST path to Registers."""

    __rest_led = "/rest/led/"
    """REST path to LEDs."""

    __rest_relay = "/rest/relay/"
    """REST path to Relays."""

    __rest_output = "/rest/output/"
    """REST path to DO."""

    __rest_di = "/rest/di/"
    """REST path to DI."""

    __rest_ao = "/rest/ao/"
    """REST path to AO."""

    __rest_ai = "/rest/ai/"
    """REST path to AI."""

    __rest_watchdog = "/rest/watchdog/"
    """REST path to WD"""

    __instance = None
    """Singelton instance."""

#endregion

#region Properties

    @property
    def json_data(self):
        """Returns JSON response of the device.

        Returns
        -------
        str
            Whole JSON data.
        """
        return self.__json_data

    @property
    def host(self):
        """Returns Host URL of the servie.

        Returns
        -------
        str
            Host URL of the servie.
        """

        return self.__host

    @host.setter
    def host(self, host):
        """Set Host URL of the service.

        Parameters
        ----------
        host : str
            Host URL of the servie.
        """

        host_no_slash = host

        if host_no_slash.endswith("/"):
            host_no_slash = host_no_slash[:-1]

        self.__host = host_no_slash

    @property
    def timeout(self):
        """Get timeout.

        Returns
        -------
        int
            Timeout.
        """

        return self.__timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout.

        Parameters
        ----------
        timeout : int
            Timeout.
        """

        self.__timeout = timeout

    @property
    def last_com_time(self):
        """Get last connection time. [seconds]

        Returns
        -------
        str
            Evok last communication time.
        """

        return self.__get_device_parameter("last_comm")

    @property
    def model(self):
        """Get device model.

        Returns
        -------
        str
            Evok model.
        """

        return self.__get_device_parameter("model")

    @property
    def serial_number(self):
        """Get device serial number.

        Returns
        -------
        str
            Evok serial number.
        """

        return self.__get_device_parameter("sn")

    @property
    def version(self):
        """Get device version.

        Returns
        -------
        str
            Evok software version.
        """

        return self.__get_device_parameter("ver2")

#endregion

#region Constructor

    def __init__(self, config):
        """Class constructor."""

        super().__init__(config)

        self.host = self._config["host"]
        self.timeout = self._config["timeout"]
        self.__logger = get_logger(__name__)

#endregion

#region Private Methods

    def __get_device_parameter(self, parameter):
        """Get device parameter of the Evok.

        Parameters
        ----------
        parameter : str
            Parameter name.

        Returns
        -------
        str
            Parameter value.
        """

        value = None

        for field in self.__json_data:
            if ("circuit" in field) and ("dev" in field) and (parameter in field):
                if (field["circuit"] == "1") and (field["dev"] == "neuron"):
                    value = field[parameter]
                    break

        return value

#endregion

#region Protected Methods

    def _update(self):
        """Make request to the device to update the data.

        This method is directly related to the EVOK REST API.
        See https://evok-14.api-docs.io/1.11/rest/get-complete-state
        """

        state = False

        # Call the Evok.
        uri = self.host + self.__rest_all

        try:
            response = requests.get(uri, timeout=self.__timeout)

            if response.status_code == 200:
                self.__json_data = json.loads(response.text)
                # Mark as successfull.
                state = True

            else:
                state = False

        except Exception:
            state = False

        return state

    def get_device(self, dev, circuit):
        """Get device from the list of all.

        Parameters
        ----------
        dev : str
            Device name
        circuit : str
            Circuit

        Returns
        -------
        mixed
            Description of device values and parameters.
        """

        if self.__json_data is None:
            raise BufferError("Data buffer is not set yet.")

        device = None

        for field in self.__json_data:
            if ("dev" in field)  and ("circuit" in field):
                if (field["dev"] == dev) and (field["circuit"] == circuit):
                    device = field

        return device

    def _get_1w_devices(self):
        """Get 1W device from the list of all.

        Returns
        -------
        tuple
            1W devices.
        """

        circuits = []

        if self.__json_data is None:
            return circuits

        for field in self.__json_data:
            if "dev" in field:
                if field["dev"] == "temp":
                    circuits.append(field)
                if field["dev"] == "1wdevice":
                    circuits.append(field)

        return circuits

    def _get_modbus_devices(self):
        """Get MODBUS device from the list of all.

        Returns
        -------
        tuple
            MODBUS devices.
        """
        circuits = []

        if self.__json_data is None:
            return circuits

        for field in self.__json_data:
            if "uart_port" in field:
                if field["uart_port"] != "":
                    circuits.append(field)

        return circuits

    def _get_uart_register(self, uart, dev_id, register, register_type=None):
        """Get register data of the device.

        Parameters
        ----------
        uart : int
            UART device
        dev_id : int
            Device ID
        register : int
            Register
        register_type : Modbus.ParameterType
            Register type

        Returns
        -------
        tuple
            UART register value.
        """

        device = None
        value = None
        circuit = Evok.generate_uart_circuit(uart, dev_id, register, register_type)
        device = self.get_device("register", circuit)

        if device is not None:
            if "value" in device:
                value = device["value"]

        return value

    def _get_uart_registers(self, uart, dev_id, registers, register_type=None):
        """ Get registers data of the UART device.

        Parameters
        ----------
        uart : int
            UART device
        dev_id : int
            Device ID
        register : int
            Register
        register : int
            Register
        register_type : int
            Register type.

        Returns
        -------
        list
            UART registers values.
        """

        values = {}

        if registers is None:
            raise Exception("Invalid registers.")

        for register in registers:
            values[register] = self._get_uart_register(uart, dev_id, register, register_type)

        return values

    def _set_uart_register(self, uart, dev_id, register, value):
        """Set register data of the UART device.

        Parameters
        ----------
        uart : str
            UART device
        dev_id : int
            Device ID
        register : int
            Register

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_uart_circuit(uart, dev_id, register)
        uri = self.__host + self.__rest_register + circuit
        response = requests.post(uri, data={"value":str(value)}, timeout=self.__timeout)
        return json.loads(response.text)

    def _set_led(self, major_index, minor_index, value=0):
        """Turn the LED state.

        See https://evok-14.api-docs.io/1.11/rest/get-uled-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            minor index
        value : int, optional
            value of the LED [1, 0]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_led + circuit
        response = requests.post(uri, data={"value":str(value)}, timeout=self.__timeout)
        return json.loads(response.text)

    def _set_relay(self, major_index, minor_index, value):
        """Turn the Relay state.

        See https://evok-14.api-docs.io/1.11/rest/change-relay-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        value : int, optional
            Value of the Relay [1, 0]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_relay + circuit
        response = requests.post(uri, data={"value":str(value)}, timeout=self.__timeout)
        return json.loads(response.text)

    def _set_digital_output(self, major_index, minor_index, value):
        """Turn the DO state.

        See https://evok.api-docs.io/1.0/rest/change-output-state-relay-alias

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        value : int, optional
            Value of the DO [1, 0]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_output + circuit
        response = requests.post(uri, data={"value":str(value), "mode":"Simple"}, \
            timeout=self.__timeout)
        return json.loads(response.text)

    def _set_pwm(self, major_index, minor_index, value=0, freq=8000):
        """Turn the PWM state.

        See https://evok-14.api-docs.io/1.11/rest/change-output-state-relay-alias

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        value : int, optional
            Value of the Duty Cycle [0, 99][%]
        freq : int, optional
            Value of the frequency [0, 10000][Hz]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_output + circuit
        response = requests.post(uri, data={"mode":"PWM", "pwm_duty":int(value), \
            "pwm_freq":int(freq)}, timeout=self.__timeout)
        return json.loads(response.text)

    def _set_analog_output(self, major_index, minor_index, value=0):
        """Turn the AO state.

        See https://evok.api-docs.io/1.0/rest/change-analog-output-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        value : int, optional
            Value of the AO [0, 10][V]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_ao + circuit

        response = requests.post(uri, data={"value":str(value), \
            "mode":"Voltage"}, timeout=self.__timeout)
        return json.loads(response.text)

    def _set_input_mode(self, major_index, minor_index, mode="Simple"):
        """Turn the DI state.

        See https://evok-14.api-docs.io/1.11/rest/change-digital-input-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        mode : str, optional
            Mode: Simple, DirectSwitch

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_di + circuit
        response = requests.post(uri, data={"mode":mode}, timeout=self.__timeout)
        return json.loads(response.text)

    def _set_input_debounce(self, major_index, minor_index, debounce=50):
        """Turn the DI state.

        See https://evok-14.api-docs.io/1.11/rest/change-digital-input-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        debounce : int, optional
            DEbounce time. [0, N][mS]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_di + circuit
        response = requests.post(uri, data={"debounce":str(debounce)}, timeout=self.__timeout)
        return json.loads(response.text)

    def _reset_input_counter(self, major_index, minor_index, counter=0):
        """Turn the DI state.

        See https://evok-14.api-docs.io/1.11/rest/change-digital-input-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        counter : int, optional
            Counter of the input. [0, N][inc]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_di + circuit
        response = requests.post(uri, data={"counter":str(counter)}, timeout=self.__timeout)
        return json.loads(response.text)

    def _toggle_input_counter(self, major_index, minor_index, value=0):
        """Turn the DI state.

        See https://evok-14.api-docs.io/1.11/rest/change-digital-input-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        value : int, optional
            Toggle the counter mode.

        Returns
        -------
        mixed
            JSON response data.
        """

        counter_mode = "False"

        if value:
            counter_mode = "True"
        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_di + circuit
        response = requests.post(uri, data={"counter_mode":str(counter_mode)}, \
            timeout=self.__timeout)
        return json.loads(response.text)

    def _save_current_state(self, major_index, minor_index):
        """Saves the current state fo the IOs of the Evok.

        See https://evok-14.api-docs.io/1.11/rest/change-watchdog-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index
        value : int, optional
            Toggle the counter mode.

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        uri = self.__host + self.__rest_watchdog + circuit
        response = requests.post(uri, data={"nv_save": 1}, timeout=self.__timeout)
        return json.loads(response.text)

    def _get_digital_input(self, major_index, minor_index):
        """Read digital input.

        See https://evok-14.api-docs.io/1.11/rest/change-watchdog-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)
        circuit_data = self.get_device("input", circuit)
        # uri = self.__host + self.__rest_di + circuit
        # response = requests.get(uri, timeout=self.__timeout)
        # return json.loads(response.text)
        return circuit_data

    def _get_counter(self, major_index, minor_index):
        """Read digital input counter.

        See https://evok-14.api-docs.io/1.11/rest/change-watchdog-state

        Parameters
        ----------
        major_index : int
            Major index
        minor_index : int
            Minor index

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = Evok.generate_device_circuit(major_index, minor_index)

        # circuit_data = self.get_device("input", circuit)
        # return circuit_data

        uri = self.__host + self.__rest_di + circuit
        response = requests.get(uri, timeout=self.__timeout)
        return json.loads(response.text)

    def _get_analog_in(self, major_index, minor_index):

        circuit = Evok.generate_device_circuit(major_index, minor_index)

        # circuit_data = self.get_device("input", circuit)
        # return circuit_data

        uri = self.__host + self.__rest_ai + circuit
        response = requests.get(uri, timeout=self.__timeout)
        return json.loads(response.text)

#endregion

#region Static Methods

    @staticmethod
    def generate_device_circuit(major_index, minor_index):
        """Generate a device circuit for major and minor index.

        Parameters
        ----------
        major_index : int
            Major index of the circuit.
        minor_index : int
            Minor index of the circuit.

        Returns
        -------
        str
            Evok circuit.
        """

        circuit = ""

        minor_index_l = ""
        if minor_index < 10:
            minor_index_l = "0" + str(minor_index)
        else:
            minor_index_l = minor_index

        circuit = str(major_index) + "_" + str(minor_index_l)

        return circuit

    @staticmethod
    def generate_uart_circuit(uart, dev_id, register, register_type=None):
        """Generate a device circuit for major, minor  index for.

        This method is directly related to the EVOK REST API.
        See https://evok.api-docs.io/1.0/json/get-uart-state-json

        Parameters
        ----------
        uart : int
            UART index.
        dev_id : int
            Modbus device ID.
        register : int
            MODBUS register ID.
        register_type : str
            Register type.

        Returns
        -------
        str
            UART circuit.
        """

        key = ""

        if register_type is not None:

            if "inp" in register_type:
                key = "UART_" + str(uart) + "_" + str(dev_id) + "_" + \
                    str(register) + "_" + register_type

            elif register_type == "":
                key = "UART_" + str(uart) + "_" + str(dev_id) + "_" + str(register)

        else:
            key = "UART_" + str(uart) + "_" + str(dev_id) + "_" + str(register)

        return key

    @staticmethod
    def read_eeprom():
        """Read Neurons EEPROM."""
        device_cfg = {
            "version": "UniPi 1.0",
            "devices": {
                "ai": {
                    "1": 5.564920867,
                    "2": 5.564920867,
                }
            },
            "version1": None,
            "version2": None,
            "serial": None,
            "model": None
        }

        # Try to access the EEPROM at /sys/bus/i2c/devices/1-0050/eeprom
        try:
            with open("/sys/bus/i2c/devices/1-0050/eeprom", "rb") as eeprom:

                content = eeprom.read()

                control = struct.unpack(">H", content[224:226])[0]

                if control == 64085:

                    if ord(content[226]) == 1 and ord(content[227]) == 1:
                        device_cfg["version"] = "UniPi 1.1"

                    elif ord(content[226]) == 11 and ord(content[227]) == 1:
                        device_cfg["version"] = "UniPi Lite 1.1"

                    else:
                        device_cfg["version"] = "UniPi 1.0"

                    device_cfg["version1"] = device_cfg["version"]

                    #AIs coeff
                    if device_cfg["version"] in ("UniPi 1.1", "UniPi 1.0"):
                        device_cfg["devices"] = {
                            "ai": {
                                "1": struct.unpack("!f", content[240:244])[0],
                                "2": struct.unpack("!f", content[244:248])[0],
                                }
                            }

                    else:
                        device_cfg["devices"] = {
                            "ai": {
                                "1": 0,
                                "2": 0,
                                }
                            }

                    device_cfg["serial"] = struct.unpack("i", content[228:232])[0]
        except Exception:
            pass

        # Try to access the EEPROM at /sys/bus/i2c/devices/1-0057/eeprom
        try:
            with open("/sys/bus/i2c/devices/1-0057/eeprom", "rb") as eeprom:

                # Get content.
                content = eeprom.read()

                # Get control sum.
                control = struct.unpack(">H", content[96:98])[0]
                if control == 64085:

                    # Version
                    v1 = content[99]
                    v2 = content[98]
                    version2 = "{}.{}".format(v1, v2)
                    device_cfg["version2"] = version2

                    # Model
                    model = struct.unpack("4s", content[106:110])
                    model = model[0]
                    model = model.decode("utf8")
                    device_cfg["model"] = model

                    # Serial Number
                    device_cfg["serial"] = struct.unpack("i", content[100:104])[0]

        except Exception:
            pass

        # Try to access the EEPROM at /sys/bus/i2c/devices/0-0057/eeprom
        try:
            with open("/sys/bus/i2c/devices/0-0057/eeprom", "rb") as eeprom:

                # Get content.
                content = eeprom.read()

                # Get control sum.
                control = struct.unpack(">H", content[96:98])[0]
                if control == 64085:

                    # Version
                    v1 = content[99]
                    v2 = content[98]
                    version2 = "{}.{}".format(v1, v2)
                    device_cfg["version2"] = version2

                    # Model
                    model = struct.unpack("4s", content[106:110])
                    model = model[0]
                    model = model.decode("utf8")
                    device_cfg["model"] = model

                    # Serial Number
                    device_cfg["serial"] = struct.unpack("i", content[100:104])[0]
        except Exception:
            pass

        return device_cfg

#endregion

#region Public Methods

    def device_to_uniname(self, device):
        """Convert device to unified GPIO name.

        Args:
            device (JSON): Device description.

        Returns:
            str: Unified device name.
        """

        target = None
        dev = device["dev"]
        circuit = device["circuit"]

        circuit = circuit.replace("0", "")
        index = circuit.split("_")
        major_index = int(index[0])
        minor_index = int(index[1])

        for item in self._gpio_map:
            if item != "identification":
                if dev == self._gpio_map[item]["dev"]\
                    and major_index == self._gpio_map[item]["major_index"]\
                    and minor_index == self._gpio_map[item]["minor_index"]:

                    target = item

        return target

#endregion

#region Base Controller Implementation

    def update(self):
        """Update controller state."""

        return self._update()

    def digital_read(self, pin):
        """Read the digital input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        Returns
        -------
        int
            State of the pin.
        """

        state = False

        if pin is None:
            raise ValueError("Pin can not be None.")

        l_pin = pin.replace("!", "")

        if not self.is_valid_gpio_type(l_pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(l_pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(l_pin):
            return state

        gpio_map = self._gpio_map[l_pin]
        response = self._get_digital_input(gpio_map["major_index"], gpio_map["minor_index"])
        if response is not None:
            state = response["value"]

        # Inversion
        polarity = pin.startswith("!")

        if polarity:
            state = not state
        else:
            state = bool(state)

        return state

    def digital_write(self, pin, value):
        """Write the digital output pin.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the output pin.

        Returns
        -------
        mixed
            State of the pin.
        """

        l_pin = pin.replace("!", "")
        response = None

        if not self.is_valid_gpio_type(l_pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(l_pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(l_pin):
            return response

        gpio_map = self._gpio_map[l_pin]

        # Inversion
        polarity = pin.startswith("!")
        state = 0

        if polarity:
            state = not value
        else:
            state = bool(value)

        state = int(state)

        if state > 1:
            state = 1

        if gpio_map["dev"] == "do":
            response = self._set_digital_output(gpio_map["major_index"],\
                gpio_map["minor_index"], state)
        elif gpio_map["dev"] == "relay":
            response = self._set_relay(gpio_map["major_index"], gpio_map["minor_index"], state)

        return response

    def analog_write(self, pin, value):
        """Write the analog input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the output pin.

        Returns
        -------
        int
            State of the pin.
        """

        response = None

        if not self.is_valid_gpio_type(pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(pin):
            return response

        gpio_map = self._gpio_map[pin]

        if gpio_map["dev"] == "ao":
            response = self._set_analog_output(gpio_map["major_index"],\
                gpio_map["minor_index"], value)
        elif gpio_map["dev"] == "pwm":
            response = self._set_pwm(gpio_map["major_index"], gpio_map["minor_index"], value)

        return response

    def read_counter(self, pin):
        """Read the digital counter input.

        Parameters
        ----------
        pin : str
            Pin index.

        Returns
        -------
        int
            State of the pin.
        """

        counter = 0

        if not self.is_valid_gpio_type(pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(pin):
            return counter

        gpio_map = self._gpio_map[pin]

        response = self._get_counter(gpio_map["major_index"], gpio_map["minor_index"])
        if response is not None:
            counter = response["counter"]

        return counter

    def analog_read(self, pin):
        """Write the analog input pin.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the output pin.

        Returns
        -------
        int
            State of the pin.
        """

        response = None

        if not self.is_valid_gpio_type(pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(pin):
            return response

        gpio_map = self._gpio_map[pin]

        if gpio_map["dev"] == "ai":
            response = self._get_analog_in(gpio_map["major_index"],\
                gpio_map["minor_index"])

        return response

    def write_counter(self, pin, value):
        """Write the digital counter value.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the counter.

        Returns
        -------
        int
            State of the pin.
        """

        response = None

        if not self.is_valid_gpio_type(pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(pin):
            return response

        gpio_map = self._gpio_map[pin]
        response = self._reset_input_counter(gpio_map["major_index"],\
            gpio_map["minor_index"], value)

        return response

    def set_led(self, pin, value):
        """Write the LED.

        Parameters
        ----------
        pin : str
            Pin index.

        value : int
            Value for the LED.

        Returns
        -------
        int
            State of the pin.
        """

        l_pin = pin.replace("!", "")

        response = None

        if not self.is_valid_gpio_type(l_pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(l_pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(l_pin):
            return response

        gpio_map = self._gpio_map[l_pin]

        # Inversion
        polarity = pin.startswith("!")
        state = 0

        if polarity:
            state = not value
        else:
            state = bool(value)

        state = int(state)

        response = self._set_led(gpio_map["major_index"], gpio_map["minor_index"], value)

        return response

    def read_temperature(self, dev, circuit):
        """Read the thermometer.

        Parameters
        ----------
        dev : str
            Dev ID.

        circuit : str
            Circuit ID.

        Returns
        -------
        int
            State of the device.
        """

        value = 0

        device = self.get_device(dev, circuit)

        if device is None:
            return value

        dev_type = device["typ"]

        if dev_type == "DS2438":
            value = device["temp"]

        elif dev_type == "DS18B20":
            value = device["value"]

        return value

    def read_light(self, dev, circuit):
        """Read the light sensor.

        Parameters
        ----------
        dev : str
            Dev ID.

        circuit : str
            Circuit ID.

        Returns
        -------
        int
            State of the device.
        """

        value = 0

        device = self.get_device(dev, circuit)

        if device is None:
            return value

        value = float(device["vis"])

        return value

    def read_mb_registers(self, uart, dev_id, registers, register_type=None):
        """Read MODBUS register.

        Parameters
        ----------
        uart : int
            UART index.

        dev_id : int
            MODBUS ID.

        registers : array
            Registers IDs.

        register_type : str
            Registers types.

        Returns
        -------
        mixed
            State of the device.
        """

        return self._get_uart_registers(uart, dev_id, registers, register_type)

    def get_1w_devices(self):
        """Get 1W device from the list of all.

        Returns
        -------
        tuple
            1W devices.
        """

        return self._get_1w_devices()

#endregion
