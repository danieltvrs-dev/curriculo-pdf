import { SelectHTMLAttributes, ReactNode } from 'react'

type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  label: string
  children: ReactNode
}

export function Select({ label, required, children, ...rest }: SelectProps) {
  return (
    <label className="block">
      <span className="block text-sm font-medium text-slate-700 mb-1">
        {label}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </span>
      <select
        {...rest}
        required={required}
        className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm bg-white focus:border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-500"
      >
        {children}
      </select>
    </label>
  )
}
