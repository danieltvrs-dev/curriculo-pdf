"""
Router de autenticacao com refresh token em cookie httpOnly.

Endpoints:
- POST /registrar  publico, cria usuario
- POST /login      publico, devolve access (body) + refresh (cookie)
- POST /refresh    publico (mas exige cookie), devolve novo access
- POST /logout     publico, revoga refresh do cookie
- GET  /me         protegido, dados do usuario
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import RefreshToken, User
from app.schemas import Token, UserLogin, UserRegistro, UserResposta
from app.services import (
    config_cookie_refresh,
    criar_access_token,
    gerar_hash_senha,
    gerar_refresh_token,
    hash_refresh_token,
    verificar_senha,
)

router = APIRouter()


def _emitir_refresh(db: Session, response: Response, user_id: int) -> None:
    """Cria refresh token novo, salva no banco e seta cookie na resposta."""
    token, token_hash, expira_em = gerar_refresh_token()
    db.add(
        RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expira_em=expira_em,
        )
    )
    db.commit()
    response.set_cookie(value=token, **config_cookie_refresh())


@router.post(
    "/registrar",
    response_model=UserResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuario",
)
def registrar(dados: UserRegistro, db: Session = Depends(get_db)) -> User:
    existente = db.query(User).filter(User.email == dados.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ja cadastrado.",
        )

    user = User(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Autentica usuario, devolve access (body) e refresh (cookie httpOnly)",
)
def login(
    dados: UserLogin,
    response: Response,
    db: Session = Depends(get_db),
) -> Token:
    user = db.query(User).filter(User.email == dados.email).first()
    if user is None or not verificar_senha(dados.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos.",
        )

    _emitir_refresh(db, response, user.id)
    access = criar_access_token(user.id)
    return Token(access_token=access)


@router.post(
    "/refresh",
    response_model=Token,
    summary="Troca refresh token (cookie) por novo access token",
)
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> Token:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token ausente.",
        )

    token_hash = hash_refresh_token(refresh_token)
    armazenado = (
        db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    )

    agora = datetime.now(timezone.utc)
    if armazenado is None or not armazenado.esta_valido(agora):
        # Token invalido/expirado: limpa cookie pra evitar loop
        response.delete_cookie("refresh_token", path="/")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalido ou expirado.",
        )

    # Rotacao: revoga o atual e emite um novo (defesa contra replay).
    armazenado.revogado_em = agora
    db.commit()
    _emitir_refresh(db, response, armazenado.user_id)

    access = criar_access_token(armazenado.user_id)
    return Token(access_token=access)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoga refresh token e limpa cookie",
)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> Response:
    if refresh_token:
        token_hash = hash_refresh_token(refresh_token)
        armazenado = (
            db.query(RefreshToken)
            .filter(RefreshToken.token_hash == token_hash)
            .first()
        )
        if armazenado and armazenado.revogado_em is None:
            armazenado.revogado_em = datetime.now(timezone.utc)
            db.commit()

    response.delete_cookie("refresh_token", path="/")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/me",
    response_model=UserResposta,
    summary="Dados do usuario autenticado",
)
def me(user: User = Depends(get_current_user)) -> User:
    return user
