from fastapi import FastAPI
import redis
from pydantic import BaseModel
from config import REDIS_URL
import json # Importar json


app = FastAPI()
r = redis.from_url(REDIS_URL)


# ---------------------------
# MODELOS DE DADOS
# ---------------------------

class Context(BaseModel):
    session_id: str
    owner: str


class Message(BaseModel):
    session_id: str
    role: str   # "user" ou "agent"
    content: str


class SessionData(BaseModel):
    session_id: str
    data: dict


# ---------------------------
# ROTAS DE CONTEXTO
# ---------------------------

@app.post("/set_context")
def set_context(data: Context):
    key = f"{data.session_id}:CONTEXT"
    r.set(key, data.owner)
    return {"status": "ok", "session_id": data.session_id, "owner": data.owner}


@app.get("/get_context/{session_id}")
def get_context(session_id: str):
    key = f"{session_id}:CONTEXT"
    val = r.get(key)
    return {"session_id": session_id, "owner": val.decode() if val else None}


# ---------------------------
# ROTAS DE HISTÓRICO DE CONVERSA
# ---------------------------

@app.post("/add_message")
def add_message(msg: Message):
    key = f"{msg.session_id}:HISTORY"
    entry = f"{msg.role}:{msg.content}"
    r.rpush(key, entry)
    return {"status": "ok"}


@app.get("/get_history/{session_id}")
def get_history(session_id: str):
    key = f"{session_id}:HISTORY"
    entries = r.lrange(key, 0, -1)
    history = [e.decode() for e in entries]
    return {"session_id": session_id, "history": history}


@app.delete("/clear_history/{session_id}")
def clear_history(session_id: str):
    key = f"{session_id}:HISTORY"
    r.delete(key)
    return {"status": "cleared", "session_id": session_id}


# ---------------------------
# ROTAS DE DADOS DA SESSÃO
# ---------------------------

@app.post("/set_session_data")
def set_session_data(payload: SessionData):
    """Salva um dicionário de dados para uma sessão específica."""
    key = f"{payload.session_id}:SESSION_DATA"
    # Converte o dicionário de dados para uma string JSON antes de salvar
    r.set(key, json.dumps(payload.data))
    return {"status": "ok", "session_id": payload.session_id}


@app.get("/get_session_data/{session_id}")
def get_session_data(session_id: str):
    """Recupera os dados de uma sessão específica."""
    key = f"{session_id}:SESSION_DATA"
    val = r.get(key)
    if val:
        # Decodifica e converte a string JSON de volta para um dicionário
        data = json.loads(val.decode())
        return {"session_id": session_id, "data": data}
    return {"session_id": session_id, "data": None}