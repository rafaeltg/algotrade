#!/usr/bin/env bash

docker run -p 8086:8086 \
  -d \
  -e INFLUXDB_REPORTING_DISABLED=true \
  -e INFLUXDB_DATA_QUERY_LOG_ENABLED=false \
  -e INFLUXDB_DB='instruments' \
  -e INFLUXDB_USER='user' \
  -e INFLUXDB_USER_PASSWORD='123mudar' \
  -v $PWD:/var/lib/influxdb \
  --rm \
  --name ifdb \
  influxdb