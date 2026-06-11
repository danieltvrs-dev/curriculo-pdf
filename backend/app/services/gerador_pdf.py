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
- Todo texto vindo do usuario passa por escape de HTML antes de virar
  Paragraph. Quebras de linha sao preservadas em campos de texto livre.
"""

import html
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
    Certificacao,
    CurriculoEntrada,
    DadosPessoais,
    Experiencia,
    Formacao,
    Idioma,
    Projeto,
)


# ---------------------------------------------------------------------------
# Helpers de seguranca de texto
# ---------------------------------------------------------------------------
# Tudo que vem do usuario precisa passar por aqui ANTES de virar Paragraph.
# Sem escape, caracteres como '<' quebram o parser do ReportLab.


def _escapa(texto: str) -> str:
    """Escapa caracteres especiais de HTML (& < >) pra Paragraph seguro."""
    return html.escape(texto, quote=False)


def _escapa_multiline(texto: str) -> str:
    """
    Escapa HTML e converte quebras de linha do usuario em <br/>.

    Usado em campos de texto livre (resumo profissional, descricao
    de experiencia, descricao de projeto), onde preservar paragrafos
    do usuario importa pra legibilidade.
    """
    return _escapa(texto).replace("\n", "<br/>")


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
# Helpers de formatacao
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
    partes: list[str] = [
        _escapa(dados.email),
        _escapa(dados.telefone),
        _escapa(dados.cidade),
    ]
    if dados.linkedin_url:
        partes.append(_escapa(str(dados.linkedin_url)))
    if dados.github_url:
        partes.append(_escapa(str(dados.github_url)))
    if dados.portfolio_url:
        partes.append(_escapa(str(dados.portfolio_url)))
    return " · ".join(partes)


def _lista_tecnologias(tecs: list[str]) -> str:
    """Junta tecnologias separadas por virgula, ja escapadas."""
    return ", ".join(_escapa(t) for t in tecs)


def _bloco_experiencia(exp: Experiencia) -> list:
    blocos = [
        Paragraph(
            f"{_escapa(exp.cargo)} — {_escapa(exp.empresa)}",
            _estilo_subtitulo,
        ),
        Paragraph(_formata_periodo(exp.data_inicio, exp.data_fim), _estilo_periodo),
        Paragraph(_escapa_multiline(exp.descricao), _estilo_corpo),
    ]
    if exp.tecnologias:
        blocos.append(
            Paragraph(
                "Tecnologias: " + _lista_tecnologias(exp.tecnologias),
                _estilo_tecnologias,
            )
        )
    return blocos


def _bloco_formacao(form: Formacao) -> list:
    return [
        Paragraph(
            f"{_escapa(form.curso)} ({_escapa(form.nivel.value)})",
            _estilo_subtitulo,
        ),
        Paragraph(_escapa(form.instituicao), _estilo_corpo),
        Paragraph(_formata_periodo(form.data_inicio, form.data_fim), _estilo_periodo),
        Spacer(1, 4),
    ]


def _bloco_projeto(proj: Projeto) -> list:
    blocos = [
        Paragraph(_escapa(proj.nome), _estilo_subtitulo),
        Paragraph(_escapa_multiline(proj.descricao), _estilo_corpo),
    ]
    if proj.tecnologias:
        blocos.append(
            Paragraph(
                "Tecnologias: " + _lista_tecnologias(proj.tecnologias),
                _estilo_tecnologias,
            )
        )
    if proj.url:
        blocos.append(Paragraph(_escapa(str(proj.url)), _estilo_corpo))
    return blocos


def _linha_idioma(idi: Idioma) -> str:
    return f"{_escapa(idi.idioma)} — {_escapa(idi.nivel.value)}"


def _bloco_certificacao(cert: Certificacao) -> list:
    cabecalho = _escapa(cert.nome)
    detalhe_partes: list[str] = [_escapa(cert.instituicao)]
    if cert.ano is not None:
        detalhe_partes.append(str(cert.ano))
    detalhe = " · ".join(detalhe_partes)

    blocos = [
        Paragraph(cabecalho, _estilo_subtitulo),
        Paragraph(detalhe, _estilo_corpo),
    ]
    if cert.url:
        blocos.append(Paragraph(_escapa(str(cert.url)), _estilo_tecnologias))
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
        Paragraph(_escapa(curriculo.dados_pessoais.nome_completo), _estilo_nome)
    )
    flowables.append(
        Paragraph(_linha_contato(curriculo.dados_pessoais), _estilo_contato)
    )

    # Resumo profissional
    flowables.append(Paragraph("RESUMO PROFISSIONAL", _estilo_secao))
    flowables.append(
        Paragraph(_escapa_multiline(curriculo.resumo_profissional), _estilo_corpo)
    )

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
        Paragraph(_lista_tecnologias(curriculo.habilidades), _estilo_corpo)
    )

    # Projetos (so se houver)
    if curriculo.projetos:
        flowables.append(Paragraph("PROJETOS", _estilo_secao))
        for proj in curriculo.projetos:
            flowables.append(KeepTogether(_bloco_projeto(proj)))

    # Idiomas (so se houver): linha unica com "Idioma — Nivel" separados por ·
    if curriculo.idiomas:
        flowables.append(Paragraph("IDIOMAS", _estilo_secao))
        linha = " · ".join(_linha_idioma(idi) for idi in curriculo.idiomas)
        flowables.append(Paragraph(linha, _estilo_corpo))

    # Certificacoes (so se houver)
    if curriculo.certificacoes:
        flowables.append(Paragraph("CERTIFICAÇÕES", _estilo_secao))
        for cert in curriculo.certificacoes:
            flowables.append(KeepTogether(_bloco_certificacao(cert)))

    documento.build(flowables)
    return buffer.getvalue()
