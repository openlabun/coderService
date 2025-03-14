# Dockerfile for csharp_executor
FROM mcr.microsoft.com/dotnet/sdk:5.0
WORKDIR /app
# Create a new console project, replace the Program.cs with the submitted code, then run it.
CMD dotnet new console -o app && cp main.cs app/Program.cs && dotnet run --project app
