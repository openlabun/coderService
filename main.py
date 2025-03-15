from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import docker
import tempfile
import os
import time

app = FastAPI(
    title="Coder service API",
    description="An API to compile and execute code in Python, JavaScript, Java, C, CPP, Ruby, PHP, C#, Go and R.",
    version="1.0.0"
)


# Enable CORS (adjust allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = docker.from_env()

class CodePayload(BaseModel):
    language: str
    code: str

# Mapping of supported languages with their file names and executor images
supported_languages = {
    "python": {"filename": "code.py", "image": "python_executor"},
    "javascript": {"filename": "code.js", "image": "node_executor"},
    "java": {"filename": "Main.java", "image": "java_executor"},
    "c": {"filename": "main.c", "image": "c_executor"},
    "cpp": {"filename": "main.cpp", "image": "cpp_executor"},
    "ruby": {"filename": "main.rb", "image": "ruby_executor"},
    "php": {"filename": "main.php", "image": "php_executor"},
    "csharp": {"filename": "main.cs", "image": "csharp_executor"},
    "go": {"filename": "main.go", "image": "go_executor"},
    "r": {"filename": "main.r", "image": "r_executor"}
}

@app.post("/execute")
def execute_code(payload: CodePayload):
    language = payload.language.lower()
    if language not in supported_languages:
        raise HTTPException(status_code=400, detail="Unsupported language.")

    config = supported_languages[language]
    filename = config["filename"]
    image = config["image"]

    # Write code to a temporary file
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, filename)
        with open(file_path, "w") as code_file:
            code_file.write(payload.code)
        
        # Start timer and run the container with resource limits and no network access
        start_time = time.time()
        try:
            container = client.containers.run(
                image=image,
                volumes={tmpdir: {'bind': '/app', 'mode': 'ro'}},
                detach=True,
                network_disabled=True,      # Disable networking inside the container
                mem_limit="100m",           # Limit memory usage
                cpu_period=100000,
                cpu_quota=50000             # Limit CPU usage (approx. 50% of one CPU)
            )
            container.wait(timeout=10)
            logs = container.logs().decode("utf-8")
            container.remove()
        except docker.errors.ContainerError as e:
            logs = str(e)
        except docker.errors.APIError as e:
            raise HTTPException(status_code=500, detail=f"Docker API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error executing code: {str(e)}")
        
        execution_time = time.time() - start_time

    return {"output": logs, "execution_time": execution_time}
