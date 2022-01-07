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

# IT SHOULD BE STARTED FROM HERE!

cd ../

SUB='10.00/10'
all_py_files=$(find ./ -type f -name "*.py")

# echo $all_py_files

for py_file in $all_py_files
do
    cmd_line="python3 -m pylint $py_file"
    # echo $cmd_line

    result=$(${cmd_line})
    # echo "$result"


    # my_array=($(echo $result | tr "," "\r"))

    # for item in $my_array
    # do
    #     echo $item
    #     echo "test ====="
    # done

    # IFS=$'\n' read -ra my_array <<< "${result}"

    # echo "${#my_array[@]}"
    # echo "${my_array[0]}"

    # number=$(awk '{ sub(/.*rated at/, ""); sub(/previous.*/, ""); print }' <<< ${result})
    # echo -e ${number}

    if [[ "$result" != *"$SUB"* ]]; then
        # number=$(awk '{ sub(/.*rated at/, ""); sub(/previous.*/, ""); print }' <<< $result)
        # echo -e ${number}
        # cut_num=${number:1:5}
        # echo -e ${cut_num}
        # echo -e "${p}"
        echo "$result"
    fi


done

