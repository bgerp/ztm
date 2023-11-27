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
import json

from data.register import Register

from utils.logger import get_logger

from services.global_error_handler.global_error_handler import GlobalErrorHandler

from data.register import Scope

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2019, POLYGON Team Ltd."
"""Copyrighter
@see http://polygonteam.com/"""

__credits__ = ["Angel Boyarov"]
"""Credits"""

__license__ = "MIT"
"""License
@see https://opensource.org/licenses/MIT"""

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

class Registers(list):
    """Registers"""

#region Attributes

    __logger = None
    """Logger
    """

#endregion

#region Constructor

    def __init__(self):
        """Constructor
        """

        super().__init__()

        # Create logger.
        self.__logger = get_logger(__name__)

#endregion

#region Private Methods

    def __preprocess_value(self, value):

        out_value = None

        if isinstance(value, str):

            if value == "false":
                out_value = False

            elif value == "true":
                out_value = True

            elif value.startswith("[") and value.endswith("]"):
                out_value = json.loads(value)

            elif value.startswith("{") and value.endswith("}"):
                out_value = json.loads(value)

            else:
                out_value = value

        else:
            out_value = value

        return out_value

#endregion

#region Public Methods

    def update(self, registers):
        """Update registers content.

        Args:
            registers (dict): Dictionary of registers.

        Raises:
            ValueError: None register values.
        """

        if registers is None:
            raise ValueError("Registers can not be None.")

        if len(registers) <= 0:
            return

        # Go through registers.
        for name in registers:

            register = None

            # Update registers.
            if name in self.names():
                register = self.by_name(name)
                register.value = self.__preprocess_value(registers[name])

            # Add missing register.
            else:
                register = Register(name)
                register.value = self.__preprocess_value(registers[name])
                self.append(register)

                GlobalErrorHandler.log_unexpected_register(self.__logger, register)

    def exists(self, name: str):
        """Update registers content.

        Args:
            name (str): Name of the register.

        Returns:
            bool: Exists or not.
        """

        result = False

        for register in self:
            if name in register.name:
                result = True
                break

        if not result:
            GlobalErrorHandler.log_register_not_found(self.__logger, name)

        return result

    def by_ts(self, ts):
        """Get registers with specified scope.

        Args:
            ts (float): Timestamp

        Returns:
            list: Registers specified time.
        """

        result = Registers()

        for register in self:
            if ts < register.ts:
                result.append(register)

        return result

    def new_then(self, seconds):
        """Get registers newer then specific time from time of calling.

        Args:
            seconds (float): seconds

        Returns:
            list: Registers newer than specific time.
        """

        result = Registers()

        time_now = time.time()

        for register in self:

            delta_t = time_now - register.ts
            if delta_t < seconds:
                result.append(register)

        return result

    def by_scope(self, scope):
        """Get registers with specified scope.

        Args:
            scope (Scope): Scope of action.

        Returns:
            list: Registers with scope.
        """

        result = Registers()

        for register in self:
            if (scope.value & register.scope.value) > 0:
                result.append(register)

        return result

    def by_key(self, key: str):
        """Get registers with specified key in name.

        Args:
            key (str): Key in name.

        Returns:
            list: Registers with key names.
        """

        result = Registers()

        for register in self:
            if key in register.name:
                result.append(register)

        return result

    def by_name(self, name: str):
        """Returns register with specified name.

        Args:
            name (str): Name of the register.

        Returns:
            list: Registers with name.
        """

        if name is None:
            raise ValueError("Name can not be None.")

        if name == "":
            raise ValueError("Name can not be empty string.")

        result = None

        for register in self:
            if name == register.name:
                result = register
                break

        return result

    def by_names(self, names: list):
        """Returns registers with specified name.

        Args:
            names (list): Names of the registers.

        Returns:
            list: Registers with names.
        """

        filtered = Registers()

        for name in names:
            selected = self.by_name(name)

            if selected is not None:
                filtered.append(selected)

        return filtered

    def names(self):
        """Get registers names.

        Returns:
            list: Array of names.
        """

        result = []

        for register in self:
            result.append(register.name)

        return result

    def to_dict(self):
        """Converts array in to dictionary.
        Consisted of name and value as (key and value).

        Returns:
            dict: Dictionary of registers.
        """

        result = {}

        for register in self:

            # Handle list and dict types.
            if register.data_type == "json":

                if isinstance(register.value, list):
                    pass

                if isinstance(register.value, dict):
                    temp_list = []
                    for item in register.value:

                        temp_dict = {}
                        for sub_item in item:
                            temp_dict[sub_item.name] = sub_item.value

                        temp_list.append(temp_dict)

                    result[register.name] = json.dumps(temp_list)

            # No need special handling.
            else:
                result[register.name] = register.value

        return result

    def get_json(self):
        """Converts array to JSON.

        Returns:
            dict: Dictionary of registers.
        """

        result = []

        for register in self:

            # Handle list and dict types.
            result.append(register.get_json())

        return result

    def get_group(self, name: str):
        """Get registerr with specified group name.

        Args:
            name (str): Name of the registers.

        Returns:
            Register: Registers with name.
        """

        result = []

        for register in self:
            if register.name.startswith("{}.".format(name)):
                result.append(register)

        return result

    def get_groups(self):
        """Return the groups.

        Returns:
            list: Names of the registers in list.
        """

        base_names = []
        for register in self:
            if not register.base_name in base_names:
                base_names.append(register.base_name)

        return base_names

    def keys(self):
        """Return keys.

        Returns:
            list: Names of the registers in list.
        """

        registers_keys = []
        for register in self:
            registers_keys.append(register.name)

        return registers_keys

    def write(self, name: str, value):
        """Write in specific register.

        Args:
            name (str): The name.
            value (Any): The value.

        Returns:
            bool: Execution status.
        """

        status = False

        target_register = self.by_name(name)
        if target_register is not None:
            target_register.value = value
            status = True

        return status

    def add_callback(self, name: str, cb, **kwargs):
        """[summary]

        Args:
            name (str): Name of the register.
            cb (function): Function name.
        """

        register = self.by_name(name)
        if register is not None:
            register.update_handlers = cb
            if "update" in kwargs:
                register.update()

