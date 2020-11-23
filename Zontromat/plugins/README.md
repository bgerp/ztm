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

 - The Enabled register can take only two values **false** or **true**. Any other value will be interpreted as 0. The format of this register is integer.

    Example: **example.enabled = false / example.enabled = true**

 - There is few data types of registers in the system
   - Integer
   - Float
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

 - When register exists in the system it always have allowed values. For this purpose we use few special characters to describe is this enum, interval (open and close), or just a string value.
   - In case of **Enum**, we divide possible values wit vertical pipe "**|**", example: 0|1|2|3|4|5
   - In case we have **Interval** we use slash "**/**", example: from 0 to 5, 0/5. If we wan to define a lower limit 0/. This means that all positive values are allowed. Respectively we can define upper limit by doing this /50. It means that all values below 50 are acceptable.  

# Registers

In this hedging we will describe all the register related to the work of the Zontromat software.


## Access Control

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Plugin enabled | ac.enabled | str | true |
| Allowed attendees | ac.allowed_attendees | json | [{'card_id': '445E6046010080FF', 'pin': '159753', 'valid_until': '1595322860'}] |
|  | ac.nearby_attendees | json | [] |
| Card reader - vendor/model/serial number | ac.entry_reader_1.enabled | str | TERACOM/act230/2897 |
| Card reader port baud rate | ac.entry_reader_1.port.baudrate | int | 9600 |
| Card reader port name | ac.entry_reader_1.port.name | str | COM5 |
| Card reader - vendor/model/serial number | ac.exit_reader_1.enabled | str | TERACOM/act230/2911 |
| Card reader port baud rate | ac.exit_reader_1.port.baudrate | int | 9600 |
| Card reader port name | ac.exit_reader_1.port.name | str | COM11 |
| Exit button input | ac.exit_button_1.input | str | DI8 |
| Lock mechanism output | ac.lock_mechanism_1.output | str | DO1 |
| Lock mechanism time to open | ac.time_to_open_1 | int | 2 |
| Door closed input | ac.door_closed_1.input | str | DI2 |
| PIR sensor input | ac.pir_1.input | str | DI0 |
| Window closed input | ac.window_closed_1.input | str | DI3 |
| Card reader - vendor/model/serial number | ac.entry_reader_2.enabled | str | TERACOM/act230/2897 |
| Card reader port baud rate | ac.entry_reader_2.port.baudrate | int | 9600 |
| Card reader port name | ac.entry_reader_2.port.name | str | COM5 |
| Card reader - vendor/model/serial number | ac.exit_reader_2.enabled | str | TERACOM/act230/2911 |
| Card reader port baud rate | ac.exit_reader_2.port.baudrate | int | 9600 |
| Card reader port name | ac.exit_reader_2.port.name | str | COM11 |
| Exit button input | ac.exit_button_2.input | str | off |
| Lock mechanism output | ac.lock_mechanism_2.output | str | off |
| Lock mechanism time to open | ac.time_to_open_2 | int | 2 |
| Door closed input | ac.door_closed_2.input | str | off |
| PIR sensor input | ac.pir_2.input | str | off |
| Window closed input | ac.window_closed_2.input | str | off |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Attendees for last minute. | ac.last_minute_attendees | json | [] |
| Next attendance | ac.next_attendance | int | 0 |
| Zone occupied flag. | ac.zone_occupied | int | 0 |
| Door closed flag | ac.door_closed_1.state | bool | False |
| Door closed flag | ac.door_closed_2.state | bool | False |
| PIR sensor flag | ac.pir_1.state | bool | False |
| PIR sensor flag | ac.pir_2.state | bool | False |
| Window closed flag | ac.window_closed_1.state | bool | False |
| Window closed flag | ac.window_closed_2.state | bool | False |

