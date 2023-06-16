


## <a name='AccessControl'>Access Control</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Plugin enabled | ac.enabled | bool | False |
| Allowed attendees | ac.allowed_attendees | json | [] |
| Number of security zones | ac.zones_count | int | 2 |
| Nearby attendees | ac.nearby_attendees | json | [] |
| Card reader enabled | ac.entry_reader_1.enabled | json | {} |
| Card reader enabled | ac.exit_reader_1.enabled | json | {} |
| Exit button 1 input | ac.exit_button_1.input | str | off |
| Lock mechanism output | ac.lock_mechanism_1.output | str | off |
| Lock mechanism time to open [s] | ac.time_to_open_1 | int | 3 |
| Door closed input | ac.door_closed_1.input | str | off |
| Card reader settings | ac.entry_reader_2.enabled | json | {} |
| Card reader settings | ac.exit_reader_2.enabled | json | {} |
| Exit button 2 input | ac.exit_button_2.input | str | off |
| Lock 2 mechanism output | ac.lock_mechanism_2.output | str | off |
| Lock 2 mechanism time to open | ac.time_to_open_2 | int | 3 |
| Door 2 closed input | ac.door_closed_2.input | str | off |
| PIR 1 sensor input | ac.pir_1.input | str | off |
| PIR 2 sensor input | ac.pir_2.input | str | off |
| Window 1 closed input | ac.window_closed_1.input | str | off |
| Window 2 closed input | ac.window_closed_2.input | str | off |
| Door window blind 1 output | ac.door_window_blind_1.output | str | off |
| Door window blind 2 output | ac.door_window_blind_2.output | str | off |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Last update attendee | ac.last_update_attendees | json | [] |
| Next attendance | ac.next_attendance | float | 0.0 |
| Door closed input state | ac.door_closed_1.state | bool | False |
| Door 2 closed input state | ac.door_closed_2.state | bool | False |
| PIR 1 sensor input state | ac.pir_1.state | bool | False |
| PIR 2 sensor input state | ac.pir_2.state | bool | False |
| Window 1 closed input state | ac.window_closed_1.state | bool | False |
| Window 2 closed input state | ac.window_closed_2.state | bool | False |
| Door window blind 1 value | ac.door_window_blind_1.value | bool | False |
| Door window blind 2 value | ac.door_window_blind_2.value | bool | False |
| Zone occupied flag | ac.zone_1_occupied | bool | False |
| Zone occupied flag | ac.zone_2_occupied | bool | False |

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='Blinds'>Blinds</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Window 1 blinds mechanism | blinds.blind_1.mechanism | json | {'vendor': 'Yihao', 'model': 'BlindsV2', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'feedback': 'off', 'feedback_tresh': 0.093, 'min': 0, 'max': 180, 'deg_per_sec': 10.0, 'uart': 0, 'mb_id': 11}} |
| Object height [m]. | blinds.blind_1.object_height | float | 2.0 |
| Sun spot limit [m]. | blinds.blind_1.sunspot_limit | float | 1.0 |
| Number of blind controllers | blinds.count | int | 1 |
| Plugin enabled | blinds.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Position [deg] | blinds.blind_1.position | float | 0.0 |

* * *


