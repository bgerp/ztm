# Registers descriptions for the plugins

## Intro

In this document we will discuss all topics related to registers for the plugins.
Every plugin has group of registers that is responsible for its behavior.

# Concept

 - Every plugin has its own unique name and it should be unique. All letters should be small letters. Numbers are excepted in to the names, only in the end wof the word.

    Example: **example1**

 - Every plugin have own sub registers all sub registers is deviate by full stop "**.**"

    Example: **example.register**

 - If plugin name or sub register is constructed by more then two word the intervals between words is replaced by under score "**_**"

    Example: **example.sub_register**

 - By definition every plugin can be started or stopped. This is done through an official register. Its name is "**enabled**".

    Example: **example.enabled**

 - The Enabled register can take only two values 0 or 1. Any other value will be interpreted as 0. The format of this register is integer.

    Example: **example.enabled = 0 / example.enabled = 1**

 - There is 3 main data types of registers in the system
   - Float/Integer
   - String
   - Array
   - JSON

    Example: 

    - example.float_register = 0.123456789
    - example.string_register = "String Value"
    - example.array_register = [1, 2, 3]
    - example.string_json = "{\"Current\": 0.327, \"ExportActiveEnergy\": 95.598, \"ApparentPower\": 80.345}"

    Note: Every register that is array can accept all data type described in this bullet.

 - In most cases every plugin contain more then one sub register. In this case, the name of the plugin is considered a namespace. So every sub register that has many is also considered as namespace.

 - The exchange format between the Zontromat and bgERP is **JSON**

# Registers

In this hedging we will describe all the register related to the work of the Zontromat software.


## Access Control

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Plugin enabled | ac.enabled | str | yes |
| Allowed attendees | ac.allowed_attendees | json | [{'card_id': '445E6046010080FF', 'pin': '159753', 'valid_until': '1595322860'}] |
|  | ac.nearby_attendees | json | [] |
| Card reader enabled | ac.entry_reader.enabled | str | yes |
| Card reader vendor | ac.entry_reader.vendor | str | TERACOM |
| Card reader model | ac.entry_reader.model | str | act230 |
| Card reader port baud rate | ac.entry_reader.port.baudrate | int | 9600 |
| Card reader port name | ac.entry_reader.port.name | str | COM5 |
| Card reader serial number | ac.entry_reader.serial_number | str | 2897 |
| Card reader enabled | ac.exit_reader.enabled | str | yes |
| Card reader vendor | ac.exit_reader.vendor | str | TERACOM |
| Card reader model | ac.exit_reader.model | str | act230 |
| Card reader port baud rate | ac.exit_reader.port.baudrate | int | 9600 |
| Card reader port name | ac.exit_reader.port.name | str | COM11 |
| Card reader serial number | ac.exit_reader.serial_number | str | 2911 |
| Exit button input | ac.exit_button.input | str | DI8 |
| Lock mechanism output | ac.lock_mechanism.output | str | DO1 |
| Lock mechanism time to open | ac.time_to_open | int/float | 2 |
| Door closed input | ac.door_closed.input | str | DI2 |
| Card reader enabled | ac.entry_reader2.enabled | str | no |
| Card reader vendor | ac.entry_reader2.vendor | str | TERACOM |
| Card reader model | ac.entry_reader2.model | str | act230 |
| Card reader port baud rate | ac.entry_reader2.port.baudrate | int | 9600 |
| Card reader port name | ac.entry_reader2.port.name | str | COM5 |
| Card reader serial number | ac.entry_reader2.serial_number | str | 2897 |
| Card reader enabled | ac.exit_reader2.enabled | str | no |
| Card reader vendor | ac.exit_reader2.vendor | str | TERACOM |
| Card reader model | ac.exit_reader2.model | str | act230 |
| Card reader port baud rate | ac.exit_reader2.port.baudrate | int | 9600 |
| Card reader port name | ac.exit_reader2.port.name | str | COM11 |
| Card reader serial number | ac.exit_reader2.serial_number | str | 2911 |
| Exit button input | ac.exit_button2.input | str | off |
| Lock mechanism output | ac.lock_mechanism2.output | str | off |
| Lock mechanism time to open | ac.time_to_open2 | int/float | 2 |
| Door closed input | ac.door_closed2.input | str | off |
| PIR sensor input | ac.pir.input | str | DI0 |
| PIR sensor input | ac.pir2.input | str | off |
| Window closed input | ac.window_closed.input | str | DI3 |
| Window closed input | ac.window_closed2.input | str | off |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Last 30 attendees | ac.last30_attendees | json | [] |
| Next attendance | ac.next_attendance | int/float | 0 |
| zone_occupied | ac.zone_occupied | int | 0 |
| Door closed flag | ac.door_closed.state | int | False |
| Door closed flag | ac.door_closed2.state | int | 0 |
| PIR sensor flag | ac.pir.state | int | False |
| PIR sensor flag | ac.pir2.state | int | 0 |
| Window closed flag | ac.window_closed.state | int | False |
| Window closed flag | ac.window_closed2.state | int | 0 |

