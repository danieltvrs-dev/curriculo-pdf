"""
Service de autenticacao.

Concentra tres responsabilidades:
- Hash de senha com bcrypt (via passlib)
- Geracao e validacao de access tokens JWT (via python-jose)
- Geracao de refresh tokens opacos (random + hash SHA-256 no banco)

O access token vai no header Authorization. O refresh token vai num
cookie httpOnly e e usado so para obter novos access tokens.
"""

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from jose import JWTError, jwt
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------------------------------------------
# Senhas
# ---------------------------------------------------------------------------


def gerar_hash_senha(senha: str) -> str:
    return _pwd_context.hash(senha)


def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    return _pwd_context.verify(senha, hash_armazenado)


# ---------------------------------------------------------------------------
# Access token (JWT)
# ---------------------------------------------------------------------------


def _config_jwt() -> Tuple[str, str, int]:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET nao configurado. Veja backend/.env.example.")
    algoritmo = os.getenv("JWT_ALGORITHM", "HS256")
    expira_min = int(os.getenv("ACCESS_TOKEN_EXPIRA_MINUTOS", "15"))
    return secret, algoritmo, expira_min


def criar_access_token(user_id: int) -> str:
    """JWT curto (15 min default) com user_id em `sub`."""
    secret, algoritmo, expira_min = _config_jwt()
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": agora,
        "exp": agora + timedelta(minutes=expira_min),
    }
    return jwt.encode(payload, secret, algorithm=algoritmo)


def decodificar_token(token: str) -> Optional[int]:
    """Valida access token. Retorna user_id ou None."""
    secret, algoritmo, _ = _config_jwt()
    try:
        payload = jwt.decode(token, secret, algorithms=[algoritmo])
        sub = payload.get("sub")
        if sub is None:
            return None
        return int(sub)
    except (JWTError, ValueError):
        return None


# Alias para retro-compatibilidade com codigo existente que importava
# criar_token diretamente.
criar_token = criar_access_token


# ---------------------------------------------------------------------------
# Refresh token (opaco)
# ---------------------------------------------------------------------------


def _config_refresh() -> int:
    return int(os.getenv("REFRESH_TOKEN_EXPIRA_MINUTOS", "43200"))


def gerar_refresh_token() -> Tuple[str, str, datetime]:
    """
    Cria um refresh token aleatorio.

    Retorna:
    - token: string opaca (vai pro cookie)
    - token_hash: SHA-256 (vai pro banco)
    - expira_em: datetime UTC

    O backend NUNCA armazena o token em texto puro, igual senha.
    """
    token = secrets.token_urlsafe(64)
    token_hash = hash_refresh_token(token)
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=_config_refresh())
    return token, token_hash, expira_em


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Cookie config
# ---------------------------------------------------------------------------


def config_cookie_refresh() -> dict:
    """
    Retorna kwargs para Response.set_cookie do refresh token.

    Valores vem do .env, para facilitar trocar em dev/producao sem mudar codigo.
    """
    return {
        "key": "refresh_token",
        "httponly": True,
        "secure": os.getenv("COOKIE_SECURE", "false").lower() == "true",
        "samesite": os.getenv("COOKIE_SAMESITE", "lax"),
        "path": "/",
        "max_age": _config_refresh() * 60,
    }
