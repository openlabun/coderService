# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
import tempfile
import os
import time

app = FastAPI()
client = docker.from_env()

class CodePayload(BaseModel):
    language: str
    code: str

@app.post("/execute")
def execute_code(payload: CodePayload):
    language = payload.language.lower()
    if language not in ["python", "js"]:
        raise HTTPException(status_code=400, detail="Unsupported language. Only 'python' and 'js' are supported.")

    # Select filename and executor image based on the language
    if language == "python":
        filename = "code.py"
        image = "python_executor"
    else:  # language == "js"
        filename = "code.js"
        image = "node_executor"

    # Write the submitted code to a temporary file
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, filename)
        with open(file_path, "w") as code_file:
            code_file.write(payload.code)

        # Run the executor container with the temporary directory mounted as read-only at /app
        start_time = time.time()
        try:
            container = client.containers.run(
                image=image,
                volumes={tmpdir: {'bind': '/app', 'mode': 'ro'}},
                detach=True,
                network_disabled=True,  # disable networking inside executor container
                mem_limit="100m",       # memory limit
                cpu_period=100000,
                cpu_quota=50000         # limit CPU usage (50% of one CPU)
            )
            container.wait(timeout=10)
            logs = container.logs().decode("utf-8")
            container.remove()  # cleanup
        except docker.errors.ContainerError as e:
            logs = str(e)
        except docker.errors.APIError as e:
            raise HTTPException(status_code=500, detail=f"Docker API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error executing code: {str(e)}")
        execution_time = time.time() - start_time

    return {"output": logs, "execution_time": execution_time}
