"""
Codigo compartilhado entre os templates de PDF.

Cada template fornece seu proprio dicionario de ParagraphStyles. As funcoes
aqui aplicam o mesmo "esqueleto" (cabecalho, secoes, listas) usando esses
estilos, evitando duplicacao.
"""

import html
from datetime import date
from io import BytesIO
from typing import Optional

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
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
# Helpers de texto
# ---------------------------------------------------------------------------


def escapa(texto: str) -> str:
    return html.escape(texto, quote=False)


def escapa_multiline(texto: str) -> str:
    return escapa(texto).replace("\n", "<br/>")


def formata_data(d: Optional[date]) -> str:
    if d is None:
        return "Atual"
    return d.strftime("%m/%Y")


def formata_periodo(inicio: date, fim: Optional[date]) -> str:
    return f"{formata_data(inicio)} — {formata_data(fim)}"


def linha_contato(dados: DadosPessoais) -> str:
    partes: list[str] = [escapa(dados.email), escapa(dados.telefone), escapa(dados.cidade)]
    if dados.linkedin_url:
        partes.append(escapa(str(dados.linkedin_url)))
    if dados.github_url:
        partes.append(escapa(str(dados.github_url)))
    if dados.portfolio_url:
        partes.append(escapa(str(dados.portfolio_url)))
    return " · ".join(partes)


def lista_tecnologias(tecs: list[str]) -> str:
    return ", ".join(escapa(t) for t in tecs)


def linha_idioma(idi: Idioma) -> str:
    return f"{escapa(idi.idioma)} — {escapa(idi.nivel.value)}"


# ---------------------------------------------------------------------------
# Blocos parametrizados por estilos
# ---------------------------------------------------------------------------


def bloco_experiencia(exp: Experiencia, estilos: dict) -> list:
    blocos = [
        Paragraph(f"{escapa(exp.cargo)} — {escapa(exp.empresa)}", estilos["subtitulo"]),
        Paragraph(formata_periodo(exp.data_inicio, exp.data_fim), estilos["periodo"]),
        Paragraph(escapa_multiline(exp.descricao), estilos["corpo"]),
    ]
    if exp.tecnologias:
        blocos.append(
            Paragraph(
                "Tecnologias: " + lista_tecnologias(exp.tecnologias),
                estilos["tecnologias"],
            )
        )
    return blocos


def bloco_formacao(form: Formacao, estilos: dict) -> list:
    return [
        Paragraph(f"{escapa(form.curso)} ({escapa(form.nivel.value)})", estilos["subtitulo"]),
        Paragraph(escapa(form.instituicao), estilos["corpo"]),
        Paragraph(formata_periodo(form.data_inicio, form.data_fim), estilos["periodo"]),
        Spacer(1, 4),
    ]


def bloco_projeto(proj: Projeto, estilos: dict) -> list:
    blocos = [
        Paragraph(escapa(proj.nome), estilos["subtitulo"]),
        Paragraph(escapa_multiline(proj.descricao), estilos["corpo"]),
    ]
    if proj.tecnologias:
        blocos.append(
            Paragraph(
                "Tecnologias: " + lista_tecnologias(proj.tecnologias),
                estilos["tecnologias"],
            )
        )
    if proj.url:
        blocos.append(Paragraph(escapa(str(proj.url)), estilos["corpo"]))
    return blocos


def bloco_certificacao(cert: Certificacao, estilos: dict) -> list:
    detalhe_partes: list[str] = [escapa(cert.instituicao)]
    if cert.ano is not None:
        detalhe_partes.append(str(cert.ano))
    blocos = [
        Paragraph(escapa(cert.nome), estilos["subtitulo"]),
        Paragraph(" · ".join(detalhe_partes), estilos["corpo"]),
    ]
    if cert.url:
        blocos.append(Paragraph(escapa(str(cert.url)), estilos["tecnologias"]))
    return blocos


# ---------------------------------------------------------------------------
# Montagem do PDF
# ---------------------------------------------------------------------------


def montar_flowables(
    curriculo: CurriculoEntrada,
    estilos: dict,
    cor_destaque: Optional[Color] = None,
) -> list:
    """
    Constroi a lista de flowables do PDF, igual em estrutura para todos
    os templates. Os estilos (e a cor de destaque opcional) e o que muda.
    """
    flowables: list = []

    flowables.append(Paragraph(escapa(curriculo.dados_pessoais.nome_completo), estilos["nome"]))
    flowables.append(Paragraph(linha_contato(curriculo.dados_pessoais), estilos["contato"]))

    if cor_destaque is not None:
        flowables.append(
            HRFlowable(
                width="100%",
                thickness=1.5,
                color=cor_destaque,
                spaceBefore=2,
                spaceAfter=10,
            )
        )

    flowables.append(Paragraph("RESUMO PROFISSIONAL", estilos["secao"]))
    flowables.append(Paragraph(escapa_multiline(curriculo.resumo_profissional), estilos["corpo"]))

    if curriculo.experiencias:
        flowables.append(Paragraph("EXPERIÊNCIA PROFISSIONAL", estilos["secao"]))
        for exp in curriculo.experiencias:
            flowables.append(KeepTogether(bloco_experiencia(exp, estilos)))

    flowables.append(Paragraph("FORMAÇÃO ACADÊMICA", estilos["secao"]))
    for form in curriculo.formacoes:
        flowables.append(KeepTogether(bloco_formacao(form, estilos)))

    flowables.append(Paragraph("HABILIDADES TÉCNICAS", estilos["secao"]))
    flowables.append(Paragraph(lista_tecnologias(curriculo.habilidades), estilos["corpo"]))

    if curriculo.projetos:
        flowables.append(Paragraph("PROJETOS", estilos["secao"]))
        for proj in curriculo.projetos:
            flowables.append(KeepTogether(bloco_projeto(proj, estilos)))

    if curriculo.idiomas:
        flowables.append(Paragraph("IDIOMAS", estilos["secao"]))
        linha = " · ".join(linha_idioma(idi) for idi in curriculo.idiomas)
        flowables.append(Paragraph(linha, estilos["corpo"]))

    if curriculo.certificacoes:
        flowables.append(Paragraph("CERTIFICAÇÕES", estilos["secao"]))
        for cert in curriculo.certificacoes:
            flowables.append(KeepTogether(bloco_certificacao(cert, estilos)))

    return flowables


def gerar_documento(
    curriculo: CurriculoEntrada,
    estilos: dict,
    margem: float = 2 * cm,
    cor_destaque: Optional[Color] = None,
) -> bytes:
    """Cria o documento PDF inteiro e devolve os bytes."""
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=margem,
        rightMargin=margem,
        topMargin=margem,
        bottomMargin=margem,
        title=f"Curriculo - {curriculo.dados_pessoais.nome_completo}",
    )
    flowables = montar_flowables(curriculo, estilos, cor_destaque)
    documento.build(flowables)
    return buffer.getvalue()
