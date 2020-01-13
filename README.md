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
