# Compiler API
This is a simple API that can compile and run code in multiple languages. It uses FastAPI as the backend and Docker in Docker to run the code in a container. The frontend is a simple Vue.js app that sends the code to the backend and displays the output.

In the current version, the API supports Python, Node.

The editor is ace-builds (https://github.com/ajaxorg/ace-builds)

## Installation
```
docker build -f Dockerfile.fastapi -t coderservice-image .

docker run --privileged -d -it -p 5029:8000  -v dind-data:/var/lib/docker --restart unless-stopped --name coderService coderservice-image

```

## Usage
Test with 
```
python -m pytest test_backend.py
```


```
curl.exe -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{ "language": "python", "code": "print(\"Hello World\")" }'
```
```
curl.exe -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{ "language": "python", "code": "print(\"Hello World\")\nprint(\"Second line\")" }'
```

