"""
Service de autenticacao.

Concentra duas responsabilidades:
- Hash de senha com bcrypt (via passlib)
- Geracao e validacao de JWT (via python-jose)

O secret, algoritmo e tempo de expiracao do JWT vem do .env. Nunca
hardcode esses valores.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    """Gera hash bcrypt da senha. Salt aleatorio e embutido no hash."""
    return _pwd_context.hash(senha)


def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    """Compara senha em texto puro com o hash. Retorna True se bate."""
    return _pwd_context.verify(senha, hash_armazenado)


def _config_jwt() -> tuple[str, str, int]:
    """Le secret, algoritmo e expiracao do .env. Falha alto se faltar secret."""
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET nao configurado. Veja backend/.env.example.")
    algoritmo = os.getenv("JWT_ALGORITHM", "HS256")
    expira_min = int(os.getenv("JWT_EXPIRA_MINUTOS", "10080"))  # 7 dias
    return secret, algoritmo, expira_min


def criar_token(user_id: int) -> str:
    """
    Gera um JWT com o id do usuario no `sub` e expiracao em `exp`.

    `sub` (subject) e o claim padrao do JWT pra identificar o dono do token.
    """
    secret, algoritmo, expira_min = _config_jwt()
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": agora,
        "exp": agora + timedelta(minutes=expira_min),
    }
    return jwt.encode(payload, secret, algorithm=algoritmo)


def decodificar_token(token: str) -> Optional[int]:
    """
    Valida o JWT e devolve o user_id. None se token e invalido ou expirado.
    """
    secret, algoritmo, _ = _config_jwt()
    try:
        payload = jwt.decode(token, secret, algorithms=[algoritmo])
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (JWTError, ValueError):
        return None
