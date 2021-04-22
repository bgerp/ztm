# Communication with bgERP

## Intro

In this document we will discuss all topics related to method of exchange information between bgERP and Zontromat software. It is basicity P2P communication that is exchanging information between two peers. bgERP and Zontromat software. The relations between two peers is Client <-> Server.

## Goals

 - Two-way data exchange.
 - Send periodically the status of the area.
 - Change of parameter values for the respective function blocks and / or devices.
 - Loading new functions in the controller.

## Login procedure

In this section we will pay attention to all the fields of the communication package. The data is sent to the server via an HTTP-POST request. The content of the request consists of the JSON string field to which this data is assigned.

1. Example of the request:

 - Domains

Tests:
http://zontromat.polygonteam.com/ztm/login

Working:
https://bcvt.eu/ztm/login

 - No additional headers are required.

 - No parameters are required.

 - Body

In the body of the request is the JSON structure, which contains the data for a controller.

```json
{
    "serial_number":  346,
    "model":  "S103",
    "version":  "1.0"
}
```

2. Example of the response:

The response to this request is based mainly on the HTTP operating codes and the body of the JSON response. The status code of the HTTP protocol is used to determine the problem.

 - Answer with status code **200**

With this status code, the device is considered to be well received by the system and responds with content in the body of the response.

Answer body:

```json
{
    "session_id": "5dd2861d5f1d91.55146905",
    "bgerp_id": "BG_ERP_ID"
}
```

 - Answer with status code **403**

This status code indicates that the device is not accepted. For whatever reason.

Answer body: NO

 - Answer with status code **423**

This status code indicates that the device is already registered and its session key must be used.

Answer body: NO

## Sync procedure

Request to the server for current status. The data is sent to the server via an HTTP-POST request. The content of the request is empty.

1. Example of the request:

 - Domains

Tests:
http://zontromat.polygonteam.com/ztm/sync

Working:
http://bcvt.eu/ztm/sync

 - No additional headers are required.

 - No parameters are required.

 - Body:

In the body of the request is the JSON structure that contains the session identifier.

```json
{   "session_id":"5f044225ea5d84.80102310",
   "regs":{
      "general.is_empty":1,
      "general.is_empty_timeout":"None",
      "general.cwf.leak":0,
      "general.hwf.leak":0,
      "monitoring.info_message":"",
      "monitoring.warning_message":"",
      "monitoring.error_message":"",
      "monitoring.clear_errors":0,
      "wc.state":"None",
      "dc.state":"None",
      "pd.state":"None",
      "at.state":"None",
      "fire_detect.state":"None",
      "cwf.value":"None",
      "hwf.value":"None",
      "sc.sub_dev.current.value":0,
      "sc.sub_dev.total_energy.value":0,
      "sc.sub_dev.current_power.value":0,
      "ac1.next_attendance":"None",
      "ac2.next_attendance":"None",
      "wt.state":"None",
      "self.ram.current":0,
      "self.ram.peak":0,
      "self.time.usage":0
    }
}
```

2. Example of the answer:

The response to this request is based primarily on JSON. The status code of the HTTP protocol is used to determine the problem.

 - Answer with status code 200

With this status code, the device is considered to be well received by the system and responds with content in the body of the response.

Answer body:

