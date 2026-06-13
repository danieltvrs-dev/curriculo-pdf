import { User } from '../types/auth'
import api from './api'

type LoginResposta = {
  access_token: string
  token_type: string
}

export async function login(email: string, senha: string): Promise<string> {
  const r = await api.post<LoginResposta>('/auth/login', { email, senha })
  return r.data.access_token
}

export async function registrar(
  nome: string,
  email: string,
  senha: string
): Promise<User> {
  const r = await api.post<User>('/auth/registrar', { nome, email, senha })
  return r.data
}

export async function me(): Promise<User> {
  const r = await api.get<User>('/auth/me')
  return r.data
}

export async function refresh(): Promise<string> {
  const r = await api.post<LoginResposta>('/auth/refresh')
  return r.data.access_token
}

export async function logout(): Promise<void> {
  await api.post('/auth/logout')
}
