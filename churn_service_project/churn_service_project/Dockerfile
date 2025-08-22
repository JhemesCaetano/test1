# Arquivo: ./Dockerfile

FROM python:3.10-slim
WORKDIR /app

COPY churn_flow/requirements.txt churn_requirements.txt
COPY service_flow/requirements.txt service_requirements.txt
RUN pip install --no-cache-dir -r churn_requirements.txt -r service_requirements.txt

COPY common/ ./common
COPY churn_flow/ ./churn_flow
COPY service_flow/ ./service_flow

COPY main.py .
COPY master_workflow.py .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]