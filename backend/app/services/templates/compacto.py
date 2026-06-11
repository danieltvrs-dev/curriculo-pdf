"""
Template Compacto: fontes menores, espacamentos enxutos, margens reduzidas.

Util para curriculos longos que precisam caber em 1 ou 2 paginas.
"""

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

from app.schemas import CurriculoEntrada
from app.services.templates.comum import gerar_documento

_ESTILOS = {
    "nome": ParagraphStyle(
        "Nome",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        spaceAfter=3,
        alignment=TA_LEFT,
    ),
    "contato": ParagraphStyle(
        "Contato",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        spaceAfter=8,
        textColor="#333333",
    ),
    "secao": ParagraphStyle(
        "Secao",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        spaceBefore=6,
        spaceAfter=4,
    ),
    "subtitulo": ParagraphStyle(
        "Subtitulo",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        spaceAfter=1,
    ),
    "periodo": ParagraphStyle(
        "Periodo",
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        spaceAfter=2,
        textColor="#555555",
    ),
    "corpo": ParagraphStyle(
        "Corpo",
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        spaceAfter=3,
    ),
    "tecnologias": ParagraphStyle(
        "Tecnologias",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        spaceAfter=5,
        textColor="#444444",
    ),
}


def gerar(curriculo: CurriculoEntrada) -> bytes:
    return gerar_documento(curriculo, _ESTILOS, margem=1.5 * cm)
