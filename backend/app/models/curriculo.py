"""
Modelo SQLAlchemy de Curriculo.

O campo `dados` guarda o JSON completo do CurriculoEntrada (schema Pydantic).
Em vez de normalizar cada bloco em tabelas separadas, mantemos o JSON inteiro:
e mais flexivel pra MVP e o curriculo so e usado todo de uma vez (gerar PDF).

`nome` e um apelido escolhido pelo usuario (ex: "CV Backend Junior", "CV Geral").
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Curriculo(Base):
    __tablename__ = "curriculos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    dados: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="curriculos")

    def __repr__(self) -> str:
        return f"<Curriculo id={self.id} nome={self.nome!r}>"
