/**
 * Service de comunicacao com a API de curriculos.
 *
 * Encapsula a chamada axios e o ritual de download de Blob, pra que
 * os componentes React nao precisem saber nada disso.
 */

import { CurriculoEntrada } from '../types/curriculo'
import { prepararParaEnvio } from '../utils/prepararEnvio'
import api from './api'

const REGEX_FILENAME = /filename="?([^";]+)"?/

function extrairNomeArquivo(headers: Record<string, string>): string {
  const disposicao = headers['content-disposition'] ?? ''
  const match = REGEX_FILENAME.exec(disposicao)
  return match?.[1] ?? 'curriculo.pdf'
}

function disparaDownload(blob: Blob, nomeArquivo: string) {
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = nomeArquivo
  document.body.appendChild(anchor)
  anchor.click()
  document.body.removeChild(anchor)
  URL.revokeObjectURL(url)
}

/**
 * Envia o curriculo pra API e dispara o download do PDF gerado.
 *
 * Lanca excecao em qualquer erro (rede, 4xx, 5xx). O caller decide
 * o que mostrar pro usuario.
 */
export async function gerarCurriculoPdf(
  curriculo: CurriculoEntrada
): Promise<void> {
  const dados = prepararParaEnvio(curriculo)

  const response = await api.post('/curriculos', dados, {
    responseType: 'blob',
  })

  const nomeArquivo = extrairNomeArquivo(response.headers as Record<string, string>)
  disparaDownload(response.data as Blob, nomeArquivo)
}
