# HHC-R4I4D IO Module

## Features

 - 4 opto-isolated inputs for dry contact input switch, not with voltage
 - 4 10A high current relay outputs.
 - Adoption RS485 interface, A popular protocol used industry MODBUS RTU protocol. You can easily embed the RS485 bus. An RS485 bus 32 modules can be attached.
 - Software set address and other parameters. Address and other parameters are stored in EEPROM.
 - Standard industrial rail mounting.
 - Anti aspiration design.
 - The power is not aspiration.
 - MODBUS standard provides test software.
 - Wide power supply 9-24V supply.

## Wiring instructions

| Index | Signal Name | Note |
|----------|:-------------|:-------------|
| 01 | +12V | 12V
| 02 | GND | GND
| 03 | NC | Empty, do not use a third group.
| 04 | 485A | RS485 are the first group of relay normally closed.
| 05 | 485B | RS486 negative.
| 07 | IN1 | Group 1 digital input.
| 09 | IN2 | Group 2 digital input.
| 11 | IN3 | Group 3 digital input.
| 13 | IN4 | Group 4 digital input.
| 14 | NO1 | Group 1 normally open relay.
| 15 | COM1 | Group 1 relay common.
| 16 | NC1 | Group 1 normally closed relay.
| 17 | NO2 | Group 2 normally open relay.
| 18 | COM2 | Group 2 relay common.
| 19 | NC2 | Group 2 normally closed relay.
| 20 | NO3 | Group 3 normally open relay.
| 21 | COM3 | Group 3 relay common.
| 22 | NC3 | Group 4 normally closed relay.
| 23 | NO4 | Group 4 normally open relay.
| 24 | COM4 | Group 4 relay common.
| 25 | NC4 | Group 4 normally closed relay.
| 26 | NC | Empty, do not use a third group.

## Software Agreement

 - UART: 9600 baud, A start bit, 8 data bits, one stop bit, invalid check digit.
 - Default Address: 0x01.
 - In line with MODBUS RTU protocol specification.

Detailed instructions (0x10 to address, for example)

### 1. Reading digital input

 - Send Command format: address (1 byte) + commands (one byte) + register address (two bytes) + data field (two bytes) + CRC check code (two bytes).

 - Data Returned Format: Address (1 byte) + commands (one byte) + returns the number (1 byte) + returned data (one byte) + CRC check code (two bytes) byte

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 02 | Function code | 0x02 (2) - Read Discrete Inputs |
| 00 20 | Starting address | 0x0021 (33) |
| 00 04 | Quantity | 0x0004 (4) |
| 78 03 | CRC | 0x7803 (30723) |
Send Package: 0x01, 0x02, 0x00, 0x20, 0x00, 0x04, 0x78, 0x03

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 02 | Function code | 0x02 (2) - Read Discrete Inputs |
| 01 | Byte count | 0x01 (1) |
| 0F | Status | On On On On Off Off Off Off |
| E1 8C | CRC | 0xE18C (57740) |
Returns Package: 0x01, 0x02, 0x01, 0x0F, 0xE1, 0x8c

Return Return 0x0F, This module only low four, only interested in the low four. From the first to the second 4, respectively, the digital input INPUT1 to INPUT4 state, when there is the digital input

When the signal, the corresponding bit is 0 if the first way switch input, there is no other way switch input, the value 0x0E.

## 2 Control relay outputs.

### 2.1 a control individual relay (assuming module 0x01)

 - Turn ON relay 1:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 10 | Output address | 0x0011 (17) |
| FF 00 | Output value | On |
| 8D FF | CRC | 0x8DFF (36351) |
Package: **0x01, 0x05, 0x00, 0x10, 0xFF, 0x00, 0x8D, 0xFF**

 - Turn ON relay 2: 

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 11 | Output address | 0x0012 (18) |
| FF 00 | Output value | On |
| DC 3F | CRC | 0xDC3F (56383) |
Package: **0x01, 0x05, 0x00, 0x11, 0xFF, 0x00, 0xDC, 0x3F**

 - Turn ON relay 3:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 12 | Output address | 0x0013 (19) |
| FF 00 | Output value | On |
| 2C 3F | CRC | 0x2C3F (11327) |
Package: **0x01, 0x05, 0x00, 0x12, 0xFF, 0x00, 0x2C, 0x3F**

 - Turn ON relay 4:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 13 | Output address | 0x0014 (20) |
| FF 00 | Output value | On |
| 7D FF | CRC | 0x7DFF (32255) |
Package: **0x01, 0x05, 0x00, 0x13, 0xFF, 0x00, 0x7D, 0xFF**

 - Turn OFF relay 1:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 10 | Output address | 0x0011 (17) |
| 00 00 | Output value | Off |
| CC 0F | CRC | 0xCC0F (52239) |
Package: **0x01, 0x05, 0x00, 0x10, 0x00, 0x00, 0xCC, 0x0F**

 - Turn OFF relay 2:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 11 | Output address | 0x0012 (18) |
| 00 00 | Output value | Off |
| 9D CF | CRC | 0x9DCF (40399) |
Package: **0x01, 0x05, 0x00, 0x11, 0x00, 0x00, 0x9D, 0xCF**

 - Turn OF relay 3:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1)
