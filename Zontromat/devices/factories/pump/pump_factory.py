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

from devices.vendors.grundfos.magna1_80_100_f_360_1x230v_pn6.magna1_80_100_f_360_1x230v_pn6 import MAGNA1_80_100_F_360_1x230V_PN6
from devices.vendors.grundfos.magna3_40_150_f_q.magna3_40_150_f_q import Magna3_40_150_F_Q
from devices.vendors.grundfos.magna3_40_180_f_250_1x230v_pn6_10.magna3_40_180_f_250_1x230v_pn6_10 import MAGNA3_40_180_F_250_1x230V_PN6_10
from devices.vendors.grundfos.nbe_65_125_127s2af2abqqe.nbe_65_125_127s2af2abqqe import NBE_65_125_127S2AF2ABQQE
from devices.vendors.grundfos.tp_80_240_2_a_f_b_baqe_lx1_ie3.tp_80_240_2_a_f_b_baqe_lx1_ie3 import TP_80_240_2_A_F_B_BAQE_LX1_IE3
from devices.vendors.grundfos.tpe3_40_240_s_a_f_a_bqbe_hac_ie5.tpe3_40_240_s_a_f_a_bqbe_hac_ie5 import TPE3_40_240_S_A_F_A_BQBE_HAC_IE5
from devices.vendors.grundfos.tpe3_40_240_s_a_f_a_bqbe_hdc_ie5.tpe3_40_240_s_a_f_a_bqbe_hdc_ie5 import TPE3_40_240_S_A_F_A_BQBE_HDC_IE5
from devices.vendors.grundfos.tpe_100_240_2_s_a_f_a_baqemdb.tpe_100_240_2_s_a_f_a_baqemdb import TPE_100_240_2_S_A_F_A_BAQEMDB

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

class PumpFactory:
    """Pump factory calss
    """

    @staticmethod
    def create(**config):
        """Create pump device instace.
        """

        # The device.
        device = None

        # Name
        name = ""
        if "name" in config:
            name = config["name"]

        # Vendor
        vendor = None
        if "vendor" in config:
            vendor = config["vendor"]

        else:
            raise ValueError("No \"vendor\" argument has been passed.")

        # Model
        model = None
        if "model" in config:
            model = config["model"]

        else:
            raise ValueError("No \"model\" argument has been passed.")

        # Controller
        controller = None
        if "controller" in config:
            controller = config["controller"]

        else:
            raise ValueError("No \"controller\" argument has been passed.")

        # Grundfos / MAGNA1_80_100_F_360_1x230V_PN6 / 0
        if vendor == "Grundfos" and  model == "MAGNA1_80_100_F_360_1x230V_PN6":

            device = MAGNA1_80_100_F_360_1x230V_PN6(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / Magna3_40_150_F_Q / 0
        elif vendor == "Grundfos" and  model == "Magna3_40_150_F_Q":

            device = Magna3_40_150_F_Q(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / MAGNA3_40_180_F_250_1x230V_PN6_10 / 0
        elif vendor == "Grundfos" and  model == "MAGNA3_40_180_F_250_1x230V_PN6_10":

            device = MAGNA3_40_180_F_250_1x230V_PN6_10(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / NBE_65_125_127S2AF2ABQQE / 0
        elif vendor == "Grundfos" and  model == "NBE_65_125_127S2AF2ABQQE":

            device = NBE_65_125_127S2AF2ABQQE(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / TP_80_240_2_A_F_B_BAQE_LX1_IE3 / 0
        elif vendor == "Grundfos" and  model == "TP_80_240_2_A_F_B_BAQE_LX1_IE3":

            device = TP_80_240_2_A_F_B_BAQE_LX1_IE3(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / TPE_100_240_2_S_A_F_A_BAQEMDB / 0
        elif vendor == "Grundfos" and  model == "TPE_100_240_2_S_A_F_A_BAQEMDB":

            device = TPE_100_240_2_S_A_F_A_BAQEMDB(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / TPE3_40_240_S_A_F_A_BQBE_HAC_IE5 / 0
        elif vendor == "Grundfos" and  model == "TPE3_40_240_S_A_F_A_BQBE_HAC_IE5":

            device = TPE3_40_240_S_A_F_A_BQBE_HAC_IE5(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        # Grundfos / TPE3_40_240_S_A_F_A_BQBE_HDC_IE5 / 0
        elif vendor == "Grundfos" and  model == "TPE3_40_240_S_A_F_A_BQBE_HDC_IE5":

            device = TPE3_40_240_S_A_F_A_BQBE_HDC_IE5(
                name=name,
                controller=controller,
                unit=config["options"]['mb_id']
            )

        else:
            raise NotImplementedError("The {} and {}, is not supported.".format(vendor, model))

        # Return the instance.
        return device
