"""
Router de operacoes assistidas por IA.

Endpoints aqui fazem proxy seguro pro LLM: o frontend NUNCA toca a chave
da API, so o backend conhece. Cada endpoint mantem regras de validacao
(tamanhos minimos) pra evitar chamadas desperdicadas.
"""

from typing import Callable

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services import (
    melhorar_descricao_experiencia,
    melhorar_descricao_projeto,
    melhorar_resumo,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class MelhorarResumoEntrada(BaseModel):
    texto: str = Field(..., min_length=50, max_length=600)


class MelhorarDescricaoEntrada(BaseModel):
    texto: str = Field(..., min_length=10, max_length=500)
    contexto: str = Field(default="", max_length=240)


class TextoSaida(BaseModel):
    texto: str


# ---------------------------------------------------------------------------
# Helper de tratamento de erros
# ---------------------------------------------------------------------------


def _executar(funcao: Callable[..., str], **kwargs) -> TextoSaida:
    """Executa a funcao do service, traduzindo erros pra HTTPException."""
    try:
        resultado = funcao(**kwargs)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        mensagem = str(e)
        if "API key" in mensagem or "authentication" in mensagem.lower():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Chave da API do Google invalida ou ausente.",
            )
        if "quota" in mensagem.lower() or "rate" in mensagem.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de requisicoes atingido. Tente em instantes.",
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao chamar a IA: {mensagem}",
        )

    return TextoSaida(texto=resultado)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/melhorar-resumo",
    response_model=TextoSaida,
    summary="Reescreve o resumo profissional otimizado para ATS",
)
def endpoint_melhorar_resumo(dados: MelhorarResumoEntrada) -> TextoSaida:
    return _executar(melhorar_resumo, texto=dados.texto)


@router.post(
    "/melhorar-descricao-experiencia",
    response_model=TextoSaida,
    summary="Reescreve a descricao de uma experiencia profissional",
)
def endpoint_melhorar_descricao_experiencia(
    dados: MelhorarDescricaoEntrada,
) -> TextoSaida:
    return _executar(
        melhorar_descricao_experiencia,
        texto=dados.texto,
        contexto=dados.contexto,
    )


@router.post(
    "/melhorar-descricao-projeto",
    response_model=TextoSaida,
    summary="Reescreve a descricao de um projeto",
)
def endpoint_melhorar_descricao_projeto(
    dados: MelhorarDescricaoEntrada,
) -> TextoSaida:
    return _executar(
        melhorar_descricao_projeto,
        texto=dados.texto,
        contexto=dados.contexto,
    )
