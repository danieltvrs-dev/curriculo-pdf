import { createContext, ReactNode, useContext, useEffect, useState } from 'react'

import * as authService from '../services/auth'
import { TOKEN_KEY } from '../services/api'
import { User } from '../types/auth'

type AuthContextValue = {
  user: User | null
  carregando: boolean
  login: (email: string, senha: string) => Promise<void>
  registrar: (nome: string, email: string, senha: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [carregando, setCarregando] = useState(true)

  // Ao montar, tenta hidratar o user a partir do token salvo.
  useEffect(() => {
    async function hidratar() {
      const token = localStorage.getItem(TOKEN_KEY)
      if (!token) {
        setCarregando(false)
        return
      }
      try {
        const u = await authService.me()
        setUser(u)
      } catch {
        localStorage.removeItem(TOKEN_KEY)
      } finally {
        setCarregando(false)
      }
    }
    hidratar()
  }, [])

  async function login(email: string, senha: string) {
    const token = await authService.login(email, senha)
    localStorage.setItem(TOKEN_KEY, token)
    const u = await authService.me()
    setUser(u)
  }

  async function registrar(nome: string, email: string, senha: string) {
    await authService.registrar(nome, email, senha)
    await login(email, senha)
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
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
