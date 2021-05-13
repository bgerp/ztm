# DS2480B UART to 1Wire bus master

## Intro
The purpose of this driver is for controlling one wire devices over UART(USB).

This document is based on [official Dallas DS2480B](https://datasheets.maximintegrated.com/en/ds/DS2480B.pdf) bus driver.

Examples is focused on reading information from [temperature sensor DS18B20](https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf).

## Sequence 1

1. Sync the UART.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

2. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

3. Bus configuration commands.
- Pulldown slew rate control.
- Write one low time.
- Data sample offset and write 0 recovery time.
```
TX > 17 47 5F
RX < 16 46 5E
```

4. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

5. Send search command.
- Switch to data mode.
- Search ROM.
- Switch to command mode.
- Search accelerator control ON at regular speed.
- Switch to data mode.
- 16 bytes of empty data
- Switch to command mode.
- Search accelerator control OFF at regular speed.
```
TX > E1 F0 E3 B1 E1 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 E3 A1
RX < F0 80 08 AA AA A0 AA 00 A2 00 00 2A 02 0A 00 A8 88
```

6. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

7. Read DS18B20 power supply request.
- Switch to data mode.
- Skip ROM.
- Read power supply.
- Switch to command mode.
- Single bit read data at flex speed.
```
TX > E1 CC B4 E3 95
RX < CC B4 97
```

8. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

9. Perform DS18B20 temperature conversion request.
- Switch to data mode.
- Skip ROM.
- Convert.
```
TX > E1 CC 44
RX < CC 44
```

10. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

11. Read DS18B20 scratchpad request.
- Switch to data mode.
- Match ROM.
- Add ROM code (8).
- Read Scratchpad.
- Scratchpad 0xFF (9).
```
TX > E1 55 28 FF FC D0 00 17 03 AE BE FF FF FF FF FF FF FF FF FF
RX < 55 28 FF FC D0 00 17 03 AE BE 9C 01 4B 46 7F FF 0C 10 0C
```

## Sequence 2



1. Sync the UART.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

2. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

3. Bus configuration commands.
- Pulldown slew rate control.
- Write one low time.
- Data sample offset and write 0 recovery time.
```
TX > 17 47 5F
RX < 16 46 5E
```

4. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

5. Send search command.
- Switch to data mode.
- Search ROM.
- Switch to command mode.
- Search accelerator control ON at regular speed.
- Switch to data mode.
- 16 bytes of empty data.
- Switch to command mode.
- Search accelerator control OFF at regular speed.
```
TX > E1 F0 E3 B1 E1 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 E3 A1
RX < F0 00 02 80 82 08 A8 88 20 0A 00 80 00 00 00 8A A2
```

6. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

7. Read DS18B20 power supply request.
- Switch to data mode.
- Skip ROM.
- Read power supply.
- Switch to command mode.
- Single bit read data at flex speed.
```
TX > E1 CC B4 E3 95
RX < CC B4 97
```

8. Reset 1W bus.
- Switch to command mode.
- Reset at flex speed.
```
TX > E3 C5
RX < CD
```

9. Perform DS18B20 temperature conversion request.
- Switch to data mode.
- Skip ROM.
- Convert.
```
TX > E1 CC 44
RX < CC 44
```