#endregion

#region Static Methods

    @staticmethod
    def __csv_escape(value):

        result = value

        if isinstance(value, str):
            if "," in value:
                result = "\"" + value + "\""

        elif isinstance(value, list):
            result = "\"" + str(value) + "\""

        elif isinstance(value, dict):
            result = "\"" + str(value) + "\""
            result = result.replace("\'", "\"")

        return result

    @staticmethod
    def __to_scope(scope):

        p_scope = scope.lower()
        out_scope = Scope.NONE

        if p_scope == "global":
            out_scope = Scope.Global

        elif p_scope == "device":
            out_scope = Scope.Device

        elif p_scope == "system":
            out_scope = Scope.System

        elif p_scope == "both":
            out_scope = Scope.Both

        return out_scope

    @staticmethod
    def __to_value(data_type, value):

        out_value = None

        # bool
        if data_type == "bool":
            value_type = type(value)

            if value_type == bool:
                out_value = value

            else:
                if value == "false":
                    out_value = False

                if value == "true":
                    out_value = True

        # int
        elif data_type == "int":
            out_value = int(value)

        # float
        elif data_type == "float":
            out_value = float(value)

        # json
        elif data_type == "json":
            value_type = type(value)

            if value_type == list:
                out_value = value

            elif value_type == dict:
                out_value = value

            elif value_type == str:

                # Remove first "
                if value.startswith("\""):
                    value = value[1:]

                # Remove last "
                if value.endswith("\""):
                    value = value[:-1]

                # Convert single quotes to double.
                value = value.replace("\'", "\"") 

                # Converts to JSON.
                value = json.loads(value)

                out_value = value

            else:
                raise TypeError("Unsupported data type: {}".format(value_type))

        else:
            out_value = value

        return out_value

    @staticmethod
    def __from_value(data_type, value):

        our_value = Registers.__csv_escape(value)

        if data_type == "bool":
            if our_value:
                our_value = "true"
            else:
                our_value = "false"

        elif data_type == "str":
            if "," in value:
                our_value = "\"" + value + "\""

        elif data_type == "json":
            our_value = json.dumps(value)

        return our_value

    @staticmethod
    def to_csv(registers, file_path="registers.csv"):

        import csv

        with open(file_path, "w", newline="", encoding='utf-8') as csv_file:

            fieldnames = ["name", "type", "range", "plugin", "scope", "default", "description"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=",", quoting=2) #/"" , quoting=2, escapechar="\""
            writer.writeheader()

            for register in registers:

                value = Registers.__from_value(register.data_type, register.value)
                reg_range = Registers.__csv_escape(register.range)
                scope = str(register.scope).replace("Scope.", "").lower()
                description = Registers.__csv_escape(register.description)

                writer.writerow({"name": register.name,\
                                "type": register.data_type,\
                                "range": reg_range,\
                                "plugin": register.plugin_name,\
                                "scope": scope,\
                                "default": value,\
                                "description": description,\
                                })

            csv_file.close()

    @staticmethod
    def from_csv(file_path="registers.csv"):
        """Load registers from CSV"""

        registers = Registers()

        import csv

        with open(file_path, newline="") as csv_file:

            rows = csv.DictReader(csv_file, delimiter=",", quoting=2)
            for row in rows:
                register = Register(row["name"])
                register.range = row["range"]
                register.plugin_name = row["plugin"]
                register.scope = Registers.__to_scope(row["scope"])
                register.value = Registers.__to_value(row["type"], row["default"])
                register.description = row["description"]
                
                registers.append(register)

        return registers

    @staticmethod
    def to_json(registers, file_path="registers.json"):
        """JSON output"""

        dict_regs = registers.get_json()
        text = json.dumps(dict_regs, indent=4, sort_keys=True)

        with open(file_path, "w") as json_file:
            json_file.write(text)
            json_file.close()

    @staticmethod
    def from_json(file_path="registers.json"):

        registers = Registers()

        with open(file_path, newline="") as json_file:

            rows = json.load(json_file)
            for row in rows:

                register = Register(row["name"])
                register.description = row["description"]
                register.range = row["range"]
                register.plugin_name = row["plugin"]
                register.scope = Registers.__to_scope(row["scope"])
                register.value = Registers.__to_value(row["type"], row["default"])

                registers.append(register)

        return registers

    @staticmethod
    def to_md(registers, file_path="registers.md"):
        
        # Clear the tables.
        md_tables = ""

        # Add content.
        groups = registers.get_groups()
        for group in groups:

            registers_group = registers.get_group(group)

            # Clear the table.
            md_table = ""

            # Header
            md_table += "\n\n\n## <a name='{}'>{}</a> Registers\n\n".format(registers_group[0].plugin_name.replace(" ", ""), registers_group[0].plugin_name)

            # Global
            md_table += " - **Global**" + 2*"\n"
            md_table += "| Purpose | Register | Type | Value |\n"
            md_table += "|----------|:-------------|:------|:------|\n"
            for reg in registers_group:
                if reg.scope == Scope.Global:
                    md_table += "| {} | {} | {} | {} |\n".format(reg.description, reg.name, reg.data_type, reg.value)
            md_table += "\n" 

            # System
            md_table += " - **System**" + 2*"\n"
            md_table += "| Purpose | Register | Type | Value |\n"
            md_table += "|----------|:-------------|:------|:------|\n"
            for reg in registers_group:
                if reg.scope == Scope.System:
                    md_table += "| {} | {} | {} | {} |\n".format(reg.description, reg.name, reg.data_type, reg.value)
            md_table += "\n"

            # Device
            md_table += " - **Device**" + 2*"\n"
            md_table += "| Purpose | Register | Type | Value |\n"
            md_table += "|----------|:-------------|:------|:------|\n"
            for reg in registers_group:
                if reg.scope == Scope.Device:
                    md_table += "| {} | {} | {} | {} |\n".format(reg.description, reg.name, reg.data_type, reg.value)
            md_table += "\n" 

            # Both
            md_table += " - **Both**" + 2*"\n"
            md_table += "| Purpose | Register | Type | Value |\n"
            md_table += "|----------|:-------------|:------|:------|\n"
            for reg in registers_group:
                if reg.scope == Scope.Both:
                    md_table += "| {} | {} | {} | {} |\n".format(reg.description, reg.name, reg.data_type, reg.value)
            md_table += "\n" 

            # Footer
            md_table += "* * *"

            # Add the table.
            md_tables += md_table

        with open(file_path, "w") as md_file:
            md_file.write(md_tables)
            md_file.close()

#endregion
