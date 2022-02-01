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

python -m pydeps ../Zontromat/main.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/main.svg --show-deps > ../doc/main.json
python -m pydeps ../Zontromat/plugins/ac/ac.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/ac.svg --show-deps > ../doc/ac.json
python -m pydeps ../Zontromat/plugins/air_chambers/air_chambers.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/air_chambers.svg --show-deps > ../doc/air_chambers.json
python -m pydeps ../Zontromat/plugins/alarm/alarm.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/alarm.svg --show-deps > ../doc/alarm.json
python -m pydeps ../Zontromat/plugins/blinds/blinds.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/blinds.svg --show-deps > ../doc/blinds.json
python -m pydeps ../Zontromat/plugins/ecc/ecc.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/ecc.svg --show-deps > ../doc/ecc.json
python -m pydeps ../Zontromat/plugins/ecd/ecd.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/ecd.svg --show-deps > ../doc/ecd.json
python -m pydeps ../Zontromat/plugins/echp/echp.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/echp.svg --show-deps > ../doc/echp.json
python -m pydeps ../Zontromat/plugins/envm/envm.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/envm.svg --show-deps > ../doc/envm.json
python -m pydeps ../Zontromat/plugins/hvac/hvac.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/hvac.svg --show-deps > ../doc/hvac.json
python -m pydeps ../Zontromat/plugins/light/light.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/light.svg --show-deps > ../doc/light.json
python -m pydeps ../Zontromat/plugins/monitoring/monitoring.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/monitoring.svg --show-deps > ../doc/monitoring.json
python -m pydeps ../Zontromat/plugins/stat/stat.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/stat.svg --show-deps > ../doc/stat.json
python -m pydeps ../Zontromat/plugins/sys/sys.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/sys.svg --show-deps > ../doc/sys.json
python -m pydeps ../Zontromat/plugins/template_plugin/template_plugin.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/template_plugin.svg --show-deps > ../doc/template_plugin.json
python -m pydeps ../Zontromat/plugins/vent/vent.py --max-bacon 33 --cluster --max-cluster-size 10 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o ../doc/vent.svg --show-deps > ../doc/vent.json