## <a name='Monitoring'>Monitoring</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Cold water flow meter | monitoring.cw.flowmeter_settings | json | {'vendor': 'mainone', 'model': 'flowmeter_dn20', 'options': {'uart': 1, 'mb_id': 3}} |
| Hot water input flow meter | monitoring.hw.flowmeter_settings | json | {'vendor': 'mainone', 'model': 'flowmeter_dn20', 'options': {'uart': 1, 'mb_id': 3}} |
| Power analyser settings | monitoring.pa.settings | json | {'vendor': 'Eastron', 'model': 'SDM630', 'options': {'uart': 0, 'mb_id': 2}} |
| Plugin enabled | monitoring.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Cold water liters | monitoring.cw.value | float | 0.0 |
| Cold water leaked liters | monitoring.cw.leak | float | 1.0 |
| Hot water liters | monitoring.hw.value | float | 0.0 |
| Hot water leaked liters | monitoring.hw.leak | float | 1.0 |
| Power analyser measurements | monitoring.pa.measurements | json | [] |
| Power analyser measuring demand | monitoring.pa.demand_time | float | 3600.0 |

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='Environment'>Environment</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Is empty time out [s] | envm.is_empty_timeout | int | 3600 |
| Actual outside temperature [C] | envm.temp.actual | float | 20.0 |
| Actual outside temperature for 6 hours [C] | envm.temp.a6 | float | 30.0 |
| Minimum outside temperature for 24 hours [C] | envm.temp.min24 | float | 20.0 |
| Maximum outside temperature for 24 hours [C] | envm.temp.max24 | float | 36.0 |
| Actual outside relative humidity [%] | envm.rh | float | 60.0 |
| Actual wind [m/sec] | envm.wind.actual | float | 3.0 |
| Maximum wind for 12 hours [m/sec] | envm.wind.max12 | float | 6.0 |
| Outside light [lux] | envm.light | float | 1000.0 |
| Energy mode of the building | envm.energy | int | 0 |
| Emergency index for the fire. | envm.flag_fire | int | 0 |
| Emergency index for the storm. | envm.flag_storm | int | 0 |
| Emergency index for the earthquake. | envm.flag_earthquake | int | 0 |
| Emergency index for the gassing. | envm.flag_gassing | int | 0 |
| Emergency index for the flooding. | envm.flag_flooding | int | 0 |
| Emergency index for the blocking. | envm.flag_blocked | int | 0 |
| Enable software calculation of the sun position | envm.sunpos.enabled | bool | False |
| Latitude of the target building. | envm.building.location.lat | float | 43.07779 |
| Longitude of the target building. | envm.building.location.lon | float | 25.59549 |
| Longitude of the target building. | envm.building.location.elv | int | 210 |
| Longitude of the target building. | envm.building.location.time_zone | int | 2 |
| Plugin enabled | envm.enabled | bool | False |
| Sun azimuth value | envm.sun.azimuth | float | 0.0 |
| Sun elevation value | envm.sun.elevation | float | 0.0 |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Is empty flag | envm.is_empty | bool | True |

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='HVAC'>HVAC</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Plugin enabled | hvac.enabled | bool | False |
| Count of the HVAC zones. | hvac.zones_count | int | 1 |
| Air temperature sensor center settings | hvac.air_temp_cent_1.settings | str | off |
| Air temperature sensor center value | hvac.air_temp_cent_1.value | float | 0.0 |
| Air temperature sensor lower settings | hvac.air_temp_lower_1.settings | json | {'vendor': 'Donkger', 'model': 'XY-MD02', 'options': {'uart': 0, 'mb_id': 5}} |
| Air temperature sensor lower value | hvac.air_temp_lower_1.value | float | 0.0 |
| Air temperature sensor upper settings | hvac.air_temp_upper_1.settings | json | {'vendor': 'Donkger', 'model': 'XY-MD02', 'options': {'uart': 0, 'mb_id': 4}} |
| Air temperature sensor upper value | hvac.air_temp_upper_1.value | float | 0.0 |
| Convector settings | hvac.convector_1.settings | json | {'vendor': 'Silpa', 'model': 'Klimafan', 'options': {'stage1': 'U0:ID6:FC16:R0:RO0', 'stage2': 'U0:ID6:FC16:R0:RO1', 'stage3': 'U0:ID6:FC16:R0:RO2'}} |
| Loop 1 water flow meter signal input | hvac.loop1_1.flowmeter.settings | json | {'vendor': 'mainone', 'model': 'flowmeter_dn20', 'options': {'uart': 1, 'mb_id': 3}} |
| Loop 1 temperature sensor settings | hvac.loop1_1.temp.settings | json | {'vendor': 'mainone', 'model': 'inlet_temp', 'options': {'uart': 1, 'mb_id': 3}} |
| Loop 1 temperature sensor value | hvac.loop1_1.temp.value | float | 0.0 |
| Loop 1 temperature down limit | hvac.loop1_1.temp.down_limit | int | 15 |
| Loop 1 valve settings | hvac.loop1_1.valve.settings | json | {'vendor': 'Tonhe', 'model': 'a20t20b2c', 'options': {'output': 'RO0'}} |
| Loop 2 water flow meter ticks per liter scale | hvac.loop2_1.flowmeter.settings | json | {'vendor': 'mainone', 'model': 'flowmeter_dn20', 'options': {'uart': 1, 'mb_id': 3}} |
| Loop 2 temperature sensor settings | hvac.loop2_1.temp.settings | json | {'vendor': 'mainone', 'model': 'inlet_temp', 'options': {'uart': 1, 'mb_id': 3}} |
| Loop 1 temperature sensor value | hvac.loop2_1.temp.value | float | 0.0 |
| Loop 2 valve settings | hvac.loop2_1.valve.settings | json | {'vendor': 'Tonhe', 'model': 'a20t20b2c', 'options': {'output': 'RO1'}} |
| Measuring delta time | hvac.delta_time_1 | float | 5.0 |
| Goal of the building temperature | hvac.goal_building_temp | float | 20.0 |
| Actual temperature | hvac.temp_1.actual | float | 0.0 |
| Maximum achievable | hvac.temp_1.max | float | 30.0 |
| Minimum achievable | hvac.temp_1.min | float | 20.0 |
| Thermal force limit | hvac.thermal_force_limit_1 | float | 100.0 |
| Thermal mode | hvac.thermal_mode_1 | int | 2 |
| Update rate of the plugin [s] | hvac.update_rate_1 | float | 5.0 |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Adjust temperature | hvac.temp_1.adjust | float | 0.0 |

