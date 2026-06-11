/**
 * Service de comunicacao com os endpoints de IA do backend.
 *
 * O backend faz proxy seguro pro Gemini. O frontend nao toca chave nenhuma.
 */

import api from './api'

type TextoResposta = {
  texto: string
}

export async function melhorarResumo(texto: string): Promise<string> {
  const response = await api.post<TextoResposta>('/ia/melhorar-resumo', {
    texto,
  })
  return response.data.texto
}

export async function melhorarDescricaoExperiencia(
  texto: string,
  contexto: string
): Promise<string> {
  const response = await api.post<TextoResposta>(
    '/ia/melhorar-descricao-experiencia',
    { texto, contexto }
  )
  return response.data.texto
}

export async function melhorarDescricaoProjeto(
  texto: string,
  contexto: string
): Promise<string> {
  const response = await api.post<TextoResposta>(
    '/ia/melhorar-descricao-projeto',
    { texto, contexto }
  )
  return response.data.texto
}
