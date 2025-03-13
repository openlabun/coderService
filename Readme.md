```
docker build -f Dockerfile.fastapi -t fastapi_dind_executor .

docker run  --privileged -p 8000:8000 fastapi_dind_executor

cd frontend

docker build -t code_editor_frontend .

docker run -d -p 8080:80 code_editor_frontend
```

Test with 
```
curl.exe -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{ "language": "python", "code": "print(\"Hello World\")" }'
```
```
curl.exe -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{ "language": "python", "code": "print(\"Hello World\")\nprint(\"Second line\")" }'
```

