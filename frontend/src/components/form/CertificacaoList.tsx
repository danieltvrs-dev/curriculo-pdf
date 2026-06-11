import { Certificacao } from '../../types/curriculo'
import { certificacaoVazia } from '../../utils/curriculoVazio'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'

type Props = {
  certificacoes: Certificacao[]
  onChange: (certificacoes: Certificacao[]) => void
}

export function CertificacaoList({ certificacoes, onChange }: Props) {
  function adicionar() {
    onChange([...certificacoes, { ...certificacaoVazia }])
  }

  function remover(i: number) {
    onChange(certificacoes.filter((_, idx) => idx !== i))
  }

  function atualizar<K extends keyof Certificacao>(
    i: number,
    campo: K,
    valor: Certificacao[K]
  ) {
    onChange(
      certificacoes.map((it, idx) => (idx === i ? { ...it, [campo]: valor } : it))
    )
  }

  function setAno(i: number, valor: string) {
    const numero = valor.trim() === '' ? null : parseInt(valor, 10)
    atualizar(i, 'ano', Number.isNaN(numero as number) ? null : numero)
  }

  return (
    <div className="space-y-4">
      {certificacoes.length === 0 && (
        <p className="text-sm text-slate-500 italic">
          Nenhuma certificacao adicionada. Opcional.
        </p>
      )}

      {certificacoes.map((cert, i) => (
        <div
          key={i}
          className="rounded-md border border-slate-200 p-4 space-y-3 bg-slate-50/40"
        >
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-700">
              Certificacao {i + 1}
            </h3>
            <Button variant="danger" type="button" onClick={() => remover(i)}>
              Remover
            </Button>
          </div>

          <Input
            label="Nome da certificacao"
            required
            value={cert.nome}
            onChange={(e) => atualizar(i, 'nome', e.target.value)}
            placeholder="Ex: AWS Cloud Practitioner"
          />

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Input
              label="Instituicao"
              required
              value={cert.instituicao}
              onChange={(e) => atualizar(i, 'instituicao', e.target.value)}
              placeholder="Ex: Amazon, Microsoft, Coursera"
            />
            <Input
              label="Ano"
              type="number"
              value={cert.ano ?? ''}
              onChange={(e) => setAno(i, e.target.value)}
              placeholder="2024"
              min={1900}
              max={2100}
            />
          </div>

          <Input
            label="URL do certificado"
            type="url"
            value={cert.url ?? ''}
            onChange={(e) => atualizar(i, 'url', e.target.value)}
            placeholder="https://..."
          />
        </div>
      ))}

      <Button variant="secondary" type="button" onClick={adicionar}>
        + Adicionar certificacao
      </Button>
    </div>
  )
}
