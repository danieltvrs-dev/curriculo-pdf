import { CurriculoEntrada } from './curriculo'

export type CurriculoResumo = {
  id: number
  nome: string
  criado_em: string
  atualizado_em: string
}

export type CurriculoDetalhe = CurriculoResumo & {
  dados: CurriculoEntrada
}
