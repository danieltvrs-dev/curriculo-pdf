"""
Registry de templates de PDF.

Cada template e um modulo com `gerar(curriculo) -> bytes`. O dicionario
TEMPLATES mapeia nome textual -> funcao, e e usado pelo gerador_pdf.py
para escolher dinamicamente.
"""

from app.services.templates import classico, compacto, moderno

TEMPLATES = {
    "classico": classico.gerar,
    "moderno": moderno.gerar,
    "compacto": compacto.gerar,
}

NOMES_VALIDOS = list(TEMPLATES.keys())
TEMPLATE_PADRAO = "classico"
