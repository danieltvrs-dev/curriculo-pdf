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


def _cliente() -> genai.Client:
    """Cria cliente Gemini. A chave vem do env."""
    chave = os.getenv("GOOGLE_API_KEY")
    if not chave:
        raise RuntimeError(
            "GOOGLE_API_KEY nao configurada. Veja backend/.env.example."
        )
    return genai.Client(api_key=chave)


def melhorar_resumo(texto: str) -> str:
    """
    Chama Gemini para reescrever o resumo profissional.

    Lanca RuntimeError se a chave nao esta configurada.
    Outras excecoes da API sao deixadas subir para o caller decidir.
    """
    cliente = _cliente()
    modelo = os.getenv("GEMINI_MODEL", _MODELO_PADRAO)

    resposta = cliente.models.generate_content(
        model=modelo,
        contents=_INSTRUCAO_RESUMO.format(texto=texto),
    )

    if not resposta.text:
        raise RuntimeError("Resposta vazia do modelo.")

    return resposta.text.strip()
