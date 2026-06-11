"""
Schemas dos curriculos persistidos do usuario logado.

CurriculoSalvarEntrada: o que o frontend manda pra criar/atualizar.
CurriculoResumo: dados leves pra listagem (sem o JSON inteiro).
CurriculoDetalhe: dados completos pra editar/visualizar.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.curriculo import CurriculoEntrada


class CurriculoSalvarEntrada(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    dados: CurriculoEntrada


class CurriculoResumo(BaseModel):
    id: int
    nome: str
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class CurriculoDetalhe(CurriculoResumo):
    dados: CurriculoEntrada
