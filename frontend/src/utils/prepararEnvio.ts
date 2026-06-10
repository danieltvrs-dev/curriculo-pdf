/**
 * Sanitiza o curriculo antes de enviar pro backend.
 *
 * Casos tratados:
 * - URLs opcionais como string vazia ('') viram null. O Pydantic com
 *   HttpUrl rejeita '' (espera URL valida ou null).
 * - data_fim como '' (usuario digitou e apagou) vira null. Pydantic
 *   espera string ISO de data ou null.
 *
 * Mantemos o tipo CurriculoEntrada porque a forma e identica, so
 * trocamos '' por null nos campos opcionais.
 */

import { CurriculoEntrada } from '../types/curriculo'

function vazioVirarNull(v: string | null | undefined): string | null {
  if (v === null || v === undefined) return null
  if (v.trim() === '') return null
  return v
}

export function prepararParaEnvio(c: CurriculoEntrada): CurriculoEntrada {
  return {
    ...c,
    dados_pessoais: {
      ...c.dados_pessoais,
      linkedin_url: vazioVirarNull(c.dados_pessoais.linkedin_url),
      github_url: vazioVirarNull(c.dados_pessoais.github_url),
      portfolio_url: vazioVirarNull(c.dados_pessoais.portfolio_url),
    },
    experiencias: c.experiencias.map((e) => ({
      ...e,
      data_fim: vazioVirarNull(e.data_fim),
    })),
    formacoes: c.formacoes.map((f) => ({
      ...f,
      data_fim: vazioVirarNull(f.data_fim),
    })),
    projetos: c.projetos.map((p) => ({
      ...p,
      url: vazioVirarNull(p.url),
    })),
  }
}
