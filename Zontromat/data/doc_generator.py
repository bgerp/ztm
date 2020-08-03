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

from data.register import Source
from data.registers import Registers

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

def __get_type(inst):

    str_type = ""

    if isinstance(inst, str):
        str_type = "str"

    elif isinstance(inst, int):
        str_type = "int"

    elif isinstance(inst, float):
        str_type = "float/int"

    elif isinstance(inst, bool):
        str_type = "bool"

    elif isinstance(inst, list):
        str_type = "json"

    return str_type

def reg_to_json(registers):
    """JSON output"""

    bgerp_regs = registers.by_source(Source.bgERP)
    dict_regs = bgerp_regs.to_dict()
    text = json.dumps(dict_regs, indent=4, sort_keys=True)
    with open("registers_bgerp.json", "w") as f:
        f.write(text)

    ztm_regs = registers.by_source(Source.Zontromat)
    dict_regs = ztm_regs.to_dict()
    text = json.dumps(dict_regs, indent=4, sort_keys=True)
    with open("registers_ztm.json", "w") as f:
        f.write(text)

def reg_to_csv(registers):
    """CSV output"""

    bgerp_regs = registers.by_source(Source.bgERP)
    with open("registers_bgerp.csv", "w") as f:
        for register in bgerp_regs:
            f.write("{}\t{}\n".format(register.name, register.value))

    ztm_regs = registers.by_source(Source.Zontromat)
    with open("registers_ztm.csv", "w") as f:
        for register in ztm_regs:
            f.write("{}\t{}\n".format(register.name, register.value))

def reg_to_md(registers):
    """MD output"""

    bgerp_regs = registers.by_source(Source.bgERP)
    with open("registers_bgerp.md", "w") as f:

        # Header
        f.write("| Purpose | Register | Type | Value |\n")
        f.write("|----------|:-------------|:------|:------|\n")

        # Body
        for bgerp_register in bgerp_regs:

            str_type = __get_type(bgerp_register.value)

            f.write("|  | {} | {} | {} |\n"\
                .format(bgerp_register.name, str_type, bgerp_register.value))

    ztm_regs = registers.by_source(Source.Zontromat)
    with open("registers_ztm.md", "w") as f:

        # Header
        f.write("| Purpose | Register | Type | Value |\n")
        f.write("|----------|:-------------|:------|:------|\n")

        # Body
        for ztm_register in ztm_regs:

            str_type = __get_type(ztm_register.value)

            f.write("|  | {} | {} | {} |\n"\
                .format(ztm_register.name, str_type, ztm_register.value))
