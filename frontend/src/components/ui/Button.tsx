import { ButtonHTMLAttributes } from 'react'

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
}

/**
 * Botao com tres variantes:
 * - primary: acao principal (dark)
 * - secondary: acao alternativa (branco com borda)
 * - ghost: acao terciaria (so texto)
 * - danger: acao destrutiva (vermelho discreto)
 */
export function Button({
  variant = 'primary',
  className = '',
  ...rest
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed'
  const variants = {
    primary: 'bg-slate-800 text-white hover:bg-slate-700',
    secondary: 'bg-white border border-slate-300 text-slate-700 hover:bg-slate-50',
    ghost: 'text-slate-600 hover:text-slate-800',
    danger: 'text-red-600 hover:text-red-700 hover:bg-red-50',
  }
  return <button {...rest} className={`${base} ${variants[variant]} ${className}`} />
}
