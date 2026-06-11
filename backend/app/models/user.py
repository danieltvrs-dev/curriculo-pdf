"""
Modelo SQLAlchemy de Usuario.

Guardamos email, nome e senha_hash. A senha NUNCA e armazenada em texto puro:
o hash bcrypt e gerado pelo passlib no momento do cadastro.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.curriculo import Curriculo


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, index=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relacao 1-N: deletar usuario apaga curriculos juntos.
    curriculos: Mapped[list["Curriculo"]] = relationship(
        "Curriculo",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
