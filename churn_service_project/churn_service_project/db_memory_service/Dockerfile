FROM python:3.10-slim
WORKDIR /app
COPY db_memory_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# CORREÇÃO: Copia a pasta para dentro do WORKDIR
COPY db_memory_service/ .
# CORREÇÃO: O comando Uvicorn agora usa o nome do módulo
CMD ["uvicorn", "server_db:app", "--host", "0.0.0.0", "--port", "8000"]