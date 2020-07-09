# Zontromat - Zonal Electronic Automation

## Introduction

Application that is based on Python 3.7.
Its purpose is to control automatically environment in defined zones.
This zones are aka Rooms/Offices/Spaces.

The application is provoking communication with specified server of bgERP.
Server is responsible to give configuration and parameters to this app,
immediately the application starts to control the choosen zones.

The main hardware controller behind this app is [UniPi Neuron M503](https://www.unipi.technology/unipi-neuron-m503-p104).

Software that is runnig on the controller is [Evok](https://www.unipi.technology/products/evok-47)

## Limitations

- Design of the system is strictly made for this particular application.
- Application support hardware only based on top of Neuron with latest version of Evok.

## Compatible Hardware

- Neuron S/M/L serias.

Note: Any other hardware will be suported on demand. If any other hardware is needed to be suported there is a speciffic HAL that enables that.

## License

This code is released under the [GPL3](https://www.gnu.org/licenses/gpl-3.0.html) License.

## Setup the software

1. Prepare the SD card:

- Use [Zontromat]() image, based on Rasppbian Strech.
- Flash the SD card. Use [dd](http://man7.org/linux/man-pages/man1/dd.1.html) for Linux or [Etcher](https://www.balena.io/etcher/) for Windows.

2. Configuring automatic update.

    Before put the SD card in the controller.
Open the FAT parttion and change the **/boot/zontromat.conf**.
The file is in following format:

        master_ip=your.salt.domain
        minion_id=random

 - master_ip is the IP address or domain of the SALT server.
 - minion_id is the ID of the controller. If it is left at random it takes a random string for ID. If you specifie something else, the ID is set ot specified string by the admin.

 3. Runing the application:

- Affter the configuration is done, place the SD card in to the controller.
- Power up the cabinet.
- Power up the controller.

## Redirect bgERP service

### Manual

 - All nacisery settings are placed ni settings.yaml the file is located: **/opt/Zontromat/Zontromat/settings.yaml**.

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

Sfter finisihngup replacment of the settings, please restart the service, to apply the new settings. This is done by typing in terminal

```sh
sudo systemctl restart zontromat.service
```

### With flash disc drive

This procedure alow maintainer to change the domains and settings of the Zontromat software by inserting flash disc drive in to the USB port of the controller.

 - After powering up the controller insert properly set flash disc in to the USB of the controller.
 - The controller software will take settings from the flash disc drive and replace the old one with this on in the USB drive.
 - After replacing the settings Zontromat service will be automatically restarted. This means that after restart new settings will take in mind.
 - Remove the USB disc drive.

