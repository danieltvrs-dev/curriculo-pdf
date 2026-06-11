"""
Dependencias compartilhadas do FastAPI.

A funcao `get_current_user` e injetada em qualquer rota que precise de
autenticacao. Ela le o token do header Authorization, valida e devolve
o User do banco. Se algo der errado, retorna 401 imediatamente.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services import decodificar_token

# O tokenUrl e usado apenas pela documentacao do Swagger (botao Authorize).
# A validacao real e feita por nos no decodificar_token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas ou expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = decodificar_token(token)
    if user_id is None:
        raise credenciais_invalidas

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credenciais_invalidas

    return user
