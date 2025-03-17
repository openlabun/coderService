#!/bin/sh
mkdir -p /tmp/cpp
cp /app/main.cpp /tmp/cpp/
cd /tmp/cpp
g++ main.cpp -o main && ./main