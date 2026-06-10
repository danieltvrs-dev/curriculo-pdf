import { Projeto } from '../../types/curriculo'
import { projetoVazio } from '../../utils/curriculoVazio'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { TagInput } from '../ui/TagInput'
import { Textarea } from '../ui/Textarea'

type Props = {
  projetos: Projeto[]
  onChange: (projetos: Projeto[]) => void
}

export function ProjetoList({ projetos, onChange }: Props) {
  function adicionar() {
    onChange([...projetos, { ...projetoVazio, tecnologias: [] }])
  }

  function remover(i: number) {
    onChange(projetos.filter((_, idx) => idx !== i))
  }

  function atualizar<K extends keyof Projeto>(
    i: number,
    campo: K,
    valor: Projeto[K]
  ) {
    onChange(projetos.map((p, idx) => (idx === i ? { ...p, [campo]: valor } : p)))
  }

  return (
    <div className="space-y-4">
      {projetos.length === 0 && (
        <p className="text-sm text-slate-500 italic">
          Nenhum projeto adicionado. Opcional, mas valioso para juniors.
        </p>
      )}

      {projetos.map((proj, i) => (
        <div
          key={i}
          className="rounded-md border border-slate-200 p-4 space-y-3 bg-slate-50/40"
        >
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-700">
              Projeto {i + 1}
            </h3>
            <Button variant="danger" type="button" onClick={() => remover(i)}>
              Remover
            </Button>
          </div>

          <Input
            label="Nome do projeto"
            required
            value={proj.nome}
            onChange={(e) => atualizar(i, 'nome', e.target.value)}
            placeholder="Ex: Gerador de Curriculo em PDF"
          />

          <Textarea
            label="Descricao"
            required
            value={proj.descricao}
            onChange={(e) => atualizar(i, 'descricao', e.target.value)}
            maxLength={500}
            hint="Maximo 500 caracteres"
          />

          <TagInput
            label="Tecnologias"
            tags={proj.tecnologias}
            onChange={(novas) => atualizar(i, 'tecnologias', novas)}
            placeholder="Digite e tecle Enter: React, FastAPI, ..."
            hint="Enter ou virgula adiciona. Backspace remove a ultima."
          />

          <Input
            label="URL"
            type="url"
            value={proj.url ?? ''}
            onChange={(e) => atualizar(i, 'url', e.target.value)}
            placeholder="https://github.com/voce/projeto"
          />
        </div>
      ))}

      <Button variant="secondary" type="button" onClick={adicionar}>
        + Adicionar projeto
      </Button>
    </div>
  )
}
