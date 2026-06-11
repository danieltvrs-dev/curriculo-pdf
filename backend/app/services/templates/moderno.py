"""
Template Moderno: nome e cabecalhos em azul, linha decorativa apos contato.

Ainda 100% ATS-friendly: cor e elemento visual, parser le o texto igual.
"""

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

from app.schemas import CurriculoEntrada
from app.services.templates.comum import gerar_documento

_COR_DESTAQUE = HexColor("#1e3a8a")  # azul escuro

_ESTILOS = {
    "nome": ParagraphStyle(
        "Nome",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=4,
        alignment=TA_LEFT,
        textColor=_COR_DESTAQUE,
    ),
    "contato": ParagraphStyle(
        "Contato",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        spaceAfter=2,
        textColor="#333333",
    ),
    "secao": ParagraphStyle(
        "Secao",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=12,
        spaceAfter=6,
        textColor=_COR_DESTAQUE,
    ),
    "subtitulo": ParagraphStyle(
        "Subtitulo",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        spaceAfter=2,
    ),
    "periodo": ParagraphStyle(
        "Periodo",
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        spaceAfter=3,
        textColor="#555555",
    ),
    "corpo": ParagraphStyle(
        "Corpo",
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=4,
    ),
    "tecnologias": ParagraphStyle(
        "Tecnologias",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        spaceAfter=8,
        textColor="#444444",
    ),
}


def gerar(curriculo: CurriculoEntrada) -> bytes:
    return gerar_documento(
        curriculo,
        _ESTILOS,
        margem=2 * cm,
        cor_destaque=_COR_DESTAQUE,
    )
