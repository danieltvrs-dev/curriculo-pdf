"""
Service de melhoria de textos via Google Gemini.

Recebe um texto cru, devolve uma versao reescrita otimizada para ATS,
mantendo o sentido original e respeitando os limites de tamanho.

Configuracao via .env:
- GOOGLE_API_KEY: chave do Google AI Studio (free tier oficial)
- GEMINI_MODEL: modelo (default gemini-2.5-flash)
"""

import os

from google import genai

_MODELO_PADRAO = "gemini-2.5-flash"

_INSTRUCAO_RESUMO = """\
Voce e um especialista em curriculos brasileiros otimizados para sistemas \
ATS (Applicant Tracking Systems).

Sua tarefa: reescrever o "resumo profissional" abaixo de forma mais clara, \
densa em palavras-chave tecnicas relevantes para a area do candidato, e \
adequada para parsing automatizado por ATS.

Regras:
- Mantenha o sentido original e o tom da pessoa.
- NAO invente experiencias, formacoes, tecnologias ou cargos que nao foram \
mencionados.
- Use entre 50 e 600 caracteres no resultado.
- Use linguagem profissional, direta, sem cliches.
- Escreva em portugues brasileiro.
- Inclua naturalmente palavras-chave tecnicas presentes ou implicitas no \
texto original.
- NAO use marcacao Markdown nem emojis.

Devolva APENAS o texto reescrito, sem nenhuma introducao, comentario, aspas \
ou explicacao. Apenas o paragrafo final.

Texto original:
\"\"\"
{texto}
\"\"\"\
"""


_INSTRUCAO_DESCRICAO_EXPERIENCIA = """\
Voce e um especialista em curriculos brasileiros otimizados para sistemas \
ATS (Applicant Tracking Systems).

Sua tarefa: reescrever a descricao das atividades de uma experiencia \
profissional, deixando-a mais clara, com verbos de acao no presente ou \
passado, densa em palavras-chave tecnicas, e adequada para parsing por ATS.

Contexto do cargo: {contexto}

Regras:
- Mantenha as MESMAS atividades e tecnologias mencionadas. NAO invente \
realizacoes, numeros, metricas, tecnologias ou clientes.
- Use entre 10 e 500 caracteres no resultado.
- Comece cada frase com verbo de acao quando possivel (Desenvolveu, \
Implementou, Liderou, Otimizou, Atuou).
- Use linguagem profissional, direta, sem cliches.
- Escreva em portugues brasileiro.
- NAO use marcacao Markdown, listas com bullet, nem emojis.

Devolva APENAS o texto reescrito, sem nenhuma introducao, comentario, aspas \
ou explicacao.

Descricao original:
\"\"\"
{texto}
\"\"\"\
"""


_INSTRUCAO_DESCRICAO_PROJETO = """\
Voce e um especialista em curriculos brasileiros otimizados para sistemas \
ATS (Applicant Tracking Systems).

Sua tarefa: reescrever a descricao de um projeto pessoal/academico, deixando \
mais clara, profissional e densa em palavras-chave tecnicas, adequada para \
parsing por ATS.

Contexto do projeto: {contexto}

Regras:
- Mantenha o MESMO escopo, propósito e tecnologias mencionadas. NAO invente \
funcionalidades, escala ou tecnologias que nao foram citadas.
- Use entre 10 e 500 caracteres no resultado.
- Foque no problema resolvido e nas tecnologias/habilidades empregadas.
- Use linguagem profissional, direta, sem cliches.
- Escreva em portugues brasileiro.
- NAO use marcacao Markdown nem emojis.

Devolva APENAS o texto reescrito, sem nenhuma introducao, comentario, aspas \
ou explicacao.

Descricao original:
\"\"\"
{texto}
\"\"\"\
"""


def _cliente() -> genai.Client:
    """Cria cliente Gemini. A chave vem do env."""
    chave = os.getenv("GOOGLE_API_KEY")
    if not chave:
        raise RuntimeError(
            "GOOGLE_API_KEY nao configurada. Veja backend/.env.example."
        )
    return genai.Client(api_key=chave)


def _gerar(prompt: str) -> str:
    """Chama Gemini com um prompt ja montado e devolve o texto limpo."""
    cliente = _cliente()
    modelo = os.getenv("GEMINI_MODEL", _MODELO_PADRAO)

    resposta = cliente.models.generate_content(
        model=modelo,
        contents=prompt,
    )

    if not resposta.text:
        raise RuntimeError("Resposta vazia do modelo.")

    return resposta.text.strip()


def melhorar_resumo(texto: str) -> str:
    """Chama Gemini para reescrever o resumo profissional."""
    return _gerar(_INSTRUCAO_RESUMO.format(texto=texto))


def melhorar_descricao_experiencia(texto: str, contexto: str = "") -> str:
    """
    Chama Gemini para reescrever a descricao de uma experiencia profissional.

    O contexto pode incluir cargo e empresa para dar ao modelo mais base.
    """
    prompt = _INSTRUCAO_DESCRICAO_EXPERIENCIA.format(
        texto=texto,
        contexto=contexto or "nao informado",
    )
    return _gerar(prompt)


def melhorar_descricao_projeto(texto: str, contexto: str = "") -> str:
    """
    Chama Gemini para reescrever a descricao de um projeto.

    O contexto pode incluir nome do projeto para dar ao modelo mais base.
    """
    prompt = _INSTRUCAO_DESCRICAO_PROJETO.format(
        texto=texto,
        contexto=contexto or "nao informado",
    )
    return _gerar(prompt)
