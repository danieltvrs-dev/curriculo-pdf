"""
Router de curriculos.

O endpoint recebe os dados, gera o PDF e devolve o arquivo como download.
Toda a logica de geracao do PDF mora em app.services.gerador_pdf,
o router so cuida do contrato HTTP.
"""

import re
import unicodedata

from fastapi import APIRouter, Response, status

from app.schemas import CurriculoEntrada
from app.services import gerar_pdf

router = APIRouter()


def _slug_arquivo(nome: str) -> str:
    """
    Converte 'Daniel Tavares' em 'daniel_tavares'.

    Remove acentos, baixa caixa, troca espacos por underline e descarta
    qualquer caractere que nao seja alfanumerico ou underline.
    """
    nome_sem_acento = (
        unicodedata.normalize("NFKD", nome)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    nome_limpo = nome_sem_acento.lower().strip()
    nome_limpo = re.sub(r"\s+", "_", nome_limpo)
    nome_limpo = re.sub(r"[^a-z0-9_]", "", nome_limpo)
    return nome_limpo or "curriculo"


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Gera o PDF do curriculo a partir dos dados enviados",
    description=(
        "Recebe os dados do curriculo, valida via Pydantic e devolve "
        "o PDF gerado pronto para download."
    ),
    responses={
        201: {
            "description": "PDF do curriculo gerado",
            "content": {"application/pdf": {}},
        },
    },
)
def criar_curriculo(dados: CurriculoEntrada) -> Response:
    pdf_bytes = gerar_pdf(dados)
    slug = _slug_arquivo(dados.dados_pessoais.nome_completo)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="curriculo_{slug}.pdf"',
        },
    )
