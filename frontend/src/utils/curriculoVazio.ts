/**
 * Estados iniciais "vazios" usados pelo formulario.
 *
 * Separar isso aqui mantem o Form.tsx mais limpo e centraliza
 * a definicao de "como comeca uma experiencia/formacao nova".
 */

import {
  CurriculoEntrada,
  DadosPessoais,
  Experiencia,
  Formacao,
  NivelFormacao,
  Projeto,
} from '../types/curriculo'

export const dadosPessoaisVazios: DadosPessoais = {
  nome_completo: '',
  email: '',
  telefone: '',
  cidade: '',
  linkedin_url: '',
  github_url: '',
  portfolio_url: '',
}

export const experienciaVazia: Experiencia = {
  empresa: '',
  cargo: '',
  data_inicio: '',
  data_fim: null,
  descricao: '',
  tecnologias: [],
}

export const formacaoVazia: Formacao = {
  instituicao: '',
  curso: '',
  nivel: NivelFormacao.Graduacao,
  data_inicio: '',
  data_fim: null,
}

export const projetoVazio: Projeto = {
  nome: '',
  descricao: '',
  tecnologias: [],
  url: '',
}

export const curriculoVazio: CurriculoEntrada = {
  dados_pessoais: { ...dadosPessoaisVazios },
  resumo_profissional: '',
  experiencias: [],
  formacoes: [{ ...formacaoVazia }],
  habilidades: [],
  projetos: [],
}
