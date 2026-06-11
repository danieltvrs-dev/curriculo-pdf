"""
Router de operacoes assistidas por IA.

Endpoints aqui fazem proxy seguro pro LLM: o frontend NUNCA toca a chave
da API, so o backend conhece. Cada endpoint mantem regras de validacao
(tamanhos minimos) pra evitar chamadas desperdicadas.
"""

from anthropic import APIError, AuthenticationError, RateLimitError
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services import melhorar_resumo

router = APIRouter()


class MelhorarResumoEntrada(BaseModel):
    texto: str = Field(
        ...,
        min_length=50,
        max_length=600,
        description="Resumo profissional original que sera reescrito.",
    )


class MelhorarResumoSaida(BaseModel):
    texto: str = Field(..., description="Resumo reescrito pela IA.")


@router.post(
    "/melhorar-resumo",
    response_model=MelhorarResumoSaida,
    summary="Reescreve o resumo profissional otimizado para ATS",
)
def endpoint_melhorar_resumo(dados: MelhorarResumoEntrada) -> MelhorarResumoSaida:
    try:
        texto_melhorado = melhorar_resumo(dados.texto)
    except AuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chave da API da Anthropic invalida ou ausente.",
        )
    except RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite de requisicoes atingido. Tente novamente em instantes.",
        )
    except APIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao chamar a IA: {e.message}",
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return MelhorarResumoSaida(texto=texto_melhorado)
