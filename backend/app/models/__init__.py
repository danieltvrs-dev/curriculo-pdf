"""
Modelos SQLAlchemy.

IMPORTANTE: este __init__ importa todos os modelos para que o `create_all`
do main.py os enxergue pelo metadata. Se um modelo nao for importado em
algum momento antes do startup, sua tabela nao sera criada.
"""

from app.models.curriculo import Curriculo
from app.models.user import User

__all__ = ["User", "Curriculo"]
