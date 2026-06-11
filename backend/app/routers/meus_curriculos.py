"""
Router de curriculos persistidos do usuario logado.

Todas as rotas exigem JWT valido. Cada usuario so enxerga e altera os
proprios curriculos: a query sempre filtra por user_id.
"""

import re
import unicodedata

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Curriculo, User
from app.schemas import (
    CurriculoDetalhe,
    CurriculoEntrada,
    CurriculoResumo,
    CurriculoSalvarEntrada,
)
from app.services import gerar_pdf

router = APIRouter()


def _slug_arquivo(nome: str) -> str:
    nome_sem_acento = (
        unicodedata.normalize("NFKD", nome)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    nome_limpo = re.sub(r"\s+", "_", nome_sem_acento.lower().strip())
    nome_limpo = re.sub(r"[^a-z0-9_]", "", nome_limpo)
    return nome_limpo or "curriculo"


def _buscar_meu(db: Session, user_id: int, curriculo_id: int) -> Curriculo:
    """Busca curriculo do usuario ou 404. Centraliza a checagem de posse."""
    cv = (
        db.query(Curriculo)
        .filter(Curriculo.id == curriculo_id, Curriculo.user_id == user_id)
        .first()
    )
    if cv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curriculo nao encontrado.",
        )
    return cv


@router.get(
    "",
    response_model=list[CurriculoResumo],
    summary="Lista os curriculos salvos do usuario logado",
)
def listar(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Curriculo]:
    return (
        db.query(Curriculo)
        .filter(Curriculo.user_id == user.id)
        .order_by(Curriculo.atualizado_em.desc())
        .all()
    )


@router.post(
    "",
    response_model=CurriculoDetalhe,
    status_code=status.HTTP_201_CREATED,
    summary="Salva um novo curriculo",
)
def criar(
    dados: CurriculoSalvarEntrada,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Curriculo:
    cv = Curriculo(
        user_id=user.id,
        nome=dados.nome,
        dados=dados.dados.model_dump(mode="json"),
    )
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv


@router.get(
    "/{curriculo_id}",
    response_model=CurriculoDetalhe,
    summary="Detalhes de um curriculo salvo",
)
def detalhar(
    curriculo_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Curriculo:
    return _buscar_meu(db, user.id, curriculo_id)


@router.put(
    "/{curriculo_id}",
    response_model=CurriculoDetalhe,
    summary="Atualiza um curriculo salvo",
)
def atualizar(
    curriculo_id: int,
    dados: CurriculoSalvarEntrada,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Curriculo:
    cv = _buscar_meu(db, user.id, curriculo_id)
    cv.nome = dados.nome
    cv.dados = dados.dados.model_dump(mode="json")
    db.commit()
    db.refresh(cv)
    return cv


@router.delete(
    "/{curriculo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um curriculo salvo",
)
def deletar(
    curriculo_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    cv = _buscar_meu(db, user.id, curriculo_id)
    db.delete(cv)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{curriculo_id}/pdf",
    summary="Gera o PDF de um curriculo salvo",
    responses={
        200: {
            "description": "PDF do curriculo gerado",
            "content": {"application/pdf": {}},
        },
    },
)
def gerar_pdf_salvo(
    curriculo_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    cv = _buscar_meu(db, user.id, curriculo_id)
    entrada = CurriculoEntrada.model_validate(cv.dados)
    pdf_bytes = gerar_pdf(entrada)
    slug = _slug_arquivo(cv.nome)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{slug}.pdf"',
        },
    )