| 05 | Function code | 0x05 (5) - Write Single Coil
| 00 12 | Output address | 0x0013 (19)
| 00 00 | Output value | Off
| 6D CF | CRC | 0x6DCF (28111)
Package: **0x01, 0x05, 0x00, 0x12, 0x00, 0x00, 0x6D, 0xCF**

 - Turn OFF relay 4:

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 05 | Function code | 0x05 (5) - Write Single Coil |
| 00 13 | Output address | 0x0014 (20) |
| 00 00 | Output value | Off |
| 3C 0F | CRC | 0x3C0F (15375) |
Package: **0x01, 0x05, 0x00, 0x13, 0x00, 0x00, 0x3C, 0x0F**

### 2.2 all in one operation relay

 - Turn ON all

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 0F | Function code | 0x0F (15) - Write Multiple Coils |
| 00 10 | Starting address | 0x0011 (17) |
| 00 04 | Quantity | 0x0004 (4) |
| 01 | Byte count | 0x01 (1) |
| 0F | Outputs value | On On On On Off Off Off Off |
| BF 51 | CRC | 0xBF51 (48977) |
Package: **0x01, 0x0F, 0x00, 0x10, 0x00, 0x04, 0x01, 0x0F, 0xBF, 0x51**

 - Turn OFF all

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 0F | Function code | 0x0F (15) - Write Multiple Coils |
| 00 10 | Starting address | 0x0011 (17) |
| 00 04 | Quantity | 0x0004 (4) |
| 01 | Byte count | 0x01 (1) |
| 00 | Outputs value | Off Off Off Off Off Off Off Off |
| FF 55 | CRC | 0xFF55 (65365) |
Package: **0x01, 0x0F, 0x00, 0x10, 0x00, 0x04, 0x01, 0x00, 0xFF, 0x55**

 - Is set to open a two-way, set off the road thirty-four.

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 0F | Function code | 0x0F (15) - Write Multiple Coils |
| 00 10 | Starting address | 0x0011 (17) |
| 00 04 | Quantity | 0x0004 (4) |
| 01 | Byte count | 0x01 (1) |
| 03 | Outputs value | On On Off Off Off Off Off Off |
| BF 54 | CRC | 0xBF54 (48980) |
Package: **0x01, 0x0F, 0x00, 0x10, 0x00, 0x04, 0x01, 0x03, 0xBF, 0x54**

 - Set off a Road, the road home thirty-four open.

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 0F | Function code | 0x0F (15) - Write Multiple Coils |
| 00 10 | Starting address | 0x0011 (17) |
| 00 04 | Quantity | 0x0004 (4) |
| 01 | Byte count | 0x01 (1) |
| 00 | Outputs value | Off Off Off Off Off Off Off Off |
| FF 55 | CRC | 0xFF55 (65365) |
Package: **0x01, 0x0F, 0x00, 0x10, 0x00, 0x04, 0x01, 0x0C, 0xFF, 0x50**

## 3. Read relay output status

 - SendInstruction formatFormula: address (1 byte) + commands (one byte) + register address (two bytes) + data field (two bytes) + CRC check code (two bytes).
 - Data Returned Format: Address (1 byte) + commands (one byte) + returns the number (1 byte) + returned data (one byte) + CRC check code (two bytes) byte

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 01 | Function code | 0x01 (1) - Read Coils |
| 00 10 | Starting address | 0x0011 (17) |
| 00 04 | Quantity | 0x0004 (4) |
| 3C 0C | CRC | 0x3C0C (15372) |
Send Package: **0x01, 0x01, 0x00, 0x10, 0x00, 0x04, 0x3C, 0x0C**

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 01 | Slave address | 0x01 (1) |
| 01 | Function code | 0x01 (1) - Read Coils |
| 01 | Byte count | 0x01 (1) |
| 00 | Status | Off Off Off Off Off Off Off Off |
| 51 88 | CRC | 0x5188 (20872) |
Returns Package: **0x01, 0x01, 0x01, 0x00, 0x51, 0x88**

Return Back 0x00, status output relay, 0 is off, 1 is energized. This module only low four, only interested in the low four.

## 4. Setting the module address

 - Will change the device address to 1.

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
| 00 | Slave address | 0x00 (0) |
| 06 | Function code | 0x06 (6) - Write Single Register |
| 00 01 | Register address | 0x0002 (2) |
| 00 01 | Register value | 0x0001 (1) |
| 18 1B | CRC | 0x181B (6171) |
Package: **0x00, 0x06, 0x00, 0x01, 0x00, 0x01, 0x18, 0x1B**

## 5. Setting the module baud rate

 - Will change the device baud rate to 9600 (4).

| Part of Data Package | Description | Value |
|----------|:-------------|:-------------|
00 | Slave address | 0x00 (0)
06 | Function code | 0x06 (6) - Write Single Register
00 02 | Register address | 0x0003 (3)
00 04 | Register value | 0x0004 (4)
28 18 | CRC | 0x2818 (10264)
Package: **0x00, 0x06, 0x00, 0x02, 0x00, 0x04, 0x28, 0x18**

Baud rates
| Register Value | Baud Rate |
|----------|:-------------|
| 1 | 1200 |
| 2 | 2400 |
| 3 | 4800 |
| 4 | 9600 |
| 5 | 19200 |

If the value in this register is different then in the table the default value of 4 will be written.
