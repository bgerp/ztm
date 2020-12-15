# Light Log

A tool for logging the light level in case of Zontromat control system.
It is used to create a 24 or more hours log file that describes the light changes of the room that we study.
Later the file is used to create a light profile of the target room.

## Introduction

The tool is simple script that is called once every delta time depends of the density of the research.
The delta time can variate from 1 minute to 1 hour for example.
Every line of the log file is record of the level light.
The tool is made specially for the purpose of the project.

## Deploy

The tool is coming installed together with the main software part.
It is using crontab to be called.
To run the tool follow the steps.

 - Open a Crontab editor:
```sh
sudo crontab -e
```

 - Create time that the job (tool) will be called.
https://crontab-generator.org/

Use the following command for the job.
Note that the **--host** and **--device** flags should be set properly for the test case.
```sh
cd /opt/Zontromat/Zontromat/tests/ && python3 /opt/Zontromat/Zontromat/tests/light_log.py --host <YOUR HOST> --device <YOUR DEVICE ID> >/dev/null 2>&
```

Example:
cd /opt/Zontromat/Zontromat/tests/ && python3 /opt/Zontromat/Zontromat/tests/light_log.py --host 127.0.1.1 --device 26607314020000F8 >/dev/null 2>&

In this example the host is the same device that runs the system software.

 - Insert the command in to the 
```sh
* * * * * cd /opt/Zontromat/Zontromat/tests/ && python3 /opt/Zontromat/Zontromat/tests/light_log.py --host 127.0.1.1 --device 26607314020000F8 >/dev/null 2>1
```
