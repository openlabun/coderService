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
  echo "Building python_executor image (with numpy and pandas)..."
  docker build -t python_executor executors/python_executor
fi

if ! docker image inspect node_executor > /dev/null 2>&1; then
  echo "Building node_executor image..."
  docker build -t node_executor executors/node_executor
fi

if ! docker image inspect java_executor > /dev/null 2>&1; then
  echo "Building java_executor image..."
  docker build -t java_executor executors/java_executor
fi

if ! docker image inspect c_executor > /dev/null 2>&1; then
  echo "Building c_executor image..."
  docker build -t c_executor executors/c_executor
fi

if ! docker image inspect cpp_executor > /dev/null 2>&1; then
  echo "Building cpp_executor image..."
  docker build -t cpp_executor executors/cpp_executor
fi

if ! docker image inspect ruby_executor > /dev/null 2>&1; then
  echo "Building ruby_executor image..."
  docker build -t ruby_executor executors/ruby_executor
fi

if ! docker image inspect php_executor > /dev/null 2>&1; then
  echo "Building php_executor image..."
  docker build -t php_executor executors/php_executor
fi

if ! docker image inspect csharp_executor > /dev/null 2>&1; then
  echo "Building csharp_executor image..."
  docker build -t csharp_executor executors/csharp_executor
fi

if ! docker image inspect go_executor > /dev/null 2>&1; then
  echo "Building go_executor image..."
  docker build -t go_executor executors/go_executor
fi

if ! docker image inspect r_executor > /dev/null 2>&1; then
  echo "Building r_executor image..."
  docker build -t r_executor executors/r_executor
fi

echo "Starting FastAPI service..."
uvicorn main:app --host 0.0.0.0 --port 8000
