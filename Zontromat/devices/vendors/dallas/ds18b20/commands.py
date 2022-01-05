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

from enum import Enum

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

class Commands(Enum):
    """DS18B20 model.
    """

    FamilyCode = 0x28
    """DS18B20’s 1-Wire family code
    """

    #region ROM Commands

    SEARCH_ROM = 0xF0
    """SEARCH ROM [F0h]
    """

    READ_ROM = 0x33
    """READ ROM [33h]
    """

    MATCH_ROM = 0x55
    """MATCH ROM [55h]
    The match ROM command followed by a 64-bit ROM code sequence allows the bus master to address a
    specific slave device on a multidrop or single-drop bus. Only the slave that exactly matches the 64-bit
    ROM code sequence will respond to the function command issued by the master all other slaves on the
    bus will wait for a reset pulse.
    """

    SKIP_ROM = 0xCC
    """    SKIP ROM [CCh]
    The master can use this command to address all devices on the bus simultaneously without sending out
    any ROM code information. For example, the master can make all DS18B20s on the bus perform
    simultaneous temperature conversions by issuing a Skip ROM command followed by a Convert T [44h] command.
    """

    ALARM_SEARCH = 0xEC
    """ALARM SEARCH [ECh]
    """

    #endregion

    #region DS18B20 FUNCTION COMMANDS

    CONVERT_T = 0x44
    """CONVERT T [44h]
    This command initiates a single temperature conversion. Following the conversion, the resulting thermal
    data is stored in the 2-byte temperature register in the scratchpad memory and the DS18B20 returns to its
    low-power idle state.
    """

    WRITE_SCRATCHPAD = 0x4E
    """WRITE SCRATCHPAD [4Eh]
    """

    READ_SCRATCHPAD = 0xBE
    """READ SCRATCHPAD [BEh]
    This command allows the master to read the contents of the scratchpad. The data transfer starts with the
    least significant bit of byte 0 and continues through the scratchpad until the 9th byte (byte 8 – CRC) is
    read. The master may issue a reset to terminate reading at any time if only part of the scratchpad data is needed.
    """

    COPY_SCRATCHPAD = 0x48
    """COPY SCRATCHPAD [48h]
    """

    RECALL_E2 = 0xB8
    """RECALL E2 [B8h]
    """

    READ_POWER_SUPPLY = 0xB4
    """READ POWER SUPPLY [B4h]
    The master device issues this command followed by a read time slot to determine if any DS18B20s on the
    bus are using parasite power.During the read time slot, parasite powered DS18B20s will pull the bus
    low, and externally powered DS18B20s will let the bus remain high.
    """
