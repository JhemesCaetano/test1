# Arquivo: ./churn_flow/Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY churn_flow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY churn_flow/ ./churn_flow
COPY common/ ./common

EXPOSE 8001
CMD ["uvicorn", "churn_flow.server_churn:app", "--host", "0.0.0.0", "--port", "8001"]