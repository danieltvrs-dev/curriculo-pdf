import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { useAuth } from '../contexts/AuthContext'

export function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState<string | null>(null)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (enviando) return

    setEnviando(true)
    setErro(null)
    try {
      await login(email, senha)
      navigate('/', { replace: true })
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setErro(typeof detail === 'string' ? detail : 'Erro ao entrar.')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100 p-4">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow w-full max-w-md space-y-4"
      >
        <header className="mb-2">
          <h1 className="text-2xl font-bold text-slate-900">Entrar</h1>
          <p className="text-sm text-slate-600 mt-1">
            Use sua conta para gerenciar seus curriculos.
          </p>
        </header>

        {erro && (
          <div className="text-sm bg-red-50 border border-red-200 text-red-800 rounded p-3">
            {erro}
          </div>
        )}

        <Input
          label="Email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
        />

        <Input
          label="Senha"
          type="password"
          required
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          autoComplete="current-password"
        />

        <Button type="submit" disabled={enviando} className="w-full">
          {enviando ? 'Entrando...' : 'Entrar'}
        </Button>

        <p className="text-sm text-center text-slate-600 pt-2">
          Nao tem conta?{' '}
          <Link to="/cadastro" className="text-slate-900 font-medium underline">
            Cadastre-se
          </Link>
        </p>
      </form>
    </div>
  )
}
