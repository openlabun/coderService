from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import docker
import tempfile
import os
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = docker.from_env()

class CodePayload(BaseModel):
    language: str
    code: str

@app.post("/execute")
def execute_code(payload: CodePayload):
    language = payload.language.lower()
    if language not in ["python", "js"]:
        raise HTTPException(status_code=400, detail="Unsupported language. Only 'python' and 'js' are supported.")

    if language == "python":
        filename = "code.py"
        image = "python_executor"
    else:  # language == "js"
        filename = "code.js"
        image = "node_executor"

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, filename)
        with open(file_path, "w") as code_file:
            code_file.write(payload.code)

        start_time = time.time()
        try:
            container = client.containers.run(
                image=image,
                volumes={tmpdir: {'bind': '/app', 'mode': 'ro'}},
                detach=True,
                network_disabled=True,
                mem_limit="100m",
                cpu_period=100000,
                cpu_quota=50000
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
