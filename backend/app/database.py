import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./curriculo_pdf.db",
)

# SQLite no Python tem uma restricao de threading que o FastAPI dispara.
# O check_same_thread=False desliga essa checagem. Outros bancos ignoram.
_connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(DATABASE_URL, future=True, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependencia FastAPI: cria uma sessao por request e fecha no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
