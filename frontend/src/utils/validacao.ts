/**
 * Validacao "leve" para o botao de gerar PDF.
 *
 * So checa o minimo: campos obrigatorios preenchidos e tamanhos minimos
 * que o Pydantic vai exigir. NAO duplicamos toda a validacao do backend,
 * o Pydantic continua sendo a defesa real (422 com erros estruturados).
 *
 * Objetivo: dar feedback rapido pro usuario, evitando ele clicar e levar
 * um erro do servidor por um campo obvio em branco.
 */

import { CurriculoEntrada } from '../types/curriculo'

export function podeEnviar(c: CurriculoEntrada): boolean {
  const dp = c.dados_pessoais
  if (
    !dp.nome_completo.trim() ||
    !dp.email.trim() ||
    !dp.telefone.trim() ||
    !dp.cidade.trim()
  ) {
    return false
  }

  if (c.resumo_profissional.trim().length < 50) return false

  if (c.formacoes.length === 0) return false
  const formacoesOk = c.formacoes.every(
    (f) => f.instituicao.trim() && f.curso.trim() && f.data_inicio
  )
  if (!formacoesOk) return false

  if (c.habilidades.length === 0) return false

  return true
}
