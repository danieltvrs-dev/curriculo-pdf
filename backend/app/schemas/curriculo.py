"""
Schemas Pydantic do curriculo.

Define a forma dos dados que chegam pelo formulario, com validacao automatica.
Cada classe descreve um bloco do curriculo. O objeto raiz e CurriculoEntrada,
que e o que a rota POST /curriculo vai esperar no corpo da requisicao.
"""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, model_validator


class NivelFormacao(str, Enum):
    """Niveis de formacao aceitos. Enum padroniza o valor no banco e no PDF."""

    TECNICO = "Tecnico"
    TECNOLOGO = "Tecnologo"
    GRADUACAO = "Graduacao"
    POS_GRADUACAO = "Pos-graduacao"
    MESTRADO = "Mestrado"
    DOUTORADO = "Doutorado"


class DadosPessoais(BaseModel):
    """Identificacao e contato. Tudo que o recrutador precisa pra te chamar."""

    nome_completo: str = Field(..., min_length=3, max_length=120)
    email: EmailStr
    telefone: str = Field(..., min_length=8, max_length=20)
    cidade: str = Field(..., min_length=2, max_length=80, description="Formato sugerido: Cidade/UF")
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None


class Experiencia(BaseModel):
    """
    Uma posicao profissional. data_fim None significa trabalho atual.

    O campo tecnologias e tratado como lista de palavras-chave: facilita
    o parsing por ATS, que costuma extrair termos tecnicos por proximidade
    com cabecalhos como "Tecnologias:" ou em listas separadas por virgula.
    """

    empresa: str = Field(..., min_length=2, max_length=120)
    cargo: str = Field(..., min_length=2, max_length=120)
    data_inicio: date
    data_fim: Optional[date] = None
    descricao: str = Field(..., min_length=10, max_length=500)
    tecnologias: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def valida_periodo(self) -> "Experiencia":
        if self.data_fim and self.data_fim < self.data_inicio:
            raise ValueError("data_fim nao pode ser anterior a data_inicio")
        return self


class Formacao(BaseModel):
    """Um curso/formacao academica. data_fim None significa em andamento."""

    instituicao: str = Field(..., min_length=2, max_length=120)
    curso: str = Field(..., min_length=2, max_length=120)
    nivel: NivelFormacao
    data_inicio: date
    data_fim: Optional[date] = None

    @model_validator(mode="after")
    def valida_periodo(self) -> "Formacao":
        if self.data_fim and self.data_fim < self.data_inicio:
            raise ValueError("data_fim nao pode ser anterior a data_inicio")
        return self


class Projeto(BaseModel):
    """Projeto pessoal ou academico relevante."""

    nome: str = Field(..., min_length=2, max_length=120)
    descricao: str = Field(..., min_length=10, max_length=500)
    tecnologias: list[str] = Field(default_factory=list)
    url: Optional[HttpUrl] = None


class CurriculoEntrada(BaseModel):
    """
    Objeto raiz da requisicao POST /curriculo.

    Reune todos os blocos do curriculo. Cada lista tem suas regras minimas:
    formacoes precisa de pelo menos 1, habilidades tambem (sao essenciais
    pro parsing por ATS). Experiencias e projetos podem vir vazias,
    pra acomodar quem esta comecando.
    """

    dados_pessoais: DadosPessoais
    resumo_profissional: str = Field(..., min_length=50, max_length=600)
    experiencias: list[Experiencia] = Field(default_factory=list)
    formacoes: list[Formacao] = Field(..., min_length=1)
    habilidades: list[str] = Field(..., min_length=1)
    projetos: list[Projeto] = Field(default_factory=list)
