"""
Router de autenticacao.

Endpoints publicos: /registrar e /login.
Endpoint protegido: /me (exige token).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import Token, UserLogin, UserRegistro, UserResposta
from app.services import criar_token, gerar_hash_senha, verificar_senha

router = APIRouter()


@router.post(
    "/registrar",
    response_model=UserResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuario",
)
def registrar(dados: UserRegistro, db: Session = Depends(get_db)) -> User:
    # Email ja em uso?
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
    summary="Autentica usuario e devolve JWT",
)
def login(dados: UserLogin, db: Session = Depends(get_db)) -> Token:
    user = db.query(User).filter(User.email == dados.email).first()
    if user is None or not verificar_senha(dados.senha, user.senha_hash):
        # Mesma mensagem para "email nao existe" e "senha errada":
        # evita revelar a um atacante quais emails estao cadastrados.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos.",
        )

    token = criar_token(user.id)
    return Token(access_token=token)


@router.get(
    "/me",
    response_model=UserResposta,
    summary="Dados do usuario autenticado",
)
def me(user: User = Depends(get_current_user)) -> User:
    return user
