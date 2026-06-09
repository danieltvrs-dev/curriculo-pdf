"""
Router de curriculos.

Por enquanto o endpoint apenas valida o JSON recebido e devolve o mesmo
objeto. A geracao do PDF entra na proxima peca (1.3): vamos isolar
problemas, um por vez.
"""

from fastapi import APIRouter, status

from app.schemas import CurriculoEntrada

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CurriculoEntrada,
    summary="Cria um curriculo a partir dos dados enviados",
    description=(
        "Recebe os dados do curriculo, valida via Pydantic e devolve o "
        "mesmo objeto serializado. Nao persiste em banco nem gera PDF ainda."
    ),
)
def criar_curriculo(dados: CurriculoEntrada) -> CurriculoEntrada:
    return dados
