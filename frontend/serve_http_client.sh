#!/bin/bash
###############################################################################
# Author: Agustin Bassi
# Project: blue-connection
# Date: June 2020
# Usage: Run it in the same folder where this file is
#
# $ ./run_ibeacon_scanner.sh "$PWD"/src app.py "$PWD"/db 5000 host
# 
###############################################################################

#########[ Settings & Data ]###################################################

# ARGUMENTS
HOST_DIR_TO_SERVE=$1
HOST_PORT=$2

# SETTINGS
CONTAINER_NAME=http-server
CONTAINER_DIR_TO_SERVE=/usr/local/apache2/htdocs/
CONTAINER_PORT=80
CONTAINER_NETWORK=host

IMAGE_NAME=httpd:2.4

#########[ Script commands ]###################################################

echo "{$CONTAINER_NAME serving:$HOST_APP_DIR at port $HOST_PORT}"  

docker run \
--rm \
--detach \
--name $CONTAINER_NAME \
--net $CONTAINER_NETWORK \
--publish $HOST_PORT:$CONTAINER_PORT \
--volume $HOST_DIR_TO_SERVE:$CONTAINER_DIR_TO_SERVE \
$IMAGE_NAME

#########[ Enf of file ]#######################################################
