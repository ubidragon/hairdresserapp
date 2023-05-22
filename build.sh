#!/bin/bash

docker image rm -f hairdresserapp:1.2
docker build --no-cache -t hairdresserapp:1.2 .
