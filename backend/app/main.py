import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import curriculo, ia

load_dotenv()

app = FastAPI(
    title="Gerador de Curriculo em PDF",
    description="API para gerar curriculos profissionais em PDF.",
    version="0.1.0",
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    curriculo.router,
    prefix="/curriculos",
    tags=["curriculos"],
)

app.include_router(
    ia.router,
    prefix="/ia",
    tags=["ia"],
)


@app.get("/")
def raiz():
    return {"mensagem": "API do Gerador de Curriculo em PDF esta no ar."}


@app.get("/saude")
def saude():
    return {"status": "ok"}
