#!/bin/bash

SETTINGS_PATH="/opt/Zontromat/Zontromat/settings.yaml"
time=$(date +%s)

model=$(python3 /opt/Zontromat/info.py -m)

touch $SETTINGS_PATH
cat << EOF > $SETTINGS_PATH
#Application
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
  model: $model
  
# Remote server.
erp_service:

  # Remote server host address.
  host: https://test.bcvt.eu:443
  timeout: 5
  config_time: $time
  erp_id: 33
EOF
