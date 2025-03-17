#!/bin/sh
mkdir -p /tmp/csharp
cp /app/Program.cs /tmp/csharp/
cd /tmp/csharp
dotnet new console -o . --force && dotnet run
