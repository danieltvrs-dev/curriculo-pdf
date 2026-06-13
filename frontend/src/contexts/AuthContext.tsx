import { createContext, ReactNode, useContext, useEffect, useState } from 'react'

import { setAccessToken } from '../services/api'
import * as authService from '../services/auth'
import { User } from '../types/auth'

type AuthContextValue = {
  user: User | null
  carregando: boolean
  login: (email: string, senha: string) => Promise<void>
  registrar: (nome: string, email: string, senha: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [carregando, setCarregando] = useState(true)

  // Ao montar, tenta refresh com o cookie httpOnly. Se houver sessao
  // valida, recebe novo access token e busca o user.
  useEffect(() => {
    async function hidratar() {
      try {
        const novoAccess = await authService.refresh()
        setAccessToken(novoAccess)
        const u = await authService.me()
        setUser(u)
      } catch {
        setAccessToken(null)
      } finally {
        setCarregando(false)
      }
    }
    hidratar()
  }, [])

  async function login(email: string, senha: string) {
    const token = await authService.login(email, senha)
    setAccessToken(token)
    const u = await authService.me()
    setUser(u)
  }

  async function registrar(nome: string, email: string, senha: string) {
    await authService.registrar(nome, email, senha)
    await login(email, senha)
  }

  async function logout() {
    try {
      await authService.logout()
    } catch {
      // Ignora erro no logout server-side: o importante e limpar o estado local.
    }
    setAccessToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{ user, carregando, login, registrar, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider')
  return ctx
}
