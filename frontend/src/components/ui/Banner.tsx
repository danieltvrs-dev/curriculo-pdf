import { useEffect } from 'react'

type Variant = 'success' | 'error' | 'info'

type Props = {
  variant: Variant
  message: string
  onClose: () => void
  autoCloseMs?: number
}

const variantStyles: Record<Variant, string> = {
  success: 'bg-emerald-50 border-emerald-200 text-emerald-800',
  error: 'bg-red-50 border-red-200 text-red-800',
  info: 'bg-sky-50 border-sky-200 text-sky-800',
}

const variantIcon: Record<Variant, string> = {
  success: '✓',
  error: '✕',
  info: 'ℹ',
}

/**
 * Banner de feedback inline.
 *
 * Quando autoCloseMs > 0, agenda o fechamento automatico.
 * Use isso para mensagens de sucesso (some sozinho) e nao para erros
 * (usuario precisa ler com calma e decidir o que fazer).
 */
export function Banner({ variant, message, onClose, autoCloseMs }: Props) {
  useEffect(() => {
    if (!autoCloseMs) return
    const id = setTimeout(onClose, autoCloseMs)
    return () => clearTimeout(id)
  }, [autoCloseMs, onClose])

  return (
    <div
      role="alert"
      className={`flex items-start gap-3 rounded-md border px-4 py-3 mb-6 ${variantStyles[variant]}`}
    >
      <span className="font-bold leading-5">{variantIcon[variant]}</span>
      <p className="flex-1 text-sm leading-5">{message}</p>
      <button
        type="button"
        onClick={onClose}
        className="text-slate-500 hover:text-slate-900 text-sm leading-5"
        aria-label="Fechar"
      >
        ×
      </button>
    </div>
  )
}
