"""
Service de melhoria de textos via Claude (Anthropic).

Recebe um texto cru, devolve uma versao reescrita otimizada para ATS,
mantendo o sentido original e respeitando os limites de tamanho.

Configuracao via .env:
- ANTHROPIC_API_KEY: chave da Anthropic
- ANTHROPIC_MODEL: modelo (default claude-sonnet-4-6)
"""

import os

from anthropic import Anthropic

_MODELO_PADRAO = "claude-sonnet-4-6"

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


def _cliente() -> Anthropic:
    """Cria cliente Anthropic. A chave vem do env."""
    chave = os.getenv("ANTHROPIC_API_KEY")
    if not chave:
        raise RuntimeError(
            "ANTHROPIC_API_KEY nao configurada. Veja backend/.env.example."
        )
    return Anthropic(api_key=chave)


def melhorar_resumo(texto: str) -> str:
    """
    Chama Claude para reescrever o resumo profissional.

    Lanca RuntimeError se a chave nao esta configurada.
    Outras excecoes da API sao deixadas subir para o caller decidir.
    """
    cliente = _cliente()
    modelo = os.getenv("ANTHROPIC_MODEL", _MODELO_PADRAO)

    resposta = cliente.messages.create(
        model=modelo,
        max_tokens=400,
        messages=[
            {
                "role": "user",
                "content": _INSTRUCAO_RESUMO.format(texto=texto),
            }
        ],
    )

    # A API devolve uma lista de blocos de conteudo. Pegamos o texto do primeiro.
    if not resposta.content:
        raise RuntimeError("Resposta vazia do modelo.")

    primeiro = resposta.content[0]
    if not hasattr(primeiro, "text"):
        raise RuntimeError("Formato inesperado de resposta do modelo.")

    return primeiro.text.strip()
