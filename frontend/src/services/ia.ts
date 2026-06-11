/**
 * Service de comunicacao com os endpoints de IA do backend.
 *
 * O backend faz proxy seguro pro Gemini. O frontend nao toca chave nenhuma.
 */

import api from './api'

type MelhorarResumoResposta = {
  texto: string
}

export async function melhorarResumo(texto: string): Promise<string> {
  const response = await api.post<MelhorarResumoResposta>(
    '/ia/melhorar-resumo',
    { texto }
  )
  return response.data.texto
}
