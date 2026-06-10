"""
Gerador de PDF do curriculo, layout ATS-friendly.

Estrategia:
- ReportLab Platypus (alto nivel): construimos uma lista de flowables
  e o SimpleDocTemplate cuida da paginacao automaticamente.
- Layout em uma unica coluna A4, fonte Helvetica padrao, margens de 2 cm.
- Cabecalhos de secao em MAIUSCULAS pra parser ATS identificar como
  delimitadores de bloco.
- Listas de tecnologias e habilidades como texto separado por virgula
  em paragrafo simples, NUNCA como tabela ou tags visuais (parser baga).
"""

from datetime import date
from io import BytesIO
from typing import Optional

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.schemas import (
    CurriculoEntrada,
    DadosPessoais,
    Experiencia,
    Formacao,
    Projeto,
)


# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------
# Centralizamos todos os ParagraphStyle aqui. Pra mudar a aparencia do
# curriculo inteiro, basta alterar estas constantes.

_estilo_nome = ParagraphStyle(
    "Nome",
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=20,
    spaceAfter=4,
    alignment=TA_LEFT,
)

_estilo_contato = ParagraphStyle(
    "Contato",
    fontName="Helvetica",
    fontSize=9,
    leading=12,
    spaceAfter=14,
    textColor="#333333",
)

_estilo_secao = ParagraphStyle(
    "Secao",
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    spaceBefore=10,
    spaceAfter=6,
)

_estilo_subtitulo = ParagraphStyle(
    "Subtitulo",
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=13,
    spaceAfter=2,
)

_estilo_periodo = ParagraphStyle(
    "Periodo",
    fontName="Helvetica-Oblique",
    fontSize=9,
    leading=12,
    spaceAfter=3,
    textColor="#555555",
)

_estilo_corpo = ParagraphStyle(
    "Corpo",
    fontName="Helvetica",
    fontSize=10,
    leading=13,
    spaceAfter=4,
)

_estilo_tecnologias = ParagraphStyle(
    "Tecnologias",
    fontName="Helvetica",
    fontSize=9,
    leading=12,
    spaceAfter=8,
    textColor="#444444",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _formata_data(d: Optional[date]) -> str:
    """Converte date em 'MM/AAAA'. None vira 'Atual'."""
    if d is None:
        return "Atual"
    return d.strftime("%m/%Y")


def _formata_periodo(inicio: date, fim: Optional[date]) -> str:
    return f"{_formata_data(inicio)} — {_formata_data(fim)}"


def _linha_contato(dados: DadosPessoais) -> str:
    """Monta a linha de contato no cabecalho, separada por bullets."""
    partes: list[str] = [dados.email, dados.telefone, dados.cidade]
    if dados.linkedin_url:
        partes.append(str(dados.linkedin_url))
    if dados.github_url:
        partes.append(str(dados.github_url))
    if dados.portfolio_url:
        partes.append(str(dados.portfolio_url))
    return " · ".join(partes)


def _bloco_experiencia(exp: Experiencia) -> list:
    blocos = [
        Paragraph(f"{exp.cargo} — {exp.empresa}", _estilo_subtitulo),
        Paragraph(_formata_periodo(exp.data_inicio, exp.data_fim), _estilo_periodo),
        Paragraph(exp.descricao, _estilo_corpo),
    ]
    if exp.tecnologias:
        blocos.append(
            Paragraph(
                "Tecnologias: " + ", ".join(exp.tecnologias),
                _estilo_tecnologias,
            )
        )
    return blocos


def _bloco_formacao(form: Formacao) -> list:
    return [
        Paragraph(f"{form.curso} ({form.nivel.value})", _estilo_subtitulo),
        Paragraph(form.instituicao, _estilo_corpo),
        Paragraph(_formata_periodo(form.data_inicio, form.data_fim), _estilo_periodo),
        Spacer(1, 4),
    ]


def _bloco_projeto(proj: Projeto) -> list:
    blocos = [
        Paragraph(proj.nome, _estilo_subtitulo),
        Paragraph(proj.descricao, _estilo_corpo),
    ]
    if proj.tecnologias:
        blocos.append(
            Paragraph(
                "Tecnologias: " + ", ".join(proj.tecnologias),
                _estilo_tecnologias,
            )
        )
    if proj.url:
        blocos.append(Paragraph(str(proj.url), _estilo_corpo))
    return blocos


# ---------------------------------------------------------------------------
# Funcao principal
# ---------------------------------------------------------------------------


def gerar_pdf(curriculo: CurriculoEntrada) -> bytes:
    """
    Monta o PDF do curriculo e devolve os bytes.

    Nao escreve em disco. O caller (rota HTTP, tarefa em background, script
    de testes) decide o que fazer com os bytes retornados.
    """
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"Curriculo - {curriculo.dados_pessoais.nome_completo}",
    )

    flowables: list = []

    # Cabecalho: nome + linha de contato
    flowables.append(
        Paragraph(curriculo.dados_pessoais.nome_completo, _estilo_nome)
    )
    flowables.append(
        Paragraph(_linha_contato(curriculo.dados_pessoais), _estilo_contato)
    )

    # Resumo profissional
    flowables.append(Paragraph("RESUMO PROFISSIONAL", _estilo_secao))
    flowables.append(Paragraph(curriculo.resumo_profissional, _estilo_corpo))

    # Experiencia profissional (so se houver)
    if curriculo.experiencias:
        flowables.append(Paragraph("EXPERIÊNCIA PROFISSIONAL", _estilo_secao))
        for exp in curriculo.experiencias:
            flowables.append(KeepTogether(_bloco_experiencia(exp)))

    # Formacao academica
    flowables.append(Paragraph("FORMAÇÃO ACADÊMICA", _estilo_secao))
    for form in curriculo.formacoes:
        flowables.append(KeepTogether(_bloco_formacao(form)))

    # Habilidades tecnicas: linha unica separada por virgula
    flowables.append(Paragraph("HABILIDADES TÉCNICAS", _estilo_secao))
    flowables.append(
        Paragraph(", ".join(curriculo.habilidades), _estilo_corpo)
    )

    # Projetos (so se houver)
    if curriculo.projetos:
        flowables.append(Paragraph("PROJETOS", _estilo_secao))
        for proj in curriculo.projetos:
            flowables.append(KeepTogether(_bloco_projeto(proj)))

    documento.build(flowables)
    return buffer.getvalue()
