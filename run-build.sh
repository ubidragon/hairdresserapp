#!/bin/bash

docker image rm -f hairdresserapp:0.2
docker build --no-cache -t hairdresserapp:0.2 .