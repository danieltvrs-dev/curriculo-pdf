"""Template Classico: sobrio, maxima compatibilidade ATS."""

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

from app.schemas import CurriculoEntrada
from app.services.templates.comum import gerar_documento

_ESTILOS = {
    "nome": ParagraphStyle(
        "Nome",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceAfter=4,
        alignment=TA_LEFT,
    ),
    "contato": ParagraphStyle(
        "Contato",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        spaceAfter=14,
        textColor="#333333",
    ),
    "secao": ParagraphStyle(
        "Secao",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=10,
        spaceAfter=6,
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
    return gerar_documento(curriculo, _ESTILOS, margem=2 * cm)
