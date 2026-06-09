/**
 * Tipos do curriculo, espelho dos schemas Pydantic do backend.
 *
 * Quando o schema do backend mudar, ATUALIZA AQUI tambem. Sao duas fontes
 * que precisam andar juntas. Em projetos maduros isso e gerado automaticamente
 * a partir do OpenAPI do FastAPI, mas pra MVP didatico mantemos manual.
 */

export enum NivelFormacao {
  Tecnico = 'Tecnico',
  Tecnologo = 'Tecnologo',
  Graduacao = 'Graduacao',
  PosGraduacao = 'Pos-graduacao',
  Mestrado = 'Mestrado',
  Doutorado = 'Doutorado',
}

export type DadosPessoais = {
  nome_completo: string
  email: string
  telefone: string
  cidade: string
  linkedin_url?: string | null
  github_url?: string | null
  portfolio_url?: string | null
}

export type Experiencia = {
  empresa: string
  cargo: string
  data_inicio: string // formato ISO "AAAA-MM-DD"
  data_fim?: string | null
  descricao: string
  tecnologias: string[]
}

export type Formacao = {
  instituicao: string
  curso: string
  nivel: NivelFormacao
  data_inicio: string
  data_fim?: string | null
}

export type Projeto = {
  nome: string
  descricao: string
  tecnologias: string[]
  url?: string | null
}

export type CurriculoEntrada = {
  dados_pessoais: DadosPessoais
  resumo_profissional: string
  experiencias: Experiencia[]
  formacoes: Formacao[]
  habilidades: string[]
  projetos: Projeto[]
}
