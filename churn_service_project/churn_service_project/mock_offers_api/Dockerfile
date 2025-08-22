# Arquivo: ./mock_offers_api/Dockerfile

FROM python:3.10-slim
WORKDIR /app

RUN pip install --no-cache-dir "fastapi[all]"

# Copia o arquivo do servidor da API para a raiz do WORKDIR
COPY mock_offers_api/server.py .

EXPOSE 9000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]