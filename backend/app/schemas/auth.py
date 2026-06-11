"""
Schemas Pydantic de autenticacao.

Entrada do registro/login e saida dos endpoints.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegistro(BaseModel):
    """Entrada do POST /auth/registrar."""

    nome: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    senha: str = Field(..., min_length=8, max_length=72)


class UserLogin(BaseModel):
    """Entrada do POST /auth/login."""

    email: EmailStr
    senha: str = Field(..., min_length=1, max_length=72)


class UserResposta(BaseModel):
    """Saida em endpoints que devolvem dados do usuario. Nunca inclui senha."""

    id: int
    nome: str
    email: EmailStr
    criado_em: datetime

    # Permite Pydantic ler atributos de objeto SQLAlchemy diretamente.
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Saida do POST /auth/login."""

    access_token: str
    token_type: str = "bearer"
