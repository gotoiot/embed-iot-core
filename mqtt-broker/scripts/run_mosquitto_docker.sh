#!/bin/bash
###############################################################################
# Author: Agustin Bassi
# Date: March 25, 2020
# Copyright: Globant Inc.
# Project: PagoChat
# Brief: TODO: Describe it
###############################################################################

#########[ Settings & Data ]###################################################

# General image settings
IMAGE_NAME=eclipse-mosquitto
CONTAINER_NAME=pago-chat-mosquitto
# Ports settings
MQTT_INTERNAL_CONTAINER_PORT=1883
MQTT_EXTERNAL_CONTAINER_PORT=1883
MQTTS_INTERNAL_CONTAINER_PORT=8883
MQTTS_EXTERNAL_CONTAINER_PORT=8883
# Host settings
HOST_MOSQUITTO_CONFIG_DIR=$1
HOST_MOSQUITTO_CERTS_DIR=$2
# Host settings
CONTAINER_MOSQUITTO_CONFIG_DIR=/mosquitto/config
CONTAINER_MOSQUITTO_CERTS_DIR=/mosquitto/certs

#########[ Module code ]#######################################################

echo ""
echo "Running $CONTAINER_NAME at port $MQTT_EXTERNAL_CONTAINER_PORT & $MQTTS_EXTERNAL_CONTAINER_PORT"
echo ""

docker run --rm -it \
--name $CONTAINER_NAME \
--publish $MQTT_EXTERNAL_CONTAINER_PORT:$MQTT_INTERNAL_CONTAINER_PORT \
--publish $MQTTS_EXTERNAL_CONTAINER_PORT:$MQTTS_INTERNAL_CONTAINER_PORT \
--volume $HOST_MOSQUITTO_CONFIG_DIR:$CONTAINER_MOSQUITTO_CONFIG_DIR \
--volume $HOST_MOSQUITTO_CERTS_DIR:$CONTAINER_MOSQUITTO_CERTS_DIR \
$IMAGE_NAME

#########[ End of file ]#######################################################