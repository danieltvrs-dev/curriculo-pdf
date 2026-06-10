import { InputHTMLAttributes } from 'react'

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string
  hint?: string
}

/**
 * Input controlado com label embutido.
 *
 * Marca asterisco vermelho quando required=true (padrao HTML).
 * O componente NAO valida nada, so dispara onChange. Validacao mora
 * no nivel do formulario, perto do botao Submit.
 */
export function Input({ label, hint, required, ...rest }: InputProps) {
  return (
    <label className="block">
      <span className="block text-sm font-medium text-slate-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </span>
      <input
        {...rest}
        required={required}
        className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-500"
      />
      {hint && <p className="mt-1 text-xs text-slate-500">{hint}</p>}
    </label>
  )
}