```json
{
    "ac1.allowed_attendees": [
        "445E6046010080FF"
    ],
    "ac1.card_reader.enabled": 1,
    "ac1.card_reader.model": "act230",
    "ac1.card_reader.port.baudrate": 9600,
    "ac1.card_reader.port.name": "COM4",
    "ac1.card_reader.serial_number": "2897",
    "ac1.card_reader.vendor": "Teracom",
    "ac1.enabled": 0,
    "ac1.exit_button.enabled": 1,
    "ac1.exit_button.input": "DI0",
    "ac1.lock_mechanism.enabled": 1,
    "ac1.lock_mechanism.output": "DO2",
    "ac1.time_to_open": 10,
    "ac2.allowed_attendees": [
        "445E6046010080FF"
    ],
    "ac2.card_reader.enabled": 1,
    "ac2.card_reader.model": "act230",
    "ac2.card_reader.port.baudrate": 9600,
    "ac2.card_reader.port.name": "COM5",
    "ac2.card_reader.serial_number": "2911",
    "ac2.card_reader.vendor": "Teracom",
    "ac2.enabled": 0,
    "ac2.exit_button.enabled": 1,
    "ac2.exit_button.input": "DI0",
    "ac2.lock_mechanism.enabled": 1,
    "ac2.lock_mechanism.output": "DO2",
    "ac2.time_to_open": 10,
    "at.enabled": 0,
    "at.input": "DI1",
    "blinds.enabled": 0,
    "blinds.input_fb": "AI0",
    "blinds.output_ccw": "DO0",
    "blinds.output_cw": "DO1",
    "blinds.position": 0,
    "blinds.sun.azimuth.mou": "deg",
    "blinds.sun.azimuth.value": 0,
    "blinds.sun.elevation.mou": "deg",
    "blinds.sun.elevation.value": 0,
    "cc.enabled": 0,
    "cc.goal_temp": 8,
    "cc.tank_temp.circuit": "28FFFCD0001703AE",
    "cc.tank_temp.dev": "temp",
    "cc.tank_temp.enabled": 1,
    "cc.tank_temp.type": "DS18B20",
    "cwf.enabled": 0,
    "cwf.input": "DI6",
    "cwf.tpl": 10,
    "dc.enabled": 0,
    "dc.input": "DI2",
    "fire_detect.enabled": 0,
    "fire_detect.input": null,
    "hc.enabled": 0,
    "hc.goal_temp": 20,
    "hc.tank_temp.circuit": "28FF2B70C11604B7",
    "hc.tank_temp.dev": "temp",
    "hc.tank_temp.enabled": 1,
    "hc.tank_temp.type": "DS18B20",
    "hwf.enabled": 0,
    "hwf.input": "DI7",
    "hwf.tpl": 10,
    "hvac.adjust_temp": 0,
    "hvac.air_temp_cent.circuit": "28FFFCD0001703AE",
    "hvac.air_temp_cent.dev": "temp",
    "hvac.air_temp_cent.enabled": 1,
    "hvac.air_temp_cent.type": "DS18B20",
    "hvac.air_temp_lower.circuit": "28FFC4EE00170349",
    "hvac.air_temp_lower.dev": "temp",
    "hvac.air_temp_lower.enabled": 1,
    "hvac.air_temp_lower.type": "DS18B20",
    "hvac.air_temp_upper.circuit": "28FF2B70C11604B7",
    "hvac.air_temp_upper.dev": "temp",
    "hvac.air_temp_upper.enabled": 1,
    "hvac.air_temp_upper.type": "DS18B20",
    "hvac.convector.enabled": 1,
    "hvac.convector.stage_1.output": "RO0",
    "hvac.convector.stage_2.output": "RO1",
    "hvac.convector.stage_3.output": "RO2",
    "hvac.convector.vendor": "silpa",
    "hvac.delta_time": 5,
    "hvac.enabled": 0,
    "hvac.goal_building_temp": 20,
    "hvac.loop1.cnt.enabled": 1,
    "hvac.loop1.cnt.input": "DI4",
    "hvac.loop1.cnt.tpl": 1,
    "hvac.loop1.fan.enabled": 1,
    "hvac.loop1.fan.max_speed": 30,
    "hvac.loop1.fan.min_speed": 0,
    "hvac.loop1.fan.output": "AO3",
    "hvac.loop1.fan.vendor": "HangzhouAirflowElectricApplications",
    "hvac.loop1.temp.circuit": "28FF2B70C11604B7",
    "hvac.loop1.temp.dev": "temp",
    "hvac.loop1.temp.enabled": 1,
    "hvac.loop1.temp.type": "DS18B20",
    "hvac.loop1.valve.enabled": 1,
    "hvac.loop1.valve.feedback": "AI1",
    "hvac.loop1.valve.max_pos": 100,
    "hvac.loop1.valve.min_pos": 0,
    "hvac.loop1.valve.output": "RO4",
    "hvac.loop1.valve.vendor": "TONHE",
    "hvac.loop2.cnt.enabled": 1,
    "hvac.loop2.cnt.input": "DI5",
    "hvac.loop2.cnt.tpl": 1,
    "hvac.loop2.fan.enabled": 1,
    "hvac.loop2.fan.max_speed": 30,
    "hvac.loop2.fan.min_speed": 0,
    "hvac.loop2.fan.output": "AO4",
    "hvac.loop2.fan.vendor": "HangzhouAirflowElectricApplications",
    "hvac.loop2.temp.circuit": "28FFC4EE00170349",
    "hvac.loop2.temp.dev": "temp",
    "hvac.loop2.temp.enabled": 1,
    "hvac.loop2.temp.type": "DS18B20",
    "hvac.loop2.valve.enabled": 1,
    "hvac.loop2.valve.feedback": "AI2",
    "hvac.loop2.valve.max_pos": 100,
    "hvac.loop2.valve.min_pos": 0,
    "hvac.loop2.valve.output": "RO3",
    "hvac.loop2.valve.vendor": "TONHE",
    "hvac.temp.actual": null,
    "hvac.temp.max": 30,
    "hvac.temp.min": 20,
    "hvac.thermal_force_limit": 100,
    "hvac.thermal_mode": 2,
    "hvac.update_rate": 3,
    "light.enabled": 0,
    "light.max": 10000,
    "light.min": 800,
    "light.sensor.circuit": "26607314020000F8",
    "light.sensor.dev": "1wdevice",
    "light.sensor.enabled": 1,
    "light.v1.output": "AO1",
    "light.v2.output": "AO2",
    "mode.emergency": 0,
    "mode.energy": 0,
    "monitoring.enabled": 0,
    "outside.light": null,
    "outside.rh": null,
    "outside.temp.a6": null,
    "outside.temp.actual": null,
    "outside.temp.max24": null,
    "outside.temp.min24": null,
    "outside.wind.actual": null,
    "outside.wind.max12": null,
    "pd.enabled": 0,
    "pd.input": "DI0",
    "sc.enabled": 0,
    "sc.sub_dev.dev_id": 2,
    "sc.sub_dev.model": "SDM120",
    "sc.sub_dev.uart": 1,
    "sc.sub_dev.vendor": "Eastron",
    "sl.blink_time": 1,
    "sl.enabled": 1,
    "sl.output": "LED0",
    "sp.enabled": 0,
    "wt.enabled": 0,
    "wt.output": "DO3",
    "wt.pulse_time": 10,
    "wt.reset": 0,
    "wc.enabled": 0,
    "wc.input": "!DI3"
}
```

 - Any status code other than 200 is considered an invalid configuration.

