# Dockerfile for python_executor
FROM python:3.8-slim
# Install numpy and pandas
RUN pip install --no-cache-dir numpy pandas
WORKDIR /app
# Expect the user code to be mounted as /app/code.py
CMD ["python", "code.py"]
