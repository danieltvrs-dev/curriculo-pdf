import { Textarea } from '../ui/Textarea'

type Props = {
  habilidades: string[]
  onChange: (habilidades: string[]) => void
}

/**
 * Habilidades sao digitadas como texto livre separado por virgula.
 * Internamente, viram um array de strings.
 *
 * Escolha de UX: texto livre e mais rapido que adicionar tag por tag.
 * Espacos extras e itens vazios sao removidos automaticamente.
 */
export function HabilidadesField({ habilidades, onChange }: Props) {
  function handleChange(texto: string) {
    const lista = texto
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
    onChange(lista)
  }

  return (
    <Textarea
      label="Habilidades"
      required
      value={habilidades.join(', ')}
      onChange={(e) => handleChange(e.target.value)}
      hint="Separe por virgulas. Ex: Python, JavaScript, React, FastAPI, PostgreSQL, Git, Docker"
      placeholder="Python, JavaScript, React, ..."
    />
  )
}
