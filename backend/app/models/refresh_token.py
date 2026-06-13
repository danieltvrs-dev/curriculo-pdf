"""
Modelo de RefreshToken.

Armazenamos o HASH (SHA-256) do refresh token, nunca o token em si.
Mesmo padrao usado para senhas: se o banco vazar, os tokens nao podem
ser usados diretamente.

`revogado_em` marca tokens invalidados manualmente (logout). Junto com
`expira_em`, define se o token e valido.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )
    expira_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revogado_em: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User")  # type: ignore  # noqa: F821

    def esta_valido(self, agora: datetime) -> bool:
        if self.revogado_em is not None:
            return False
        if self.expira_em <= agora:
            return False
        return True

    def __repr__(self) -> str:
        return f"<RefreshToken id={self.id} user_id={self.user_id}>"
