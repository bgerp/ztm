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

    Note: Every register that is array can accept all data type described in this bullet.

 - In most cases every plugin contain more then one sub register. In this case, the name of the plugin is considered a namespace. So every sub register that has many is also considered as namespace.

 - The exchange format between the Zontromat and bgERP is **JSON**

# Registers

In this hedging we will describe all the register related to the work of the Zontromat software.


## Access Control 1

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Allowed attendees cards IDs. | access_control_1.allowed_attendees | Array | ["445E6046010080FF"] |
| Card reader, enabled | "access_control_1.card_reader.enabled" | int | 1 |
| Card reader model | access_control_1.card_reader.model | str | "act230" |
| Card reader, port, baud rate | access_control_1.card_reader.port.baudrate | int | 9600 |
| Card reader, port, name | access_control_1.card_reader.port.name | str | COM4 |
| Card reader, serial number | access_control_1.card_reader.serial_number | str | "2897" |
| Card reader, vendor | access_control_1.card_reader.vendor | int | "TERACOM" |
| Card reader, enabled | access_control_1.enabled | int | 1 |
| Exit button, enabled | access_control_1.exit_button.enabled | int | 1 |
| Exit button, input | access_control_1.exit_button.input | str | "DI0" |
| Lock mechanism, enabled | access_control_1.lock_mechanism.enabled | str | 1 |
| Lock mechanism, output | access_control_1.lock_mechanism.output | str | "DO2" |
| Lock mechanism, time to open | access_control_1.time_to_open | int | 10 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Next attendance | access_control_1.next_attendance | --- | null |


## Access Control 2

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Allowed attendees cards IDs. | access_control_2.allowed_attendees | Array | ["445E6046010080FF"] |
| Card reader, enabled | "access_control_2.card_reader.enabled" | int | 1 |
| Card reader model | access_control_2.card_reader.model | str | "act230" |
| Card reader, port, baud rate | access_control_2.card_reader.port.baudrate | int | 9600 |
| Card reader, port, name | access_control_2.card_reader.port.name | str | COM5 |
| Card reader, serial number | access_control_2.card_reader.serial_number | str | "2911" |
| Card reader, vendor | access_control_2.card_reader.vendor | int | "TERACOM" |
| Card reader, enabled | access_control_2.enabled | int | 1 |
| Exit button, enabled | access_control_2.exit_button.enabled | int | 1 |
| Exit button, input | access_control_2.exit_button.input | str | "DI0" |
| Lock mechanism, enabled | access_control_2.lock_mechanism.enabled | str | 1 |
| Lock mechanism, output | access_control_2.lock_mechanism.output | str | "DO2" |
| Lock mechanism, time to open | access_control_2.time_to_open | Int | 10 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Next attendance | access_control_2.next_attendance | --- | null |


## Anti Tampering

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | anti_tampering.enabled | Int | 0 |
| Signal input | anti_tampering.input | str | "DI1" |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| State | anti_tampering.state | Int | 0 |


## Blinds

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | blinds.enabled | int | 0 |
| Feedback input | blinds.input_fb | str | "AI1" |
| CCW output | blinds.output_ccw | str | "DO0" |
| CW output | blinds.output_cw | str | "DO1" |
| Position | blinds.position | int | 0 |
| Sun azimuth MOU | blinds.sun.azimuth.mou | str | "deg" |
| Sun azimuth value | blinds.sun.azimuth.value | float | 223.04181422580086 |
| Sun elevation MOU | blinds.sun.elevation.mou | str | "deg" |
| Sun elevation value | blinds.sun.elevation.value | float | 41.59276215502962 |

 - From **Zontromat** to **bgERP**

None


## Cold drink water

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
|  | cold_circle.enabled | int | 0 |
|  | cold_water_fm.input | str | "DI6" |
|  | cold_water_fm.tpl | int | 10 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Cold water liters | cold_water_fm.value | int | 0 |

## Hot drink water

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
|  | hot_circle.enabled | int | 0 |
|  | hot_water_fm.input | str | "DI7" |
|  | hot_water_fm.tpl | int | 10 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Hot water liters | hot_water_fm.value | int | 0 |


## Door closed

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | door_closed.enabled | int | 0 |
| Door tamper signal | door_closed.input | str | "DI2" |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| State | door_closed.state | Int | 0 |

## General

### Registers

 - From **bgERP** to **Zontromat**

None

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Reported liters for the last reporting period. | general.cold_water_fm.leak | float | 0 |
| Reported liters for the last reporting period. | general.hot_water_fm.leak | float | | 0 |
| Is the zone empty. | general.is_empty | int | 0 |
| Time since empty. | general.is_empty_timeout | int | 0 |

