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

from data.registers import Registers

class RegisterHandler:
    """Register handler."""

#region Attributes

    __gpio_map = []
    """GPIO map"""

#endregion

#region Public Static Method

    @staticmethod
    def get_gpio(dev, circuit):
        """Get GPIO by Device  and Circuit."""

        gpio = None
        items = RegisterHandler.__gpio_map

        identification = None

        for item in items:
            if item == "identification":
                identification = items[item]
                break

        if identification is not None:

            if identification["vendor"] == "unipi":

                if dev == "led" or dev == "input":

                    circuit = circuit.replace("0", "")
                    index = circuit.split("_")
                    major_index = int(index[0])
                    minor_index = int(index[1])

                    for item in items:
                        if item != "identification":
                            if dev == items[item]["dev"] and major_index == items[item]["major_index"] and minor_index == items[item]["minor_index"]:
                                gpio = item

        return gpio

    @staticmethod
    def set_gpio_map(gpio_map):
        """Set GPIO map."""

        if gpio_map is None:
            return

        RegisterHandler.__gpio_map = gpio_map

    @staticmethod
    def update(request_body):

        inputs = Registers()

        registers = Registers.get_instance()

        # Access control
        inputs.add(registers.by_name("ac.door_closed_1.input"))
        inputs.add(registers.by_name("ac.door_closed_2.input"))
        # inputs.add(registers.by_name("ac.exit_button_1.input"))
        # inputs.add(registers.by_name("ac.exit_button_2.input"))
        inputs.add(registers.by_name("ac.pir_1.input"))
        inputs.add(registers.by_name("ac.pir_2.input"))
        inputs.add(registers.by_name("ac.window_closed_1.input"))
        inputs.add(registers.by_name("ac.window_closed_2.input"))

        # HVAC
        # inputs.add(registers.by_name("hvac.loop1.cnt.input"))
        # inputs.add(registers.by_name("hvac.loop2.cnt.input"))

        # Monitoring
        inputs.add(registers.by_name("monitoring.cw.input"))
        inputs.add(registers.by_name("monitoring.hw.input"))

        # System
        inputs.add(registers.by_name("sys.at.input"))
        # inputs.add(registers.by_name("sys.sl.output"))

        for device in request_body:

            gpio = RegisterHandler.get_gpio(device["dev"], device["circuit"])
            for input_reg in inputs:

                # Filter by type.
                if input_reg.value == gpio:
                    required_name = input_reg.name.replace("input", "state")
                    target_reg = registers.by_name(required_name)

                    # If register exists, apply value.
                    if target_reg is not None:
                        target_reg.value = device["value"]

#endregion
