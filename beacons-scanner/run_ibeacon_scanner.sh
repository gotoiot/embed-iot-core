#!/bin/bash
###############################################################################
# Author: Agustin Bassi
# Project: Beacon scanner
# Date: June 2020
# Usage: Run it in the same folder where there is this file
#
# $ ./run_ibeacon_scanner.sh "$PWD"/src app.py "$PWD"/db 5000 host
# 
###############################################################################

#########[ Settings & Data ]###################################################

# ARGUMENTS
HOST_APP_DIR=$1
ENTRY_POINT=$2
HOST_DB_DIR=$3
HOST_PORT=$4
CONTAINER_NETWORK=$5

# SETTINGS
CONTAINER_NAME=beacons-scanner
CONTAINER_APP_DIR=/app/src
CONTAINER_DB_DIR=/app/db
CONTAINER_PORT=5000
COMMAND_TO_RUN="python $ENTRY_POINT"

IMAGE_NAME=local/beacons-scanner:latest

#########[ Script commands ]###################################################

echo "{$CONTAINER_NAME, app-dir:$HOST_APP_DIR, command:$COMMAND_TO_RUN, net:$CONTAINER_NETWORK}"  

docker run \
--rm \
--interactive \
--name $CONTAINER_NAME \
--net $CONTAINER_NETWORK \
--publish $HOST_PORT:$CONTAINER_PORT \
--volume $HOST_APP_DIR:$CONTAINER_APP_DIR \
--volume $HOST_DB_DIR:$CONTAINER_DB_DIR \
$IMAGE_NAME \
$COMMAND_TO_RUN

#########[ Enf of file ]#######################################################