## Heating Ventilation and Air Conditioning (HVAC)

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Adjust temperature. | hvac.adjust_temp | int | 0 |
| Air temp sensor central circuit. | hvac.air_temp_cent.circuit | str | "28FFFCD0001703AE" |
| Air temp sensor central device. | hvac.air_temp_cent.dev | str | "temp" |
| Air temp sensor central enabled. | hvac.air_temp_cent.enabled | int |1 |
| Air temp sensor central type. | hvac.air_temp_cent.type | str | "DS18B20" |
| Air temp sensor lower circuit | hvac.air_temp_lower.circuit | str | "28FFC4EE00170349" |
| Air temp sensor lower device | hvac.air_temp_lower.dev | str | "temp" |
| Air temp sensor lower enabled | hvac.air_temp_lower.enabled | int |1 |
| Air temp sensor lower type | hvac.air_temp_lower.type | str | "DS18B20" |
| Air temp sensor upper circuit | hvac.air_temp_upper.circuit | str | "28FF2B70C11604B7" |
| Air temp sensor upper device | hvac.air_temp_upper.dev | str | "temp" |
| Air temp sensor upper enabled | hvac.air_temp_upper.enabled | int |1 |
| Air temp sensor upper type | hvac.air_temp_upper.type | str | "DS18B20" |
| Convector enabled. | hvac.convector.enabled | int |1 |
| Convector stage 1 output | hvac.convector.stage_1.output | str | "RO0" |
| Convector stage 2 output | hvac.convector.stage_2.output | str | "RO1" |
| Convector stage 3 output | hvac.convector.stage_3.output | str | "RO2" |
| Convector model | hvac.convector.vendor | str | "silpa" |
| Measuring delta time | hvac.delta_time | int | 5 |
| Enabled | hvac.enabled | int |0 |
| Goal of the building temperature | hvac.goal_building_temp | int | 20 |
| Loop 1, water flow meter enabled | hvac.loop1.cnt.enabled | int |1 |
| Loop 1, water flow meter signal input | hvac.loop1.cnt.input | str | "DI4" |
| Loop 1, water flow meter ticks per liter scale | hvac.loop1.cnt.tpl |int  | 1 |
| Loop 1, fan enabled | hvac.loop1.fan.enabled | int |1 |
| Loop 1, fan maximum speed [%] | hvac.loop1.fan.max_speed | int | 30 |
| Loop 1, fan minimum speed [%] | hvac.loop1.fan.min_speed | int | 0 |
| Loop 1, fan analog output | hvac.loop1.fan.output | str | "AO3" |
| Loop 1, fan vendor | hvac.loop1.fan.vendor | str | "HangzhouAirflowElectricApplications" |
| Loop 1, temperature sensor circuit | hvac.loop1.temp.circuit | str | "28FF2B70C11604B7" |
| Loop 1, temperature sensor device | hvac.loop1.temp.dev | str | "temp" |
| Loop 1, temperature sensor enabled | hvac.loop1.temp.enabled | int |1 |
| Loop 1, temperature sensor type | hvac.loop1.temp.type | str | "DS18B20" |
| Loop 1, valve enabled | hvac.loop1.valve.enabled | int |1 |
| Loop 1, valve feed back input | hvac.loop1.valve.feedback |str  | "AI1" |
| Loop 1, valve maximum position | hvac.loop1.valve.max_pos | int | 100 |
| Loop 1, valve minimum position | hvac.loop1.valve.min_pos | int | 0 |
| Loop 1, valve output | hvac.loop1.valve.output | str | "RO4" |
| Loop 1, valve vendor | hvac.loop1.valve.vendor | str | "TONHE" |
| Loop 2, water flow meter enabled | hvac.loop2.cnt.enabled | int |1 |
| Loop 2, water flow meter signal input | hvac.loop2.cnt.input | str | "DI5" |
| Loop 2, water flow meter ticks per liter scale | hvac.loop2.cnt.tpl | int | 1 |
| Loop 2, fan enabled | hvac.loop2.fan.enabled | int |1 |
| Loop 2, fan maximum speed [%] | hvac.loop2.fan.max_speed | int | 30 |
| Loop 2, fan minimum speed [%] | hvac.loop2.fan.min_speed | int | 0 |
| Loop 2, fan analog output | hvac.loop2.fan.output | str | "AO4" |
| Loop 2, fan vendor | hvac.loop2.fan.vendor | str | "HangzhouAirflowElectricApplications" |
| Loop 2, temperature sensor circuit | hvac.loop2.temp.circuit | str | "28FFC4EE00170349" |
| Loop 2, temperature sensor device | hvac.loop2.temp.dev | str | "temp" |
| Loop 2, temperature sensor enabled | hvac.loop2.temp.enabled | int |1 |
| Loop 2, temperature sensor type | hvac.loop2.temp.type | str | "DS18B20" |
| Loop 2, valve enabled | hvac.loop2.valve.enabled | int |1 |
| Loop 2, valve feed back input | hvac.loop2.valve.feedback | str | "AI2" |
| Loop 2, valve maximum position | hvac.loop2.valve.max_pos | int | 100 |
| Loop 2, valve minimum position | hvac.loop2.valve.min_pos | int | 0 |
| Loop 2, valve output | hvac.loop2.valve.output | str | "RO3" |
| Loop 2, valve vendor | hvac.loop2.valve.vendor | str | "TONHE" |
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
| Sensor circuit | light.sensor.circuit | str | "26607314020000F8" |
| Sensor device | light.sensor.dev | str | "1wdevice" |
| Sensor enabled | light.sensor.enabled | int |1 |
| Analog output 1 | light.v1.output | str | "AO1" |
| Analog output 2 | light.v2.output | str | "AO2" |

 - From **Zontromat** to **bgERP**

