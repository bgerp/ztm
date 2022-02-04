#!/bin/bash

# Zontromat - Zonal Electronic Automation

# Copyright (C) [2020] [POLYGONTeam Ltd.]

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# python -m pydeps ../Zontromat/main.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/main.svg --show-deps # > ../Zontromat/main.json
python -m pydeps ../Zontromat/plugins/ac/ac.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/ac/dep_graph.svg --show-deps # > ../Zontromat/plugins/ac/dep_graph.json
python -m pydeps ../Zontromat/plugins/air_chambers/air_chambers.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/air_chambers/dep_graph.svg --show-deps # > ../Zontromat/plugins/air_chambers/dep_graph.json
python -m pydeps ../Zontromat/plugins/alarm/alarm.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/alarm/dep_graph.svg --show-deps # > ../Zontromat/plugins/alarm/dep_graph.json
python -m pydeps ../Zontromat/plugins/blinds/blinds.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/blinds/dep_graph.svg --show-deps # > ../Zontromat/plugins/blinds/dep_graph.json
python -m pydeps ../Zontromat/plugins/ecc/ecc.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/ecc/dep_graph.svg --show-deps # > ../Zontromat/plugins/ecc/dep_graph.json
python -m pydeps ../Zontromat/plugins/ecd/ecd.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/ecd/dep_graph.svg --show-deps # > ../Zontromat/plugins/ecd/dep_graph.json
python -m pydeps ../Zontromat/plugins/echp/echp.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/echp/dep_graph.svg --show-deps # > ../Zontromat/plugins/echp/dep_graph.json
python -m pydeps ../Zontromat/plugins/envm/envm.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/envm/dep_graph.svg --show-deps # > ../Zontromat/plugins/envm/dep_graph.json
python -m pydeps ../Zontromat/plugins/hvac/hvac.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/hvac/dep_graph.svg --show-deps # > ../Zontromat/plugins/hvac/dep_graph.json
python -m pydeps ../Zontromat/plugins/light/light.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/light/dep_graph.svg --show-deps # > ../Zontromat/plugins/light/dep_graph.json
python -m pydeps ../Zontromat/plugins/monitoring/monitoring.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/monitoring/dep_graph.svg --show-deps # > ../Zontromat/plugins/monitoring/dep_graph.json
python -m pydeps ../Zontromat/plugins/stat/stat.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/stat/dep_graph.svg --show-deps # > ../Zontromat/plugins/stat/dep_graph.json
python -m pydeps ../Zontromat/plugins/sys/sys.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/sys/dep_graph.svg --show-deps # > ../Zontromat/plugins/sys/dep_graph.json
python -m pydeps ../Zontromat/plugins/template_plugin/template_plugin.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/template_plugin/dep_graph.svg --show-deps # > ../Zontromat/plugins/template_plugin/dep_graph.json
python -m pydeps ../Zontromat/plugins/vent/vent.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../Zontromat/plugins/vent/dep_graph.svg --show-deps # > ../Zontromat/plugins/vent/dep_graph.json

# Human readable format.
python ../Zontromat/export_registers.py --action w_md ../Zontromat/plugins/registers.md

# Human readable format.
python ../Zontromat/export_registers.py --action w_csv --path ../registers.csv

