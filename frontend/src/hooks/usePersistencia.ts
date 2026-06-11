import { useEffect, useState } from 'react'

/**
 * Hook que sincroniza um estado React com o localStorage do navegador.
 *
 * Le do localStorage na PRIMEIRA renderizacao (lazy initial state).
 * Salva no localStorage toda vez que o valor muda.
 * Expoe uma funcao `limpar` para remover do localStorage e voltar ao inicial.
 *
 * Generico: passe o tipo T e use como um useState normal.
 *
 * Exemplo:
 *   const [c, setC, limparC] = usePersistencia('curriculo', curriculoVazio)
 */
export function usePersistencia<T>(chave: string, valorInicial: T) {
  const [valor, setValor] = useState<T>(() => {
    try {
      const salvo = localStorage.getItem(chave)
      if (salvo !== null) return JSON.parse(salvo) as T
    } catch (e) {
      console.warn(`Erro lendo localStorage[${chave}]:`, e)
    }
    return valorInicial
  })

  useEffect(() => {
    try {
      localStorage.setItem(chave, JSON.stringify(valor))
    } catch (e) {
      console.warn(`Erro salvando localStorage[${chave}]:`, e)
    }
  }, [chave, valor])

  function limpar() {
    try {
      localStorage.removeItem(chave)
    } catch (e) {
      console.warn(`Erro removendo localStorage[${chave}]:`, e)
    }
    setValor(valorInicial)
  }

  return [valor, setValor, limpar] as const
}
