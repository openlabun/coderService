# Compiler API
This is a simple API that can compile and run code in multiple languages. It uses FastAPI as the backend and Docker in Docker to run the code in a container. The frontend is a simple Vue.js app that sends the code to the backend and displays the output.

In the current version, the API supports Python, Node.

The editor is ace-builds (https://github.com/ajaxorg/ace-builds)

## Installation
```
docker build -f Dockerfile.fastapi -t fastapi_dind_executor .

docker run  --privileged -p 8000:8000 fastapi_dind_executor

cd frontend

docker build -t code_editor_frontend .

docker run -d -p 8080:80 code_editor_frontend
```

## Usage
Test with 
```
curl.exe -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{ "language": "python", "code": "print(\"Hello World\")" }'
```
```
curl.exe -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{ "language": "python", "code": "print(\"Hello World\")\nprint(\"Second line\")" }'
```

