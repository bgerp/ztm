# Zontromat - Zonal Electronic Automation

## Introduction

Application that is based on Python 3.7.
Its purpose is to control automatically environment in defined zones.
This zones are aka Rooms/Offices/Spaces.

The application is provoking communication with specified server of bgERP.
Server is responsible to give configuration and parameters to this app,
immediately the application starts to control the chosen zones.

## Limitations

- Design of the system is made for this particular application.
- Application supports multiple types of hardware controllers.

## Compatible Hardware

- Neuron S/M/L series.

Note: Any other hardware will be supported on demand. If any other hardware is needed to be supported there is a specific HAL that enables that.

[UniPi Neuron M503](https://www.unipi.technology/unipi-neuron-m503-p104)

[UniPi Neuron M523](https://www.unipi.technology/unipi-neuron-m523-p320)


Software that is running on the controller is [Evok](https://www.unipi.technology/products/evok-47)

 - PiCons X1BlackTitanium

Costume hardware made by POLYGON Team Ltd. Industrial Tablet powered by Raspberry Pi.

 - Zuljana zl101pcc

Costume hardware made by Zuljana. Industrial  Tablet powered by Intel x86.

## License

This code is released under the [GPL3](https://www.gnu.org/licenses/gpl-3.0.html) License.

## Setup the software

1. Prepare the SD card:

- Use [Zontromat]() image, based on Rasppbian Stretch.
- Flash the SD card. Use [dd](http://man7.org/linux/man-pages/man1/dd.1.html) for Linux or [Etcher](https://www.balena.io/etcher/) for Windows.

2. Configuring automatic update.

    Before put the SD card in the controller.
Open the FAT partition and change the **/boot/zontromat.conf**.
The file is in following format:

        master_ip=your.salt.domain
        minion_id=random

 - master_ip is the IP address or domain of the SALT server.
 - minion_id is the ID of the controller. If it is left at random it takes a random string for ID. If you specifies something else, the ID is set ot specified string by the admin.

 3. Running the application:

- After the configuration is done, place the SD card in to the controller.
- Power up the cabinet.
- Power up the controller.

## Redirect bgERP service

### Manual

 - All necessary settings are placed ni settings.ini the file is located: **/opt/Zontromat/settings.ini**.

 - The structure of the file is following:

```ini
[APPLICATION]
debug_level = 10
; CRITICAL 50
; ERROR 40
; WARNING 30
; INFO 20
; DEBUG 10
; NOTSET 0

; Hardware
[CONTROLLER]
timeout = 0.1

; Neuron Interface
; model = M503
; vendor = unipi
; host = http://176.33.1.207:8080

; PiCons Interface
; model = X1BlackTitanium
; vendor = pt
; host = http://admin:admin@176.33.1.254:8090

; Zuljana Interface
vendor = zuljana
model = zl101pcc
modbus_rtu_port_1 = COM10
modbus_rtu_baud_1 = 9600

; Remote ERP service.
[ERP_SERVICE]
config_time = 1594203916
erp_id = 0000-0000-0000-0000
host = https://ip.of.the.bgERP/
timeout = 5
```

This file is auto generated in the first time of the application start.
After its generation the application is killed.
It is not dependant of the version control.
This means that in moment of generation it will be with its default settings. And if you want to change something, you will be able by simply edit the file with your favorite text editor.

Some of the field are auto generated like "config_time". This field is used for automatic detection when was last time of generating configuration. The field is used mostly of automated methods. In case you want to change it manually we recommend to use:

```sh
 date +%s
```

The result of this command will give you a unix time stamp that is made from current local time of the device. The result looks like this: **1594203916**

After finishing up replacement of the settings, please restart the service, to apply the new settings. This is done by typing in terminal

```sh
sudo systemctl restart zontromat.service
```

### With flash disc drive

This procedure alow maintainer to change the domains and settings of the Zontromat software by inserting flash disc drive in to the USB port of the controller.

 - After powering up the controller insert properly set flash disc in to the USB of the controller.
 - The controller software will take settings from the flash disc drive and replace the old one with this on in the USB drive.
 - After replacing the settings Zontromat service will be automatically restarted. This means that after restart new settings will take in mind.
 - Remove the USB disc drive.

## Logs

1. Log content

In this head we will describe where to find logs of the Zontromat software.
Log files are automatically generate files by the Zontromat software.
The files has the following format:

```log
2021-07-19 10:33:51,369	INFO	zone	:227	Controller vendor(Bao Bao Industries) / model(ZL101PCC) 
2021-07-19 10:33:51,372	INFO	plugins.plugins_manager	:367	Found plugin: ac
2021-07-19 10:33:51,372	INFO	plugins.plugins_manager	:367	Found plugin: blinds
2021-07-19 10:33:51,373	INFO	plugins.plugins_manager	:367	Found plugin: ecc
2021-07-19 10:33:51,374	INFO	plugins.plugins_manager	:367	Found plugin: ecd
2021-07-19 10:33:51,374	INFO	plugins.plugins_manager	:367	Found plugin: echp
2021-07-19 10:33:51,375	INFO	plugins.plugins_manager	:367	Found plugin: envm
2021-07-19 10:33:51,375	INFO	plugins.plugins_manager	:367	Found plugin: hvac
2021-07-19 10:33:51,376	INFO	plugins.plugins_manager	:367	Found plugin: light
2021-07-19 10:33:51,376	INFO	plugins.plugins_manager	:367	Found plugin: monitoring
2021-07-19 10:33:51,377	INFO	plugins.plugins_manager	:367	Found plugin: sys
2021-07-19 10:33:51,377	INFO	plugins.plugins_manager	:367	Found plugin: vent
2021-07-19 10:33:51,403	INFO	zone	:342	ERP state: ERPState.Login
2021-07-19 10:33:51,659	INFO	zone	:517	Starting up the Zone
```

 - The first segment is date and time of the event: **2020-07-09 09:33:42,646**
 - The Second segment is level of the log of the event: **INFO**
 - The Third segment is the message source: **zone** (In this case name of the module.)
 - The fourth segment is line number of the event in the code: **:227**
 - And the fifth segment is the actual message: **Controller vendor(Bao Bao Industries) / model(ZL101PCC)**

2. Log location

The log files are located at: **/opt/Zontromat/logs**

1. Log name

The name of the file is formatted by the following way: **YYYYMMDD.log**
Example: **20200709.log**

4. Log level

The level of logging is placed in the setting.ini described in the previous head. In segment "application->debug_level" it can be changed.

Example:

```ini
[APPLICATION]
debug_level = 10
; CRITICAL 50
; ERROR 40
; WARNING 30
; INFO 20
; DEBUG 10
; NOTSET 0
```

## Application dependency graph

![](app_deps_graph.svg)

For generating the dependency graph you need to do the following steps.

  - Go to the main project directory
 ```sh
 cd zontromat
 ```

  - Call tha following module in **Windows**.
 ```sh
python -m pydeps .\zontromat\main.py --max-bacon 33 --cluster --max-cluster-size 101 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o .\doc\app_deps_graph.svg --show-deps >> .\doc\app_deps_graph.json
 ```
 
  - Call tha following module in **Linux**.
 ```sh
python3 -m pydeps .\zontromat\main.py --max-bacon 33 --cluster --max-cluster-size 101 --noise-level 33 --include-missing --keep-target-cluster --rmprefix data. services. bgERP. devices. controllers. plugins. utils. sys. -o .\doc\app_deps_graph.svg --show-deps >> .\doc\app_deps_graph.json
 ```
 
  - The result will be write ans SVG in **app_deps_graph.svg**

  ## Generate HTML documentation

  - Go to the main project directory
 ```sh
 cd zontromat
 ```

  - Call tha following module in **Windows**.
  ```sh
python -m pdoc .\Zontromat --html --skip-errors --force -o .\doc
  ```