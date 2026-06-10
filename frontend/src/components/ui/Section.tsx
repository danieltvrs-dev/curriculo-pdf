import { ReactNode } from 'react'

type SectionProps = {
  title: string
  description?: string
  children: ReactNode
}

/**
 * Cabecalho visual de uma secao do formulario.
 * Padrao reutilizado em todas as secoes (Dados Pessoais, Experiencia, etc.).
 */
export function Section({ title, description, children }: SectionProps) {
  return (
    <section className="mb-10">
      <header className="mb-4 pb-2 border-b border-slate-200">
        <h2 className="text-lg font-bold text-slate-800">{title}</h2>
        {description && (
          <p className="mt-1 text-sm text-slate-500">{description}</p>
        )}
      </header>
      <div className="space-y-4">{children}</div>
    </section>
  )
}
