#!/bin/bash

docker image rm -f hairdresserapp:1.1
docker build --no-cache -t hairdresserapp:1.1 .