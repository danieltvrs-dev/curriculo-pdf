import { FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { useAuth } from '../contexts/AuthContext'

export function Cadastro() {
  const navigate = useNavigate()
  const { registrar } = useAuth()

  const [nome, setNome] = useState('')
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
      await registrar(nome, email, senha)
      navigate('/', { replace: true })
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setErro(typeof detail === 'string' ? detail : 'Erro ao cadastrar.')
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
          <h1 className="text-2xl font-bold text-slate-900">Criar conta</h1>
          <p className="text-sm text-slate-600 mt-1">
            Salve curriculos e baixe quando quiser.
          </p>
        </header>

        {erro && (
          <div className="text-sm bg-red-50 border border-red-200 text-red-800 rounded p-3">
            {erro}
          </div>
        )}

        <Input
          label="Nome"
          required
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          autoComplete="name"
          minLength={2}
          maxLength={120}
        />

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
          autoComplete="new-password"
          minLength={8}
          maxLength={72}
          hint="Minimo 8 caracteres"
        />

        <Button type="submit" disabled={enviando} className="w-full">
          {enviando ? 'Criando conta...' : 'Cadastrar'}
        </Button>

        <p className="text-sm text-center text-slate-600 pt-2">
          Ja tem conta?{' '}
          <Link to="/login" className="text-slate-900 font-medium underline">
            Entrar
          </Link>
        </p>
      </form>
    </div>
  )
}