# Builtin WEB server

## Goal

This module has builtin WEB server. The server allows to get and set values of the registers manually. This feature is necessary for local application control. For example local WEB page can control the Zontromat via tis server.

## Get register

Getting register means that client application can read the value of the target register by requesting information from the WEB server. This is done by making **HTTP-POST** request.

Example: http://ip-address:8890/api/v1/bgerp/registers/get

The body of the POST request is formatted in JSON.

Example: 
```json
{"token": "8niQyw7vH82eWy5r", "registers": ["sys.disc.free", "sys.disc.used"]}
```

The field registers holds the array of target names that should be returned from the WEB server. The response of te server is also formatted in JSON. Content type response header is added, **"Content-Type": "application/json; charset=utf-8"**.

Example:
```json
{"hvac.loop2_1.fan.min_speed": 5, "ac.zone_1_occupied": 0}
```

A "curl" example is provided for better comprehension of the request.

Example:
```sh
curl -v -XPOST -H 'Content-type: application/json' -d '{"token": "8niQyw7vH82eWy5r", "registers": ["sys.disc.free", "sys.disc.used"]}' 'http://192.168.0.52:8890/api/v1/bgerp/registers/get'
```

## Set register

Setting register means that client application can write value to the target register by sending information to the WEB server. This is done by making **HTTP-POST** request.

Example: http://ip-address:8890/api/v1/bgerp/registers/set

The body of the POST request is formatted in JSON.

Example: 
```json
{"token": "8niQyw7vH82eWy5r", "registers": {"hvac.loop2_1.fan.min_speed": 5, "ac.zone_1_occupied": 0}}
```

The field registers holds the dict of target names that should be set to specified values. A response is expected from the WEB server as shown below. The response of te server is also formatted in JSON. Content type response header is added, **"Content-Type": "application/json; charset=utf-8"**.

Example:
```json
{"hvac.loop2_1.fan.min_speed": 5, "ac.zone_1_occupied": 0}
```

A "curl" example is provided for better comprehension of the request.

Example:
```sh
curl -v -XPOST -H 'Content-type: application/json' -d '{"token": "8niQyw7vH82eWy5r", "registers": {"hvac.loop2_1.fan.min_speed": 0, "ac.zone_1_occupied": 0}}' 'http://192.168.0.52:8890/api/v1/bgerp/registers/set'
```
