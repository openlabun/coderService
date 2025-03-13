#!/bin/sh

# Start the Docker daemon in the background
dockerd-entrypoint.sh &

# Wait until the Docker daemon is ready
while(! docker info > /dev/null 2>&1); do
  echo "Waiting for Docker daemon to be available..."
  sleep 1
done

echo "Docker daemon is available."

# Build executor images if not already present
if ! docker image inspect python_executor > /dev/null 2>&1; then
  echo "Building python_executor image..."
  docker build -t python_executor executors/python_executor
fi

if ! docker image inspect node_executor > /dev/null 2>&1; then
  echo "Building node_executor image..."
  docker build -t node_executor executors/node_executor
fi

echo "Starting FastAPI service..."
uvicorn main:app --host 0.0.0.0 --port 8000
