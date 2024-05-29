#!/bin/bash

PORT=4422
CONTAINER_NAME=flask_api

echo "Starting Docker container..."
docker start ${CONTAINER_NAME}