import { KeyboardEvent, useState } from 'react'

type Props = {
  label: string
  tags: string[]
  onChange: (tags: string[]) => void
  placeholder?: string
  hint?: string
  required?: boolean
}

/**
 * Campo de tags estilo chip.
 *
 * Interacao:
 * - Enter ou virgula -> commita a tag
 * - Backspace com input vazio -> remove a ultima tag
 * - Blur com texto digitado -> commita automaticamente
 * - Duplicatas e strings vazias sao ignoradas
 */
export function TagInput({
  label,
  tags,
  onChange,
  placeholder,
  hint,
  required,
}: Props) {
  const [valor, setValor] = useState('')

  function adicionar(tag: string) {
    const limpa = tag.trim()
    if (!limpa) return
    if (tags.includes(limpa)) {
      setValor('')
      return
    }
    onChange([...tags, limpa])
    setValor('')
  }

  function remover(i: number) {
    onChange(tags.filter((_, idx) => idx !== i))
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault()
      adicionar(valor)
      return
    }
    if (e.key === 'Backspace' && valor === '' && tags.length > 0) {
      remover(tags.length - 1)
    }
  }

  return (
    <div className="block">
      <span className="block text-sm font-medium text-slate-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </span>
      <div className="rounded-md border border-slate-300 px-2 py-2 bg-white focus-within:border-slate-500 focus-within:ring-1 focus-within:ring-slate-500">
        <div className="flex flex-wrap items-center gap-1.5">
          {tags.map((tag, i) => (
            <span
              key={`${tag}-${i}`}
              className="inline-flex items-center gap-1 bg-slate-200 text-slate-800 text-xs px-2 py-1 rounded"
            >
              {tag}
              <button
                type="button"
                onClick={() => remover(i)}
                className="text-slate-500 hover:text-slate-900 leading-none"
                aria-label={`Remover ${tag}`}
              >
                ×
              </button>
            </span>
          ))}
          <input
            value={valor}
            onChange={(e) => setValor(e.target.value)}
            onKeyDown={handleKeyDown}
            onBlur={() => adicionar(valor)}
            placeholder={tags.length === 0 ? placeholder : ''}
            className="flex-1 min-w-[120px] text-sm bg-transparent outline-none border-none px-1 py-1"
          />
        </div>
      </div>
      {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
    </div>
  )
}
