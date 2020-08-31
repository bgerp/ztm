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

from data.register import Priority

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

def __csv_escape(value):

    result = value

    if isinstance(value, str):
        if "," in value:
            result = "\"" + value + "\""

    elif isinstance(value, list):
        result = "\"" + str(value) + "\""

    return result

def reg_to_json(registers):
    """JSON output"""

    bgerp_regs = registers.by_source(Priority.System)
    dict_regs = bgerp_regs.to_dict()
    text = json.dumps(dict_regs, indent=4, sort_keys=True)
    with open("registers_bgerp.json", "w") as file:
        file.write(text)

    ztm_regs = registers.by_source(Priority.Device)
    dict_regs = ztm_regs.to_dict()
    text = json.dumps(dict_regs, indent=4, sort_keys=True)
    with open("registers_ztm.json", "w") as file:
        file.write(text)

def reg_to_csv(registers):
    """CSV output"""

    bgerp_regs = registers.by_source(Priority.System)
    with open("registers_bgerp.csv", "w") as file:
        for register in bgerp_regs:
            file.write("{}\t{}\n".format(register.name, register.value))

    ztm_regs = registers.by_source(Priority.Device)
    with open("registers_ztm.csv", "w") as file:
        for register in ztm_regs:
            file.write("{}\t{}\n".format(register.name, register.value))

def reg_to_md(registers):
    """MD output"""

    bgerp_regs = registers.by_source(Priority.System)
    with open("registers_bgerp.md", "w") as file:

        # Header
        file.write("| Purpose | Register | Type | Value |\n")
        file.write("|----------|:-------------|:------|:------|\n")

        # Body
        for bgerp_reg in bgerp_regs:

            file.write("|  | {} | {} | {} |\n"\
                .format(bgerp_reg.name, bgerp_reg.data_type, bgerp_reg.value))

    ztm_regs = registers.by_source(Priority.Device)
    with open("registers_ztm.md", "w") as file:

        # Header
        file.write("| Purpose | Register | Type | Value |\n")
        file.write("|----------|:-------------|:------|:------|\n")

        # Body
        for ztm_reg in ztm_regs:

            file.write("|  | {} | {} | {} |\n"\
                .format(ztm_reg.name, ztm_reg.data_type, ztm_reg.value))

def reg_to_bgERP(registers):
    """Export registers"""

    with open("registers_bgerp.csv", "w") as file:

        for register in registers:

            data_type = "None"

            if register.value == "yes" or register.value == "no":
                data_type = "bool"

            else:
                data_type = register.data_type

            value = __csv_escape(register.value)
            description = __csv_escape(register.description)
            priority = str(register.priority).replace("Priority.", "").lower()
            reg_register = __csv_escape(register.range)

            line = "{},{},{},{},{},{},{}\n".\
                format(register.name, data_type, reg_register, register.plugin_name,\
                    priority, value, description)

            file.write(line)

        file.close()