## Blinds

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | blinds.enabled | int | false |
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
| Power analyser - Modbus type/Vendor/EVOK UART Index/EVOK Device index | monitoring.pa.settings | str | mb-rtu/Eastron/SDM630/2/3 |
| Enabled | monitoring.enabled | str | true |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Cold water liters consumed | monitoring.cw.value | int/float | 0 |
| Cold water liters leaks | monitoring.cw.leak | int/float | 0 |
| Hot water liters consumed | monitoring.hw.value | int/float | 0 |
| Hot water liters leaks | monitoring.hw.leak | int/float | 0 |
| Structure of electrical characteristics for LINE 1 | monitoring.pa.l1 | json | {"Current": 1.557, "ExportActiveEnergy": 95.845, "ApparentPower": 80.909} |
| Structure of electrical characteristics for LINE 2 | monitoring.pa.l2 | json | {"Current": 0.0, "ExportActiveEnergy": 0.0, "ApparentPower": 0.0} |
| Structure of electrical characteristics for LINE 3 | monitoring.pa.l3 | json | {"Current": 0.0, "ExportActiveEnergy": 0.0, "ApparentPower": 0.0} |


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
| Enabled | env.enabled | str | false |
| Energy mode of the building | env.energy | float | 0 |
| Emergency index for the fire. | env.flag_fire | int | 0 |
| Emergency index for the storm. | env.flag_storm | int | 0 |
| Emergency index for the earthquake. | env.flag_earthquake | Int | 0 |
| Emergency index for the gassing. | env.flag_gassing | int | 0 |
| Emergency index for the flooding. | env.flag_flooding | int | 0 |
| Emergency index for the blocking. | env.flag_blocked | int | 0 |
| Enable software calculation of the sun position | env.sunpos.enabled | str | false |

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
| Air temp sensor central - device/type/circuit | hvac.air_temp_cent.settings | str | temp/DS18B20/28FFFCD0001703AE |
| Air temp sensor lower - device/type/circuit | hvac.air_temp_lower.settings | str | temp/DS18B20/28FFC4EE00170349 |
| Air temp sensor upper - device/type/circuit | hvac.air_temp_upper.settings | str | temp/DS18B20/28FF2B70C11604B7 |
| Convector - vendor/model | hvac.convector.settings | str | silpa/klimafan |
| Convector stage 1 output | hvac.convector.stage_1.output | str | RO0 |
| Convector stage 2 output | hvac.convector.stage_2.output | str | RO1 |
| Convector stage 3 output | hvac.convector.stage_3.output | str | RO2 |
| Measuring delta time | hvac.delta_time | int | 5 |
| Enabled | hvac.enabled | int | false |
| Goal of the building temperature | hvac.goal_building_temp | int | 20 |
| Loop 1, water flow meter ticks per liter scale. | hvac.loop1.cnt.tpl | int | 1 |
| Loop 1, water flow meter signal input. | hvac.loop1.cnt.input | str | DI4 |
| Loop 1, fan - vendor/model  | hvac.loop1.fan.settings | str | HangzhouAirflowElectricApplications/f3p146ec072600 |
| Loop 1, fan analog output | hvac.loop1.fan.output | str | AO3 |
| Loop 1, fan maximum speed [%] | hvac.loop1.fan.max_speed | int | 30 |
| Loop 1, fan minimum speed [%] | hvac.loop1.fan.min_speed | int | 0 |
| Loop 1, temperature sensor - device/type/circuit | hvac.air_temp_cent.settings | str | temp/DS18B20/28FF2B70C11604B7 |
| Loop 1, valve - vendor/model | hvac.loop1.valve.settings | str | TONHE/a20m15b2c |
| Loop 1, valve output | hvac.loop1.valve.output | str | RO4 |
| Loop 1, valve feed back input | hvac.loop1.valve.feedback | str | AI1 |
| Loop 1, valve maximum position [%] | hvac.loop1.valve.max_pos | int | 100 |
| Loop 1, valve minimum position [%] | hvac.loop1.valve.min_pos | int | 0 |
| Loop 2, water flow meter ticks per liter scale. | hvac.loop2.cnt.tpl | int | 1 |
| Loop 2, water flow meter signal input. | hvac.loop2.cnt.input | str | DI5 |
| Loop 2, fan - vendor/model. | hvac.loop2.fan.settings | str | HangzhouAirflowElectricApplications/f3p146ec072600 |
| Loop 2, fan analog output | hvac.loop2.fan.output | str | AO4 |
| Loop 2, fan maximum speed [%] | hvac.loop2.fan.min_speed | int | 0 |
| Loop 2, fan minimum speed [%] | hvac.loop2.fan.max_speed | int | 30 |
| Loop 2, temperature sensor - device/type/circuit | hvac.loop2.temp.settings | str | temp/DS18B20/28FFC4EE00170349 |
| Loop 2, valve - vendor/model | hvac.loop2.valve.settings | str | TONHE/a20m15b2c |
| Loop 2, valve output | hvac.loop2.valve.output | str | RO3 |
| Loop 2, valve feed back input | hvac.loop2.valve.feedback | str | AI2 |
| Loop 2, valve maximum position | hvac.loop2.valve.max_pos | int | 100 |
| Loop 2, valve minimum position [%] | hvac.loop2.valve.min_pos | int | 0 |
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
| Enabled | light.enabled | int |false |
| Maximum limit | light.max | int | 10000 |
| Minimum limit | light.min | int | 800 |
| Sensor - device/circuit | light.sensor.settings | str | 1wdevice/26607314020000F8 |
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
| LED blink time | sys.sl.blink_time | float | 1 |
| Anti tampering input. | sys.at.input | str | DI1 |
| Enabled | sys.enabled | str | true |
| Clear last messages in the registers below | sys.col.clear_errors | int | 0 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Error frm the last minute. | sys.last_minute_errs | str |  |
| Current consumed RAM. | sys.ram.current | int | 0 |
| Maximum consumed RAM. | sys.ram.peak | int | 0 |
| Application cycle time. | sys.time.usage | float | 0 |
| Antin tampering state. | sys.at.state | bool | False |
| Info, similar resource detected description. | sys.col.info_message | str |  |
| Warning, similar resource description. | sys.col.warning_message | str |  |
| Error, similar resource conflict description. | sys.col.error_message | str | [{'ac.entry_reader_1.port.name': 'COM5'}, {'ac.entry_reader_2.port.name': 'COM5'}] |
