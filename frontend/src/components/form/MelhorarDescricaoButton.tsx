import { useState } from 'react'

import {
  melhorarDescricaoExperiencia,
  melhorarDescricaoProjeto,
} from '../../services/ia'
import { Button } from '../ui/Button'
import { Modal } from '../ui/Modal'

type Props = {
  tipo: 'experiencia' | 'projeto'
  textoAtual: string
  contexto: string
  onAceitar: (textoMelhorado: string) => void
}

/**
 * Botao "Melhorar com IA" generico para descricao de Experiencia e Projeto.
 *
 * Diferencas em relacao ao botao do resumo:
 * - Limite minimo de 10 caracteres (resumo exige 50).
 * - Recebe um `contexto` que vai pro prompt (ex: cargo+empresa, nome do projeto).
 * - Chama o endpoint adequado ao tipo.
 */
export function MelhorarDescricaoButton({
  tipo,
  textoAtual,
  contexto,
  onAceitar,
}: Props) {
  const [enviando, setEnviando] = useState(false)
  const [modalAberto, setModalAberto] = useState(false)
  const [sugestao, setSugestao] = useState('')
  const [erro, setErro] = useState<string | null>(null)

  const tamanhoOk = textoAtual.trim().length >= 10
  const habilitado = tamanhoOk && !enviando

  async function handleClick() {
    setEnviando(true)
    setErro(null)
    try {
      const fn =
        tipo === 'experiencia'
          ? melhorarDescricaoExperiencia
          : melhorarDescricaoProjeto
      const texto = await fn(textoAtual, contexto)
      setSugestao(texto)
      setModalAberto(true)
    } catch (err: any) {
      console.error('Erro ao melhorar descricao:', err)
      const detail = err?.response?.data?.detail
      if (err?.response?.status === 429) {
        setErro('Muitas requisicoes em pouco tempo. Espere um instante.')
      } else if (typeof detail === 'string') {
        setErro(detail)
      } else {
        setErro('Nao foi possivel melhorar a descricao.')
      }
    } finally {
      setEnviando(false)
    }
  }

  function aceitar() {
    onAceitar(sugestao)
    setModalAberto(false)
  }

  return (
    <div>
      <Button
        type="button"
        variant="secondary"
        onClick={handleClick}
        disabled={!habilitado}
        title={
          !tamanhoOk
            ? 'Escreva pelo menos 10 caracteres antes de usar a IA'
            : undefined
        }
      >
        {enviando ? 'Pensando...' : '✨ Melhorar com IA'}
      </Button>
      {erro && <p className="mt-1 text-xs text-red-600">{erro}</p>}

      <Modal
        isOpen={modalAberto}
        onClose={() => setModalAberto(false)}
        title="Sugestao da IA"
      >
        <div className="space-y-5">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-2">
              Original ({textoAtual.length} caracteres)
            </h3>
            <p className="text-sm text-slate-700 bg-slate-50 border border-slate-200 rounded p-3 whitespace-pre-wrap">
              {textoAtual}
            </p>
          </div>

          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-emerald-700 mb-2">
              Sugestao da IA ({sugestao.length} caracteres)
            </h3>
            <p className="text-sm text-slate-900 bg-emerald-50 border border-emerald-200 rounded p-3 whitespace-pre-wrap">
              {sugestao}
            </p>
          </div>

          <div className="flex justify-end gap-2 pt-2 border-t border-slate-200">
            <Button
              variant="ghost"
              type="button"
              onClick={() => setModalAberto(false)}
            >
              Manter original
            </Button>
            <Button type="button" onClick={aceitar}>
              Aceitar sugestao
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
