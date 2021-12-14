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

import traceback
import xml.etree.ElementTree as ET

import requests

from utils.logger import get_logger

from controllers.base_controller import BaseController

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

class PiCons(BaseController):
    """This class is dedicated to transfer information from and to PiCons series."""

#region Attributes

    __logger = None
    """Logger"""

    __timeout = 5
    """Communication timeout."""

    __host = ""
    """Base URI."""

    __args = "/?RelayOutputs=all&DigitalInputs=all&CounterInputs=all&AnalogInputs=all&ElectronicScales=all"
    """Arguments for the GPIO."""

    __json_data = None
    """JSON data container."""

    __map = \
    {\
        "identification": {"vendor": "bao bao industries", "model": "zl101pcc"},\

        # LEDs
        "LED0": 0, "LED1": 1, "LED2": 2, "LED3": 3,

        # Digital Inputs
        "DI0": 0, "DI1": 1, "DI2": 2, "DI3": 3,
        "DI4": 4, "DI5": 5, "DI6": 6, "DI7": 7,
        "DI8": 8, "DI9": 9,

        # Digital Outputs
        "DO0": 0, "DO1": 1, "DO2": 2, "DO3": 3,
        "DO4": 4, "DO5": 5, "DO6": 6, "DO7": 7,
        "DO8": 8, "DO9": 9, "DO10": 10, "DO11": 11,

        # Relay Outputs
        "RO0": 0, "RO1": 1, "RO2": 2, "RO3": 3,
        "RO4": 4, "RO5": 5, "RO6": 6, "RO7": 7,
        "RO8": 8, "RO9": 9, "RO10": 10, "RO11": 11,

        # Analog Inputs
        "AI0": 0, "AI1": 1, "AI2": 2, "AI3": 3,
        "AI4": 4, "AI5": 5, "AI6": 6, "AI7": 7,

        # Analog Outputs
        "AO0": 0, "AO1": 1, "AO2": 2, "AO3": 3,
    }

#endregion

