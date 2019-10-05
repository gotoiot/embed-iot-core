#!/bin/bash
CONTAINER_NAME=php-server
APP_DIR=$1
HOST_PORT=$2

echo "Serving PHP files {container:$CONTAINER_NAME, app-dir:$APP_DIR, port:$HOST_PORT}"

docker run --rm --volume $APP_DIR:/usr/src/app --interactive --name $CONTAINER_NAME -p $HOST_PORT:8080 abassi/php-server:latest