#!/bin/bash

docker image rm -f hairdresserapp:0.1
docker build --no-cache -t hairdresserapp:0.1 .