* * *


## <a name='Light'>Light</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Minimum limit | light.min | float | 800.0 |
| Maximum limit | light.max | float | 10000.0 |
| Analog output 1. U1:ID2:R0:AO2 | light.v1.output | str | off |
| Analog output 2. U1:ID2:R0:AO3 | light.v2.output | str | off |
| Hallway lighting digital output. U1:ID2:R0:DO3 | light.hallway_lighting.output | str | off |
| Hallway lighting wait time. | light.hallway_lighting.time | float | 60.0 |
| Sensor settings | light.sensor.settings | json | {'vendor': 'PT', 'model': 'light_sensor', 'options': {'input': 'AI2'}} |
| Error gain | light.error_gain | float | 0.01 |
| Plugin enabled | light.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Target illumination | light.target_illum | float | 0.0 |

* * *


## <a name='System'>System</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Status LED | sys.sl.output | str | LED0 |
| Blink time | sys.sl.blink_time | float | 1.0 |
| Anti tamper | sys.at.input | str | off |
| Clear messages | sys.col.clear_errors | int | 0 |
| Plugin enabled | sys.enabled | bool | False |
| Enable info messages | sys.col.info_message.enable | bool | True |
| Enable warning messages | sys.col.warning_message.enable | bool | True |
| Enable error messages | sys.col.error_message.enable | bool | True |
| Target software version | sys.software.target_version | json | {'repo': 'http://github.com/bgerp/ztm/', 'branch': 'master', 'commit': '3462828'} |
| Current software version. | sys.software.current_version | json | {'repo': 'http://github.com/bgerp/ztm/', 'branch': 'master', 'commit': 'e0c1dda'} |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Last update cycle error | sys.last_update_errs | json | [] |
| Current consumed RAM | sys.ram.current | int | 0 |
| Peek of consumed RAM | sys.ram.peak | int | 0 |
| Application time cycle | sys.time.usage | float | 0.0 |
| OS boot time. | sys.time.boot | float | 0.0 |
| OS uptime. | sys.time.uptime | float | 0.0 |
| Application startup time. | sys.time.startup | float | 0.0 |
| Total disc space | sys.disc.total | int | 0 |
| Used disc space | sys.disc.used | int | 0 |
| Free disc space | sys.disc.free | int | 0 |
| Anti tampering state | sys.at.state | bool | False |
| Collision info message | sys.col.info_message | json | {} |
| Collision warning message | sys.col.warning_message | json | {} |
| Collision error message | sys.col.error_message | json | {} |

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='EnergyCenterCommon'>Energy Center Common</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Plugin enabled | ecc.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='ECD'>ECD</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| ECD / Foyer Floor Heating Settings | ecd.underfloor_heating_foyer.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Foyer Floor Heating Position | ecd.underfloor_heating_foyer.valve.position | float | 0.0 |
| ECD / Foyer Floor Heating Calibration | ecd.underfloor_heating_foyer.valve.calibrate | bool | False |
| ECD / Underfloor Heating Trestle | ecd.underfloor_heating_trestle.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Underfloor Heating Trestle Position | ecd.underfloor_heating_trestle.valve.position | float | 0.0 |
| ECD / Underfloor Heating Trestle Calibration | ecd.underfloor_heating_trestle.valve.calibration | bool | False |
| ECD / Underfloor Heating Pool | ecd.underfloor_heating_pool.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Underfloor Heating Pool Position | ecd.underfloor_heating_pool.valve.position | float | 0.0 |
| ECD / Underfloor Heating Pool Calibration | ecd.underfloor_heating_pool.valve.calibration | bool | False |
| ECD / Air Cooling Valve Settings | ecd.air_cooling.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Air Cooling Valve Position | ecd.air_cooling.valve.position | float | 0.0 |
| ECD / Air Cooling Valve Calibration | ecd.air_cooling.valve.calibration | bool | False |
| ECD / Ground Drilling Valve | ecd.ground_drill.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Ground Drill Valve Position | ecd.ground_drill.valve.position | float | 0.0 |
| ECD / Ground Drill Valve Calibration | ecd.ground_drill.valve.calibration | bool | False |
| ECD / Generators Cooling Valve / Settings | ecd.generators_cooling.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Generators Cooling Valve / Position | ecd.generators_cooling.valve.position | float | 0.0 |
| ECD / Generators Cooling Valve Calibration | ecd.generators_cooling.valve.calibration | bool | False |
| ECD / Short Green/Purple Valve Settings | ecd.short_green_purple.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Short Green/Purple Valve Position | ecd.short_green_purple.valve.position | float | 0.0 |
| ECD / Generators Cooling Valve Calibration | ecd.short_green_purple.valve.calibration | bool | False |
| ECD / Underfloor West Bypass Valve Settings | ecd.underfloor_west_bypass.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Underfloor West Bypass Valve Position | ecd.underfloor_west_bypass.valve.position | float | 0.0 |
| ECD / Underfloor West Bypass Valve Calibration | ecd.underfloor_west_bypass.valve.calibration | bool | False |
| ECD / Underfloor East Bypass Valve Settings | ecd.underfloor_east_bypass.valve.enabled | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / Underfloor East Bypass Valve Position | ecd.underfloor_east_bypass.valve.position | float | 0.0 |
| ECD / Underfloor East Bypass Valve Calibration | ecd.underfloor_east_bypass.valve.calibration | bool | False |
| ECD / VCG / Pool Heating | ecd.vcg_pool_heating.valve | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Pool Heating | ecd.vcg_pool_heating.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Pool Heating | ecd.vcg_pool_heating.enabled | bool | True |
| ECD / VCG / Pool Cooling In | ecd.vcg_tva_pool.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Pool Cooling In | ecd.vcg_tva_pool.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Pool Heating In | ecd.vcg_tva_pool.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Pool Heating Out | ecd.vcg_tva_pool.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Pump | ecd.vcg_tva_pool.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Enable | ecd.vcg_tva_pool.enabled | bool | True |
| ECD / VCG / Convectors East Cooling In | ecd.convectors_east.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors East Cooling Out | ecd.convectors_east.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors East Hot In | ecd.convectors_east.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors East Hot Out | ecd.convectors_east.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors East Pump | ecd.convectors_east.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Convectors East Enable | ecd.convectors_east.enabled | bool | True |
| ECD / VCG / Floor East Cooling In | ecd.underfloor_east.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor East Cooling Out | ecd.underfloor_east.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor East Hot In | ecd.underfloor_east.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor East Hot Out | ecd.underfloor_east.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor East Pump | ecd.underfloor_east.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Floor East Enable | ecd.underfloor_east.enabled | bool | True |
| ECD / VCG / Convectors West Cooling In | ecd.convectors_west.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors West Cooling Out | ecd.convectors_west.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors West Hot In | ecd.convectors_west.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors West Hot Out | ecd.convectors_west.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors West Pump | ecd.convectors_west.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Convectors West Enable | ecd.convectors_west.enabled | bool | True |
| ECD / VCG / TVA Roof Floor In | ecd.tva_roof_floor.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Roof Floor Out | ecd.tva_roof_floor.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Roof Floor In | ecd.tva_roof_floor.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Roof Floor Out | ecd.tva_roof_floor.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Roof Floor | ecd.tva_roof_floor.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / TVA Roof Floor | ecd.tva_roof_floor.enabled | bool | True |
| ECD / VCG / TVA Fitness In | ecd.tva_fitness.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Fitness Out | ecd.tva_fitness.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Fitness In | ecd.tva_fitness.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Fitness Out | ecd.tva_fitness.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Fitness | ecd.tva_fitness.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / TVA Fitness | ecd.tva_fitness.enabled | bool | True |
| ECD / VCG / Floor West Cooling In | ecd.floor_west.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor West Cooling Out | ecd.floor_west.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor West Hot In | ecd.floor_west.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor West Hot Out | ecd.floor_west.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Floor West Pump | ecd.floor_west.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Floor West Pump | ecd.floor_west.enabled | bool | True |
| ECD / VCG / TVA Conference Center In | ecd.tva_conference_center.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Conference Center Out | ecd.tva_conference_center.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Conference Center In | ecd.tva_conference_center.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Conference Center Out | ecd.tva_conference_center.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Conference Center | ecd.tva_conference_center.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / TVA Conference Center | ecd.tva_conference_center.enabled | bool | True |
| ECD / VCG / Convectors Kitchen Cold In | ecd.convectors_kitchen.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors Kitchen Cold Out | ecd.convectors_kitchen.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors Kitchen Hot In | ecd.convectors_kitchen.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors Kitchen Hot Out | ecd.convectors_kitchen.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / Convectors Kitchen Pump | ecd.convectors_kitchen.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / Convectors Kitchen Pump | ecd.convectors_kitchen.enabled | bool | True |
| ECD / VCG / TVA Wearhouse Cold In | ecd.tva_warehouse.cold_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Wearhouse Cold Out | ecd.tva_warehouse.cold_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Wearhouse Hot In | ecd.tva_warehouse.hot_in | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Wearhouse Hot Out | ecd.tva_warehouse.hot_out | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| ECD / VCG / TVA Wearhouse | ecd.tva_warehouse.pump | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| ECD / VCG / TVA Wearhouse | ecd.tva_warehouse.enabled | bool | True |
| Plugin enabled | ecd.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='ECHP'>ECHP</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Energy Center Heat Pump machines count | echp.hp.count | int | 3 |
| Energy Center Heat Pump machine index | echp.hp.index | int | 0 |
| The power of machine | echp.hp.power | int | 0 |
| The mode of the machine | echp.hp.mode | int | 0 |
| Energy Center Heat Pump cold minimum | echp.hp.cold_min | float | 5.0 |
| Energy Center Heat Pump cold maximum | echp.hp.cold_max | float | 7.0 |
| Energy Center Heat Pump hot minimum | echp.hp.hot_min | float | 41.0 |
| Energy Center Heat Pump hot maximum | echp.hp.hot_max | float | 46.0 |
| Heat Pump Control Group / VCG / Cold Buffer / Input | echp.hpcg.vcg_cold_buf.input | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Cold Buffer / Output | echp.hpcg.vcg_cold_buf.output | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Cold Buffer / Short | echp.hpcg.vcg_cold_buf.short | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Cold Geo / Input | echp.hpcg.vcg_cold_geo.input | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Cold Geo / Output | echp.hpcg.vcg_cold_geo.output | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Cold Geo / Short | echp.hpcg.vcg_cold_geo.short | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Warm Geo / Input | echp.hpcg.vcg_warm_geo.input | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Warm Geo / Output | echp.hpcg.vcg_warm_geo.output | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Warm Geo / Short | echp.hpcg.vcg_warm_geo.short | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Warm Geo / Input | echp.hpcg.vcg_warm_floor.input | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Warm Geo / Output | echp.hpcg.vcg_warm_floor.output | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / VCG / Warm Geo / Output | echp.hpcg.vcg_warm_floor.short | json | {'vendor': 'Flowx', 'model': 'FLX-05F', 'options': {'output_cw': 'off', 'output_ccw': 'off', 'limit_cw': 'off', 'limit_ccw': 'off'}} |
| Heat Pump Control Group / Water Pump / Cold | echp.hpcg.wp_cold.settings | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 2}} |
| Heat Pump Control Group / Water Pump / Hot | echp.hpcg.wp_hot.settings | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 3}} |
| Heat Pump Control Group / Water Pump / Warm | echp.hpcg.wp_warm_p.settings | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| Heat Pump Control Group / Water Pump / Warm | echp.hpcg.wp_warm_g.settings | json | {'vendor': 'Grundfos', 'model': 'MAGNA1_80_100_F_360_1x230V_PN6', 'options': {'uart': 0, 'mb_id': 0}} |
| Heat Pump Control Group / Heat Pump | echp.hpcg.hp.settings | json | {'vendor': 'HstarsGuangzhouRefrigeratingEquipmentGroup', 'model': '40STD-N420WHSB4', 'options': {'uart': 0, 'mb_id': 0}} |
| Plugin enabled | echp.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| The state of the machine | echp.hp.run | int | 0 |

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='Ventilation'>Ventilation</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| HVAC set point | vent.hvac_setpoint_1 | int | 0 |
| AC set point | vent.ac_setpoint_1 | int | 0 |
| Fans power GPIO. | vent.power_gpio_1 | str | U0:ID6:FC16:R0:RO3 |
| Lower fan settings | vent.lower_1.fan.settings | json | {'vendor': 'HangzhouAirflowElectricApplications', 'model': 'f3p146ec072600', 'options': {'output': 'AO0'}} |
| Lower fan minimum speed [%] | vent.lower_1.fan.min_speed | float | 0.0 |
| Lower fan maximum speed [%] | vent.lower_1.fan.max_speed | float | 30.0 |
| Lower fan speed [%] | vent.lower_1.fan.speed | float | 0.0 |
| Upper fan settings | vent.upper_1.fan.settings | json | {'vendor': 'HangzhouAirflowElectricApplications', 'model': 'f3p146ec072600', 'options': {'output': 'AO1'}} |
| Upper fan minimum speed [%] | vent.upper_1.fan.min_speed | float | 0.0 |
| Upper fan speed [%] | vent.upper_1.fan.speed | float | 0.0 |
| Upper fan maximum speed [%] | vent.upper_1.fan.max_speed | float | 30.0 |
| Lower air damper settings | vent.upper_1.air_damper.settings | str | off |
| Upper air damper settings | vent.lower_1.air_damper.settings | str | off |
| Count of the ventilation zones. | vent.zones_count | int | 1 |
| Ventilation enable flag. | vent.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Operators panel set point | vent.op_setpoint_1 | int | 0 |

* * *


## <a name='Alarm'>Alarm</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Alarm module sound device settings. | alarm.device.sound.settings | json | {} |
| Alarm module visual device settings. | alarm.device.visual.settings | json | {} |
| Alarm module enable flag. | alarm.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='Statistics'>Statistics</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Statistics module enable flag. | stat.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *


## <a name='OfficeConferenceHall'>Office Conference Hall</a> Registers

 - **Global**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **System**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Office conference hall module enable flag. | oc_hall.enabled | bool | False |

 - **Device**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

 - **Both**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|

* * *