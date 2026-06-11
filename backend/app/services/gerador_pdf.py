"""
Wrapper que escolhe o template e delega a geracao.

O codigo de cada template vive em app.services.templates.*. Este modulo
existe so para manter `from app.services import gerar_pdf` funcionando
de fora, e para fazer a validacao do nome do template.
"""

from app.schemas import CurriculoEntrada
from app.services.templates import NOMES_VALIDOS, TEMPLATE_PADRAO, TEMPLATES


def gerar_pdf(
    curriculo: CurriculoEntrada,
    template: str = TEMPLATE_PADRAO,
) -> bytes:
    """Gera o PDF do curriculo usando o template indicado."""
    funcao = TEMPLATES.get(template)
    if funcao is None:
        raise ValueError(
            f"Template invalido: {template!r}. Opcoes: {NOMES_VALIDOS}"
        )
    return funcao(curriculo)
