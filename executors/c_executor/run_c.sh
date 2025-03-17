#!/bin/sh
mkdir -p /tmp/c
cp /app/main.c /tmp/c/
cd /tmp/c
gcc main.c -o main && ./main
