import { Experiencia } from '../../types/curriculo'
import { experienciaVazia } from '../../utils/curriculoVazio'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { TagInput } from '../ui/TagInput'
import { Textarea } from '../ui/Textarea'

type Props = {
  experiencias: Experiencia[]
  onChange: (experiencias: Experiencia[]) => void
}

export function ExperienciaList({ experiencias, onChange }: Props) {
  function adicionar() {
    onChange([...experiencias, { ...experienciaVazia, tecnologias: [] }])
  }

  function remover(i: number) {
    onChange(experiencias.filter((_, idx) => idx !== i))
  }

  function atualizar<K extends keyof Experiencia>(
    i: number,
    campo: K,
    valor: Experiencia[K]
  ) {
    onChange(
      experiencias.map((e, idx) => (idx === i ? { ...e, [campo]: valor } : e))
    )
  }

  return (
    <div className="space-y-4">
      {experiencias.length === 0 && (
        <p className="text-sm text-slate-500 italic">
          Nenhuma experiencia adicionada. Opcional para quem esta comecando.
        </p>
      )}

      {experiencias.map((exp, i) => (
        <div
          key={i}
          className="rounded-md border border-slate-200 p-4 space-y-3 bg-slate-50/40"
        >
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-700">
              Experiencia {i + 1}
            </h3>
            <Button variant="danger" type="button" onClick={() => remover(i)}>
              Remover
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Input
              label="Cargo"
              required
              value={exp.cargo}
              onChange={(e) => atualizar(i, 'cargo', e.target.value)}
              placeholder="Ex: Desenvolvedor Junior"
            />
            <Input
              label="Empresa"
              required
              value={exp.empresa}
              onChange={(e) => atualizar(i, 'empresa', e.target.value)}
              placeholder="Ex: Empresa XYZ"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Input
              label="Inicio"
              type="date"
              required
              value={exp.data_inicio}
              onChange={(e) => atualizar(i, 'data_inicio', e.target.value)}
            />
            <div>
              <Input
                label="Fim"
                type="date"
                value={exp.data_fim ?? ''}
                disabled={exp.data_fim === null}
                onChange={(e) =>
                  atualizar(i, 'data_fim', e.target.value || null)
                }
              />
              <label className="mt-2 inline-flex items-center gap-2 text-xs text-slate-600">
                <input
                  type="checkbox"
                  checked={exp.data_fim === null}
                  onChange={(e) =>
                    atualizar(i, 'data_fim', e.target.checked ? null : '')
                  }
                />
                Trabalho atual
              </label>
            </div>
          </div>

          <Textarea
            label="Descricao das atividades"
            required
            value={exp.descricao}
            onChange={(e) => atualizar(i, 'descricao', e.target.value)}
            hint="Maximo 500 caracteres"
            maxLength={500}
          />

          <TagInput
            label="Tecnologias"
            tags={exp.tecnologias}
            onChange={(novas) => atualizar(i, 'tecnologias', novas)}
            placeholder="Digite e tecle Enter: Python, React, ..."
            hint="Enter ou virgula adiciona uma tecnologia. Backspace remove a ultima."
          />
        </div>
      ))}

      <Button variant="secondary" type="button" onClick={adicionar}>
        + Adicionar experiencia
      </Button>
    </div>
  )
}