None


## Mode

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| State of the emergency outputs, bit coded | mode.emergency | int | 0 |
| Energy mode of the building | mode.energy | int | 0 |

 - From **Zontromat** to **bgERP**

None


## Monitoring

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | monitoring.enabled | int | 0 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Clear last messages in the registers below | monitoring.clear_errors | int | 0 |
| Error, similar resource conflict description | monitoring.error_message | JSON |  |
| Info, similar resource detected description | monitoring.info_message | JSON |  |
| Warning, similar resource description | monitoring.warning_message | JSON |  |


## Outside

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Outside of the building light. | outside.light | int | null |
| Outside of the building relative humidity | outside.rh | int | null |
| Outside of the building actual temp 6hours behind | outside.temp.a6 | int | null |
| Outside of the building actual temperature | outside.temp.actual | int | null |
| Outside of the building maximum temperature for 24 hours | outside.temp.max24 | int | null |
| Outside of the building minimum temperature for 24 hours | outside.temp.min24 | int | null |
| Outside of the building actual wind speed | outside.wind.actual | int | null |
| Outside of the building average speed for 12 hours. | outside.wind.max12 | int | null |

 - From **Zontromat** to **bgERP**

None


## PIR Detector

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | pir_detector.enabled | int |0 |
| Signal input | pir_detector.input | str | "DI0" |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| State | pir_detector.state | Int | 0 |


## Self current

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | self_current.enabled | int | 0 |
| Power analyser MODBUS ID | self_current.sub_dev.dev_id | int | 2 |
| Power analyser model name | self_current.sub_dev.model | str | "SDM120" |
| Power analyser UART name | self_current.sub_dev.uart | int | 1 |
| Power analyser vendor name | self_current.sub_dev.vendor | str | "Eastron" |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Drained current of the room | self_current.sub_dev.current.value | float | 0.098 |
| Drained power of the room | self_current.sub_dev.current_power.value | float | 17.029 |
| Total consumed energy | self_current.sub_dev.total_energy.value | float | 0.18 |

## Self

### Registers

 - From **bgERP** to **Zontromat**

None

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| RAM Usage | self.ram.current | float | 0 |
| RAM Peak usage | self.ram.peak | float | 0 |
| Cycle time consumption. | self.time.usage | float | 0 |


## Status LED

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Blink time | status_led.blink_time | int | 1 |
| Enabled | status_led.enabled | int |1 |
| Signal output | status_led.output | str | "LED0" |

 - From **Zontromat** to **bgERP**

None

## Software SUN position


### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | sun_pos.enabled | int | 1 |

 - From **Zontromat** to **bgERP**

None


## WDT Tablet

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| DEPRECATED | wdt_tablet.enabled | int | 0 |
| DEPRECATED | wdt_tablet.output | str | "DO3" |
| DEPRECATED | wdt_tablet.pulse_time | int | 10 |
| DEPRECATED | wdt_tablet.reset | int | 0 |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| DEPRECATED | wdt_tablet.state | int | 0 |

WILL BE DEPRECATED

## Window closed

### Registers

 - From **bgERP** to **Zontromat**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| Enabled | window_closed.enabled | int | 0 |
| Signal input | window_closed.input | str | "!DI3" |

 - From **Zontromat** to **bgERP**

| Purpose | Register | Type | Value |
|----------|:-------------|:------|:------|
| State | window_closed.state | Int | 0 |
