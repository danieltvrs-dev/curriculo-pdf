import { CurriculoEntrada } from '../types/curriculo'
import { CurriculoDetalhe, CurriculoResumo } from '../types/meusCurriculos'
import { prepararParaEnvio } from '../utils/prepararEnvio'
import api from './api'

export async function listar(): Promise<CurriculoResumo[]> {
  const r = await api.get<CurriculoResumo[]>('/meus-curriculos')
  return r.data
}

export async function buscar(id: number): Promise<CurriculoDetalhe> {
  const r = await api.get<CurriculoDetalhe>(`/meus-curriculos/${id}`)
  return r.data
}

export async function criar(
  nome: string,
  dados: CurriculoEntrada
): Promise<CurriculoDetalhe> {
  const r = await api.post<CurriculoDetalhe>('/meus-curriculos', {
    nome,
    dados: prepararParaEnvio(dados),
  })
  return r.data
}

export async function atualizar(
  id: number,
  nome: string,
  dados: CurriculoEntrada
): Promise<CurriculoDetalhe> {
  const r = await api.put<CurriculoDetalhe>(`/meus-curriculos/${id}`, {
    nome,
    dados: prepararParaEnvio(dados),
  })
  return r.data
}

export async function deletar(id: number): Promise<void> {
  await api.delete(`/meus-curriculos/${id}`)
}

export async function baixarPdf(id: number): Promise<void> {
  const r = await api.get(`/meus-curriculos/${id}/pdf`, {
    responseType: 'blob',
  })
  const blob = r.data as Blob
  const url = URL.createObjectURL(blob)

  const disp = (r.headers['content-disposition'] ?? '') as string
  const match = /filename="?([^";]+)"?/.exec(disp)
  const nomeArquivo = match?.[1] ?? 'curriculo.pdf'

  const a = document.createElement('a')
  a.href = url
  a.download = nomeArquivo
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