## Anti Tampering

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | at.enabled | Int | 0 |
| Signal input | at.input | str | DI1 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| State | at.state | Int | 0 |

## Blinds

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | blinds.enabled | int | 0 |
| Feedback input | blinds.input_fb | str | AI1 |
| CCW output | blinds.output_ccw | str | DO0 |
| CW output | blinds.output_cw | str | DO1 |
| Position | blinds.position | int | 0 |
| Sun azimuth MOU | blinds.sun.azimuth.mou | str | deg |
| Sun azimuth value | blinds.sun.azimuth.value | float | 223.04181422580086 |
| Sun elevation MOU | blinds.sun.elevation.mou | str | deg |
| Sun elevation value | blinds.sun.elevation.value | float | 41.59276215502962 |

 - From **Zontromat** to **bgERP**

None

## Monitoring

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Cold water input flow meter | monitoring.cw.input | str | DI6 |
| Cold water tics per liter | monitoring.cw.tpl | int/float | 1 |
| Hot water input flow meter | monitoring.hw.input | str | DI7 |
| Hot water tics per liter | monitoring.hw.tpl | int/float | 1 |
| EVOK UART Index | monitoring.pa.uart | int | 2 |
| Model of the power analyser | monitoring.pa.model | str | SDM630 |
| Vendor of the power analyser | monitoring.pa.vendor | str | Eastron |
| EVOK Device index | monitoring.pa.dev_id | int | 3 |
| Enabled | monitoring.enabled | str | yes |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Info, similar resource detected description | monitoring.info_message | str | [{'hvac.air_temp_upper.circuit': '28FF2B70C11604B7'}, {'hvac.loop1.temp.circuit': '28FF2B70C11604B7'}, {'hc.tank_temp.circuit': '28FF2B70C11604B7'}] |
| Warning, similar resource description | monitoring.warning_message | str |  |
| Error, similar resource conflict description | monitoring.error_message | str | [{'ac.lock_mechanism.output': 'DO1'}, {'blinds.output_cw': 'DO1'}] |
| Clear last messages in the registers below | monitoring.clear_errors | int | 0 |
| Cold water liters consumed | monitoring.cw.value | int/float | 0 |
| Cold water liters leaks | monitoring.cw.leak | int/float | 0 |
| Hot water liters consumed | monitoring.hw.value | int/float | 0 |
| Hot water liters leaks | monitoring.hw.leak | int/float | 0 |
| Structure of electrical characteristics for LINE 1 | monitoring.pa.l1 | str | {"Current": 1.557, "ExportActiveEnergy": 95.845, "ApparentPower": 80.909} |
| Structure of electrical characteristics for LINE 2 | monitoring.pa.l2 | str | {"Current": 0.0, "ExportActiveEnergy": 0.0, "ApparentPower": 0.0} |
| Structure of electrical characteristics for LINE 3 | monitoring.pa.l3 | str | {"Current": 0.0, "ExportActiveEnergy": 0.0, "ApparentPower": 0.0} |

