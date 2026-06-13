import axios, { AxiosRequestConfig } from 'axios'

/**
 * O access token vive em uma variavel de modulo (memoria).
 * Nao usamos mais localStorage: o refresh token agora mora num cookie
 * httpOnly setado pelo backend, e o access token e curto + descartavel.
 *
 * Em recarregamento de pagina, o AuthContext chama /auth/refresh no mount
 * e re-hidrata este valor.
 */
let accessToken: string | null = null

export function setAccessToken(token: string | null) {
  accessToken = token
}

export function getAccessToken(): string | null {
  return accessToken
}

const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  // withCredentials manda o cookie httpOnly em toda request.
  // Backend precisa de allow_credentials=True no CORS.
  withCredentials: true,
})

// Anexa o access token em toda request, se existir.
api.interceptors.request.use((config) => {
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`
  }
  return config
})

// Em 401, tenta refresh transparente uma vez. Se funcionar, retenta a request
// original com o novo access token.
api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const original = err.config as AxiosRequestConfig & { _retry?: boolean }

    const ehErroAuth = err?.response?.status === 401
    const ehRotaAuth =
      typeof original?.url === 'string' && original.url.includes('/auth/')

    if (ehErroAuth && !ehRotaAuth && !original._retry) {
      original._retry = true
      try {
        const r = await axios.post(
          `${baseURL}/auth/refresh`,
          {},
          { withCredentials: true }
        )
        const novoAccess = r.data.access_token as string
        accessToken = novoAccess
        original.headers = original.headers ?? {}
        ;(original.headers as Record<string, string>)['Authorization'] =
          `Bearer ${novoAccess}`
        return api(original)
      } catch {
        accessToken = null
        return Promise.reject(err)
      }
    }

    return Promise.reject(err)
  }
)

export default api
