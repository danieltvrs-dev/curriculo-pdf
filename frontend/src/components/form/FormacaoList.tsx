import { Formacao, NivelFormacao } from '../../types/curriculo'
import { formacaoVazia } from '../../utils/curriculoVazio'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'

type Props = {
  formacoes: Formacao[]
  onChange: (formacoes: Formacao[]) => void
}

export function FormacaoList({ formacoes, onChange }: Props) {
  function adicionar() {
    onChange([...formacoes, { ...formacaoVazia }])
  }

  function remover(i: number) {
    if (formacoes.length <= 1) return // sempre pelo menos 1
    onChange(formacoes.filter((_, idx) => idx !== i))
  }

  function atualizar<K extends keyof Formacao>(
    i: number,
    campo: K,
    valor: Formacao[K]
  ) {
    onChange(formacoes.map((f, idx) => (idx === i ? { ...f, [campo]: valor } : f)))
  }

  return (
    <div className="space-y-4">
      {formacoes.map((form, i) => (
        <div
          key={i}
          className="rounded-md border border-slate-200 p-4 space-y-3 bg-slate-50/40"
        >
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-700">
              Formacao {i + 1}
            </h3>
            <Button
              variant="danger"
              type="button"
              onClick={() => remover(i)}
              disabled={formacoes.length <= 1}
              title={
                formacoes.length <= 1
                  ? 'E necessaria pelo menos uma formacao'
                  : undefined
              }
            >
              Remover
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Input
              label="Instituicao"
              required
              value={form.instituicao}
              onChange={(e) => atualizar(i, 'instituicao', e.target.value)}
              placeholder="Ex: Faculdade XYZ"
            />
            <Input
              label="Curso"
              required
              value={form.curso}
              onChange={(e) => atualizar(i, 'curso', e.target.value)}
              placeholder="Ex: Analise e Desenvolvimento de Sistemas"
            />
          </div>

          <Select
            label="Nivel"
            required
            value={form.nivel}
            onChange={(e) =>
              atualizar(i, 'nivel', e.target.value as NivelFormacao)
            }
          >
            {Object.values(NivelFormacao).map((nivel) => (
              <option key={nivel} value={nivel}>
                {nivel}
              </option>
            ))}
          </Select>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Input
              label="Inicio"
              type="date"
              required
              value={form.data_inicio}
              onChange={(e) => atualizar(i, 'data_inicio', e.target.value)}
            />
            <div>
              <Input
                label="Conclusao"
                type="date"
                value={form.data_fim ?? ''}
                disabled={form.data_fim === null}
                onChange={(e) =>
                  atualizar(i, 'data_fim', e.target.value || null)
                }
              />
              <label className="mt-2 inline-flex items-center gap-2 text-xs text-slate-600">
                <input
                  type="checkbox"
                  checked={form.data_fim === null}
                  onChange={(e) =>
                    atualizar(i, 'data_fim', e.target.checked ? null : '')
                  }
                />
                Em andamento
              </label>
            </div>
          </div>
        </div>
      ))}

      <Button variant="secondary" type="button" onClick={adicionar}>
        + Adicionar formacao
      </Button>
    </div>
  )
}