## Environment

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Is empty time out [s] | env.is_empty_timeout | int/float | 3600 |
| Actual outside temperature [C] | env.temp.actual | int/float | 29 |
| Actual outside temperature for 6 hours [C] | env.temp.a6 | int/float | 30 |
| Minimum outside temperature for 24 hours [C] | env.temp.min24 | int/float | 27 |
| Maximum outside temperature for 24 hours [C] | env.temp.max24 | int/float | 36 |
| Actual outside relative humidity [%] | env.rh | int/float | 60 |
| Actual wind [m/sec] | env.wind.actual | int/float | 3 |
| Maximum wind for 12 hours [m/sec] | env.wind.max12 | int/float | 6 |
| Outside light [lux] | env.light | int/float | 1000 |
| Enabled | env.enabled | str | yes |
| Energy mode of the building | env.energy | int/float | 0 |
| Emergency flags of the building  | env.emergency | int/float | 0 |
| Enable software calculation of the sun position | env.sunpos.enabled | str | no |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Is empty flag. | env.is_empty | int/float | 0 |

## Heating Ventilation and Air Conditioning (HVAC)

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Adjust temperature. | hvac.adjust_temp | int | 0 |
| Air temp sensor central circuit. | hvac.air_temp_cent.circuit | str | 28FFFCD0001703AE |
| Air temp sensor central device. | hvac.air_temp_cent.dev | str | temp |
| Air temp sensor central enabled. | hvac.air_temp_cent.enabled | int |1 |
| Air temp sensor central type. | hvac.air_temp_cent.type | str | DS18B20 |
| Air temp sensor lower circuit | hvac.air_temp_lower.circuit | str | 28FFC4EE00170349 |
| Air temp sensor lower device | hvac.air_temp_lower.dev | str | temp |
| Air temp sensor lower enabled | hvac.air_temp_lower.enabled | int |1 |
| Air temp sensor lower type | hvac.air_temp_lower.type | str | DS18B20 |
| Air temp sensor upper circuit | hvac.air_temp_upper.circuit | str | 28FF2B70C11604B7 |
| Air temp sensor upper device | hvac.air_temp_upper.dev | str | temp |
| Air temp sensor upper enabled | hvac.air_temp_upper.enabled | int |1 |
| Air temp sensor upper type | hvac.air_temp_upper.type | str | DS18B20 |
| Convector enabled. | hvac.convector.enabled | int |1 |
| Convector stage 1 output | hvac.convector.stage_1.output | str | RO0 |
| Convector stage 2 output | hvac.convector.stage_2.output | str | RO1 |
| Convector stage 3 output | hvac.convector.stage_3.output | str | RO2 |
| Convector model | hvac.convector.vendor | str | silpa |
| Measuring delta time | hvac.delta_time | int | 5 |
| Enabled | hvac.enabled | int |0 |
| Goal of the building temperature | hvac.goal_building_temp | int | 20 |
| Loop 1, water flow meter enabled | hvac.loop1.cnt.enabled | int |1 |
| Loop 1, water flow meter signal input | hvac.loop1.cnt.input | str | DI4 |
| Loop 1, water flow meter ticks per liter scale | hvac.loop1.cnt.tpl |int  | 1 |
| Loop 1, fan enabled | hvac.loop1.fan.enabled | int |1 |
| Loop 1, fan maximum speed [%] | hvac.loop1.fan.max_speed | int | 30 |
| Loop 1, fan minimum speed [%] | hvac.loop1.fan.min_speed | int | 0 |
| Loop 1, fan analog output | hvac.loop1.fan.output | str | AO3 |
| Loop 1, fan vendor | hvac.loop1.fan.vendor | str | HangzhouAirflowElectricApplications |
| Loop 1, temperature sensor circuit | hvac.loop1.temp.circuit | str | 28FF2B70C11604B7 |
| Loop 1, temperature sensor device | hvac.loop1.temp.dev | str | temp |
| Loop 1, temperature sensor enabled | hvac.loop1.temp.enabled | int |1 |
| Loop 1, temperature sensor type | hvac.loop1.temp.type | str | DS18B20 |
| Loop 1, valve enabled | hvac.loop1.valve.enabled | int |1 |
| Loop 1, valve feed back input | hvac.loop1.valve.feedback |str  | AI1 |
| Loop 1, valve maximum position | hvac.loop1.valve.max_pos | int | 100 |
| Loop 1, valve minimum position | hvac.loop1.valve.min_pos | int | 0 |
| Loop 1, valve output | hvac.loop1.valve.output | str | RO4 |
| Loop 1, valve vendor | hvac.loop1.valve.vendor | str | TONHE |
| Loop 2, water flow meter enabled | hvac.loop2.cnt.enabled | int |1 |
| Loop 2, water flow meter signal input | hvac.loop2.cnt.input | str | DI5 |
| Loop 2, water flow meter ticks per liter scale | hvac.loop2.cnt.tpl | int | 1 |
| Loop 2, fan enabled | hvac.loop2.fan.enabled | int |1 |
| Loop 2, fan maximum speed [%] | hvac.loop2.fan.max_speed | int | 30 |
| Loop 2, fan minimum speed [%] | hvac.loop2.fan.min_speed | int | 0 |
| Loop 2, fan analog output | hvac.loop2.fan.output | str | AO4 |
| Loop 2, fan vendor | hvac.loop2.fan.vendor | str | HangzhouAirflowElectricApplications |
| Loop 2, temperature sensor circuit | hvac.loop2.temp.circuit | str | 28FFC4EE00170349 |
| Loop 2, temperature sensor device | hvac.loop2.temp.dev | str | temp |
| Loop 2, temperature sensor enabled | hvac.loop2.temp.enabled | int |1 |
| Loop 2, temperature sensor type | hvac.loop2.temp.type | str | DS18B20 |
| Loop 2, valve enabled | hvac.loop2.valve.enabled | int |1 |
| Loop 2, valve feed back input | hvac.loop2.valve.feedback | str | AI2 |
| Loop 2, valve maximum position | hvac.loop2.valve.max_pos | int | 100 |
| Loop 2, valve minimum position | hvac.loop2.valve.min_pos | int | 0 |
| Loop 2, valve output | hvac.loop2.valve.output | str | RO3 |
| Loop 2, valve vendor | hvac.loop2.valve.vendor | str | TONHE |
| Actual temperature | hvac.temp.actual | int | null |
| Maximum achievable | hvac.temp.max | int | 30 |
| Minimum achievable | hvac.temp.min | int | 20 |
| Thermal force limit | hvac.thermal_force_limit | int | 100 |
| Thermal mode | hvac.thermal_mode | int | 2 |
| Update rate of the plugin | hvac.update_rate | int | 3 |

 - From **Zontromat** to **bgERP**

None

## Light

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | light.enabled | int |0 |
| Maximum limit | light.max | int | 10000 |
| Minimum limit | light.min | int | 800 |
| Sensor circuit | light.sensor.circuit | str | 26607314020000F8 |
| Sensor device | light.sensor.dev | str | 1wdevice |
| Sensor enabled | light.sensor.enabled | int |1 |
| Analog output 1 | light.v1.output | str | AO1 |
| Analog output 2 | light.v2.output | str | AO2 |

 - From **Zontromat** to **bgERP**

None

## System

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| System activity LED output | sys.sl.output | str | LED0 |
| LEd blink time | sys.sl.blink_time | int/float | 1 |
| Enabled | sys.enabled | str | yes |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Current consumed RAM | sys.ram.current | int/float | 0 |
| Maximum consumed RAM | sys.ram.peak | int/float | 0 |
| Application cycle time. | sys.time.usage | int/float | 0 |

## WDT Tablet

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| ASK | wt.enabled | int | 0 |
| ASK | wt.output | str | DO3 |
| ASK | wt.pulse_time | int | 10 |
| ASK | wt.reset | int | 0 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| ASK | wt.state | int | 0 |
