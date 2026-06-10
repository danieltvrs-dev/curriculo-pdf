import { TagInput } from '../ui/TagInput'

type Props = {
  habilidades: string[]
  onChange: (habilidades: string[]) => void
}

/**
 * Habilidades como chips removiveis.
 *
 * Mesmo padrao de tecnologias em Experiencia e Projeto: o usuario
 * digita uma habilidade por vez e tecla Enter/virgula. Mantem o
 * formato esperado pelo backend (lista de strings) e da visual claro
 * de quantas habilidades ja foram adicionadas.
 */
export function HabilidadesField({ habilidades, onChange }: Props) {
  return (
    <TagInput
      label="Habilidades"
      required
      tags={habilidades}
      onChange={onChange}
      placeholder="Python, JavaScript, React, FastAPI, ..."
      hint="Cada habilidade vira uma palavra-chave para o ATS. Quanto mais relevantes, melhor."
    />
  )
}
