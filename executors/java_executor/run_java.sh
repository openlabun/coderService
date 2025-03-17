#!/bin/sh
mkdir -p /tmp/java
cp /app/Main.java /tmp/java/
cd /tmp/java

javac Main.java && java Main