#region Properties

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
            Neuron last communication time.
        """

        return 1601280859

    @property
    def model(self):
        """Get device model.

        Returns
        -------
        str
            Neuron model.
        """

        return "X1-Black"

    @property
    def serial_number(self):
        """Get device serial number.

        Returns
        -------
        str
            Neuron serial number.
        """

        return 25

    @property
    def version(self):
        """Get device version.

        Returns
        -------
        str
            PiCons device version.
        """

        return self._get_field("ProtocolVersion")

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

    def __xml_to_dict(self, content):
        """XML to dictionary."""

        root = ET.fromstring(content)
        # root = tree.getroot()

        converted_data = dict()

        for child in root:

            if child.tag == "LastComTime":
                converted_data[child.tag] = child.text

            elif child.tag == "Model":
                converted_data[child.tag] = child.text

            elif child.tag == "SerialNumber":
                converted_data[child.tag] = child.text

            elif child.tag == "ProtocolVersion":
                converted_data[child.tag] = child.text

            elif child.tag == "Device":
                converted_data[child.tag] = child.text

            elif child.tag == "Entries":
                if not child.tag in converted_data:
                    converted_data[child.tag] = list()

                for entire in child:

                    if entire.tag == "item":
                        data_item = dict()

                        for attr in entire:

                            if attr.tag == "ID":
                                data_item[attr.tag] = int(attr.text)

                            else:
                                data_item[attr.tag] = attr.text

                        converted_data[child.tag].append(data_item)

            else:
                print("Tag: {}; Text: {}".format(child.tag, child.text))

        return converted_data

#endregion

#region Protected Methods

    def _update(self):
        """Make request to the device to update the data."""

        state = False

        # Call the Neuron.
        uri = self.__host + self.__args

        try:
            response = requests.get(uri, timeout=self.__timeout)

            if response.status_code == 200:

                # print(response.text)
                self.__json_data = self.__xml_to_dict(response.text)
                # print(self.__json_data)

                # Mark as successfull.
                state = True

            else:
                self.__logger.error("Controller answer with: {}".format(response.status_code))
                state = False

        except Exception:
            state = False
            self.__logger.error(traceback.format_exc())

        return state

    def _get_field(self, name):
        """Get field from the list of all.

        Parameters
        ----------
        name : str
            Field name

        Returns
        -------
        mixed
            Description of field values.
        """

        value = None

        if name in self.__json_data:
            value = self.__json_data[name]

        return value

    def _get_item(self, entries, idx):

        item = None

        for entre in entries:
            if entre["ID"] == idx:
                item = entre
                break

        return item

    def _set_relay(self, idx, value):
        """Turn the Relay state.

        Parameters
        ----------
        idx : str
            GPIO identifier.
        value : int, optional
            Value of the Relay [1, 0]

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = "Relay{}={}".format(idx+1, str(value))
        uri = self.__host + "/?" + circuit
        response = requests.get(uri, timeout=self.__timeout)
        json_data = self.__xml_to_dict(response.text)
        return json_data

    def _set_digital_output(self, idx, value):
        """Turn the DO state.

        Parameters
        ----------
        idx : str
            GPIO identifier.
        value : int, optional
            Value of the DO [1, 0].

        Returns
        -------
        mixed
            JSON response data.
        """

        circuit = "Relay{}={}".format(idx+1, str(value))
        uri = self.__host + "/?" + circuit
        response = requests.get(uri, timeout=self.__timeout)
        json_data = self.__xml_to_dict(response.text)
        return json_data

    def _reset_input_counter(self, idx):
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

        entries = self._get_field("Entries")

        item = self._get_item(entries, idx)

        return item

    def _get_counter(self, idx):
        """Read digital input counter.

        Parameters
        ----------
        idx : str
            Counter identifier.

        Returns
        -------
        mixed
            JSON response data.
        """

        entries = self._get_field("Entries")

        item = self._get_item(entries, idx)

        return item

    def _get_digital_input(self, idx):
        """Read digital input.

        Parameters
        ----------
        idx : str
            GPIO identifier.

        Returns
        -------
        mixed
            JSON response data.
        """

        entries = self._get_field("Entries")

        item = self._get_item(entries, idx)

        return item

    def _get_relay_outputs(self, idx):
        """Read relay outputs.

        Parameters
        ----------
        idx : str
            GPIO identifier.

        Returns
        -------
        mixed
            JSON response data.
        """

        entries = self._get_field("Entries")

        item = self._get_item(entries, idx)

        return item

    def _get_digital_outputs(self, idx):
        """Read digital outputs.

        Parameters
        ----------
        idx : str
            GPIO identifier.

        Returns
        -------
        mixed
            JSON response data.
        """

        entries = self._get_field("Entries")

        item = self._get_item(entries, idx)

        return item

    def _get_analog_in(self, idx):
        """Read analog inputs.

        Parameters
        ----------
        idx : str
            GPIO identifier.

        Returns
        -------
        mixed
            JSON response data.
        """

        entries = self._get_field("Entries")

        item = self._get_item(entries, idx)

        return item

#endregion

#region Static Methods

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

        l_pin = pin.replace("!", "")

        if not self.is_valid_gpio_type(l_pin):
            raise ValueError("Pin can not be None or empty string.")

        if not self.is_valid_gpio(l_pin):
            raise ValueError("Pin does not exists in pin map.")

        if self.is_off_gpio(l_pin):
            return state

        gpio_map = self.__map[l_pin]
        # if gpio_map["dev"] == "do":
        #     response = self._get_digital_output(gpio_map["id"])
        #     state = int(response["Value"])

        if gpio_map["dev"] == "relay":
            response = self._get_relay_outputs(gpio_map["id"])
            state = int(response["Value"])

        elif gpio_map["dev"] == "input":
            response = self._get_digital_input(gpio_map["id"])
            state = int(response["Value"])

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

        gpio_map = self.__map[l_pin]

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
            response = self._set_digital_output(gpio_map["id"], state)
        elif gpio_map["dev"] == "relay":
            response = self._set_relay(gpio_map["id"], state)

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

        gpio_map = self.__map[pin]

        response = self._get_counter(gpio_map)
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

        gpio_map = self.__map[pin]

        if gpio_map["dev"] == "ai":
            response = self._get_analog_in(gpio_map)

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

        gpio_map = self.__map[pin]

        response = self._reset_input_counter(gpio_map)

        return response

    def get_1w_devices(self):
        """Returns list of One Wire Device."""

        return []

#endregion
