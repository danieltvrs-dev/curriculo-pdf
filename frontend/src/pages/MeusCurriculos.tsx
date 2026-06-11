import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { EscolherTemplateModal } from '../components/form/EscolherTemplateModal'
import { Banner } from '../components/ui/Banner'
import { Button } from '../components/ui/Button'
import { useAuth } from '../contexts/AuthContext'
import * as service from '../services/meusCurriculos'
import { TemplatePdf } from '../services/meusCurriculos'
import { CurriculoResumo } from '../types/meusCurriculos'

type Feedback = { variant: 'success' | 'error'; message: string }

export function MeusCurriculos() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [curriculos, setCurriculos] = useState<CurriculoResumo[] | null>(null)
  const [feedback, setFeedback] = useState<Feedback | null>(null)
  const [idParaBaixar, setIdParaBaixar] = useState<number | null>(null)

  useEffect(() => {
    service
      .listar()
      .then(setCurriculos)
      .catch(() => {
        setFeedback({ variant: 'error', message: 'Erro ao carregar a lista.' })
        setCurriculos([])
      })
  }, [])

  async function handleExcluir(id: number, nome: string) {
    if (!window.confirm(`Excluir "${nome}"? Essa acao nao pode ser desfeita.`)) {
      return
    }
    try {
      await service.deletar(id)
      setCurriculos((c) => c?.filter((x) => x.id !== id) ?? null)
      setFeedback({ variant: 'success', message: 'Curriculo excluido.' })
    } catch {
      setFeedback({ variant: 'error', message: 'Erro ao excluir.' })
    }
  }

  function handleBaixar(id: number) {
    // Abre o modal para escolher o template
    setIdParaBaixar(id)
  }

  async function handleConfirmarTemplate(template: TemplatePdf) {
    if (idParaBaixar === null) return
    try {
      await service.baixarPdf(idParaBaixar, template)
      setFeedback({ variant: 'success', message: 'PDF baixado.' })
    } catch {
      setFeedback({ variant: 'error', message: 'Erro ao baixar PDF.' })
    } finally {
      setIdParaBaixar(null)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-slate-900">
            Gerador de Curriculo em PDF
          </h1>
          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-600 hidden sm:inline">
              {user?.nome}
            </span>
            <Button variant="ghost" onClick={logout}>
              Sair
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Seus curriculos</h2>
            <p className="text-sm text-slate-600 mt-1">
              Cada curriculo pode ser editado, regerado em PDF e excluido.
            </p>
          </div>
          <Button onClick={() => navigate('/novo')}>+ Novo curriculo</Button>
        </div>

        {feedback && (
          <Banner
            variant={feedback.variant}
            message={feedback.message}
            onClose={() => setFeedback(null)}
            autoCloseMs={feedback.variant === 'success' ? 4000 : undefined}
          />
        )}

        {curriculos === null && (
          <p className="text-slate-500">Carregando...</p>
        )}

        {curriculos && curriculos.length === 0 && (
          <div className="bg-white rounded-md p-8 text-center">
            <p className="text-slate-700 font-medium">
              Voce ainda nao tem curriculos salvos.
            </p>
            <p className="mt-1 text-sm text-slate-500">
              Clique em "+ Novo curriculo" pra comecar.
            </p>
          </div>
        )}

        {curriculos && curriculos.length > 0 && (
          <ul className="space-y-2">
            {curriculos.map((c) => (
              <li
                key={c.id}
                className="bg-white rounded-md p-4 shadow-sm flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3"
              >
                <div className="min-w-0">
                  <h3 className="font-semibold text-slate-900 truncate">
                    {c.nome}
                  </h3>
                  <p className="text-xs text-slate-500">
                    Atualizado em{' '}
                    {new Date(c.atualizado_em).toLocaleString('pt-BR')}
                  </p>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <Button
                    variant="secondary"
                    onClick={() => handleBaixar(c.id)}
                  >
                    Baixar PDF
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => navigate(`/editar/${c.id}`)}
                  >
                    Editar
                  </Button>
                  <Button
                    variant="danger"
                    onClick={() => handleExcluir(c.id, c.nome)}
                  >
                    Excluir
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </main>

      <EscolherTemplateModal
        isOpen={idParaBaixar !== null}
        onClose={() => setIdParaBaixar(null)}
        onConfirmar={handleConfirmarTemplate}
      />
    </div>
  )
}
