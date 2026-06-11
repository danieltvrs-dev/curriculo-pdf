import { Idioma, NivelIdioma } from '../../types/curriculo'
import { idiomaVazio } from '../../utils/curriculoVazio'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'

type Props = {
  idiomas: Idioma[]
  onChange: (idiomas: Idioma[]) => void
}

export function IdiomaList({ idiomas, onChange }: Props) {
  function adicionar() {
    onChange([...idiomas, { ...idiomaVazio }])
  }

  function remover(i: number) {
    onChange(idiomas.filter((_, idx) => idx !== i))
  }

  function atualizar<K extends keyof Idioma>(
    i: number,
    campo: K,
    valor: Idioma[K]
  ) {
    onChange(idiomas.map((it, idx) => (idx === i ? { ...it, [campo]: valor } : it)))
  }

  return (
    <div className="space-y-4">
      {idiomas.length === 0 && (
        <p className="text-sm text-slate-500 italic">
          Nenhum idioma adicionado. Opcional.
        </p>
      )}

      {idiomas.map((it, i) => (
        <div
          key={i}
          className="rounded-md border border-slate-200 p-4 bg-slate-50/40"
        >
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-sm font-semibold text-slate-700">
              Idioma {i + 1}
            </h3>
            <Button variant="danger" type="button" onClick={() => remover(i)}>
              Remover
            </Button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Input
              label="Idioma"
              required
              value={it.idioma}
              onChange={(e) => atualizar(i, 'idioma', e.target.value)}
              placeholder="Ex: Ingles, Espanhol, Frances"
            />
            <Select
              label="Nivel"
              required
              value={it.nivel}
              onChange={(e) =>
                atualizar(i, 'nivel', e.target.value as NivelIdioma)
              }
            >
              {Object.values(NivelIdioma).map((nivel) => (
                <option key={nivel} value={nivel}>
                  {nivel}
                </option>
              ))}
            </Select>
          </div>
        </div>
      ))}

      <Button variant="secondary" type="button" onClick={adicionar}>
        + Adicionar idioma
      </Button>
    </div>
  )
}
