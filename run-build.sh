#!/bin/bash

docker image rm -f hairdresserapp:1.0
docker build --no-cache -t hairdresserapp:1.0 .