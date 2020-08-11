# Zontromat - Zonal Electronic Automation

## Introduction

Application that is based on Python 3.7.
Its purpose is to control automatically environment in defined zones.
This zones are aka Rooms/Offices/Spaces.

The application is provoking communication with specified server of bgERP.
Server is responsible to give configuration and parameters to this app,
immediately the application starts to control the chosen zones.

The main hardware controller behind this app is [UniPi Neuron M503](https://www.unipi.technology/unipi-neuron-m503-p104).

Software that is running on the controller is [Evok](https://www.unipi.technology/products/evok-47)

## Limitations

- Design of the system is strictly made for this particular application.
- Application support hardware only based on top of Neuron with latest version of Evok.

## Compatible Hardware

- Neuron S/M/L series.

Note: Any other hardware will be supported on demand. If any other hardware is needed to be supported there is a specific HAL that enables that.

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

 - All necessary settings are placed ni settings.yaml the file is located: **/opt/Zontromat/Zontromat/settings.yaml**.

 - The structure of the file is following:

```yaml
# Application
application:

  # CRITICAL 50
  # ERROR 40
  # WARNING 30
  # INFO 20
  # DEBUG 10
  # NOTSET 0
  debug_level: 10

# Hardware
controller:

  # IP address of the hardware. It will be replaced with 127.0.0.1
  host: http://localhost:8080
  timeout: 5
  vendor: unipi
  model: M503
  
# Remote server.
erp_service:

  # Remote server host address.
  host: http://bcvt.eu
  timeout: 5
  config_time: 1594203916

```
This file is auto generated and it is not dependant of version control.
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
2020-07-09 09:33:42,646	INFO	__main__	Starting
2020-07-09 09:33:42,649	INFO	plugins.status_led.status_led	Starting up the Status LED
2020-07-09 09:33:42,654	INFO	zone	Zone state: ZoneState.Init
```

 - The first segment is date and time of the event: **2020-07-09 09:33:42,646**
 - The Second segment is level of the log of the event: **INFO**
 - The Third segment is the message source: **__main__**
(In this case name of the module.)
 - And the fourth segment is the actual message: **Starting**

2. Log location

The log files are located at: **/opt/Zontromat/Zontromat/logs**

3. Log name

The name of the file is formatted by the following way: **YYYYMMDD.log**
Example: **20200709.log**

4. Log level

The level of logging is placed in the setting.yaml described in the previous head. In segment "application->debug_level" it can be changed.

Example:

```yaml
application:

  # CRITICAL 50
  # ERROR 40
  # WARNING 30
  # INFO 20
  # DEBUG 10
  # NOTSET 0
  debug_level: 10
```
