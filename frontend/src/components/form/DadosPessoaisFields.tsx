import { DadosPessoais } from '../../types/curriculo'
import { Input } from '../ui/Input'

type Props = {
  dados: DadosPessoais
  onChange: (campo: keyof DadosPessoais, valor: string) => void
}

export function DadosPessoaisFields({ dados, onChange }: Props) {
  return (
    <>
      <Input
        label="Nome completo"
        required
        value={dados.nome_completo}
        onChange={(e) => onChange('nome_completo', e.target.value)}
        placeholder="Ex: Daniel Tavares"
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Email"
          type="email"
          required
          value={dados.email}
          onChange={(e) => onChange('email', e.target.value)}
          placeholder="seu@email.com"
        />
        <Input
          label="Telefone"
          required
          value={dados.telefone}
          onChange={(e) => onChange('telefone', e.target.value)}
          placeholder="(11) 99999-9999"
        />
      </div>
      <Input
        label="Cidade/UF"
        required
        value={dados.cidade}
        onChange={(e) => onChange('cidade', e.target.value)}
        placeholder="Sao Paulo/SP"
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="LinkedIn"
          type="url"
          value={dados.linkedin_url ?? ''}
          onChange={(e) => onChange('linkedin_url', e.target.value)}
          placeholder="https://linkedin.com/in/voce"
        />
        <Input
          label="GitHub"
          type="url"
          value={dados.github_url ?? ''}
          onChange={(e) => onChange('github_url', e.target.value)}
          placeholder="https://github.com/voce"
        />
      </div>
      <Input
        label="Portfolio"
        type="url"
        value={dados.portfolio_url ?? ''}
        onChange={(e) => onChange('portfolio_url', e.target.value)}
        placeholder="https://seusite.com"
      />
    </>
  )
}
