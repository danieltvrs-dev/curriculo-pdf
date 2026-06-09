/// <reference types="vite/client" />

// Tipagem das variaveis de ambiente expostas ao frontend.
// So variaveis com prefixo VITE_ ficam disponiveis em import.meta.env.

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
