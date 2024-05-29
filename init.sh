#!/bin/bash

IMAGE_NAME=my_python_app
PORT=4422
CONTAINER_NAME=flask_api

echo "Building Docker image..."
docker build -t ${IMAGE_NAME} .

if [ $? -ne 0 ]; then
  echo "Docker image build failed."
  exit 1
fi

echo "Docker image built successfully."

echo "Creating Docker container..."
CONTAINER_ID=$(docker create -p ${PORT}:5000 --name ${CONTAINER_NAME} ${IMAGE_NAME})

if [ $? -ne 0 ]; then
  echo "Failed to create Docker container."
  exit 1
fi

echo "Docker container created successfully with ID: ${CONTAINER_ID}. Now you do not need to run init.sh, only use start.sh"
