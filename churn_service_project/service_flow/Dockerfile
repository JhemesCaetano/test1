# Arquivo: ./service_flow/Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY service_flow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service_flow/ ./service_flow
COPY common/ ./common

EXPOSE 8002
CMD ["uvicorn", "service_flow.server_service:app", "--host", "0.0.0.0", "--port", "8002"]