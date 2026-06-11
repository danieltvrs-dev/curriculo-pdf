import { FormEvent, useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { Banner } from '../components/ui/Banner'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Section } from '../components/ui/Section'
import { Textarea } from '../components/ui/Textarea'

import { CertificacaoList } from '../components/form/CertificacaoList'
import { DadosPessoaisFields } from '../components/form/DadosPessoaisFields'
import { ExperienciaList } from '../components/form/ExperienciaList'
import { FormacaoList } from '../components/form/FormacaoList'
import { HabilidadesField } from '../components/form/HabilidadesField'
import { IdiomaList } from '../components/form/IdiomaList'
import { MelhorarResumoButton } from '../components/form/MelhorarResumoButton'
import { ProjetoList } from '../components/form/ProjetoList'

import * as service from '../services/meusCurriculos'
import { CurriculoEntrada, DadosPessoais } from '../types/curriculo'
import { curriculoVazio } from '../utils/curriculoVazio'
import { podeEnviar } from '../utils/validacao'

type Feedback = { variant: 'success' | 'error'; message: string }

export function EditorCurriculo() {
  const { id } = useParams<{ id?: string }>()
  const navigate = useNavigate()
  const isEditando = Boolean(id)

  const [carregando, setCarregando] = useState(isEditando)
  const [nome, setNome] = useState('')
  const [curriculo, setCurriculo] = useState<CurriculoEntrada>(curriculoVazio)
  const [enviando, setEnviando] = useState(false)
  const [feedback, setFeedback] = useState<Feedback | null>(null)

  useEffect(() => {
    if (!id) return
    service
      .buscar(parseInt(id, 10))
      .then((cv) => {
        setNome(cv.nome)
        setCurriculo(cv.dados)
      })
      .catch(() => {
        setFeedback({ variant: 'error', message: 'Curriculo nao encontrado.' })
      })
      .finally(() => setCarregando(false))
  }, [id])

  function atualizarDadosPessoais(campo: keyof DadosPessoais, valor: string) {
    setCurriculo({
      ...curriculo,
      dados_pessoais: { ...curriculo.dados_pessoais, [campo]: valor },
    })
  }

  async function salvar(): Promise<number | null> {
    try {
      if (isEditando && id) {
        const cv = await service.atualizar(
          parseInt(id, 10),
          nome.trim(),
          curriculo
        )
        return cv.id
      }
      const cv = await service.criar(nome.trim(), curriculo)
      return cv.id
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setFeedback({
        variant: 'error',
        message: typeof detail === 'string' ? detail : 'Erro ao salvar.',
      })
      return null
    }
  }

  async function handleSalvar(e: FormEvent) {
    e.preventDefault()
    if (enviando) return
    setEnviando(true)
    setFeedback(null)
    const cvId = await salvar()
    if (cvId !== null) {
      setFeedback({ variant: 'success', message: 'Curriculo salvo.' })
      if (!isEditando) navigate(`/editar/${cvId}`, { replace: true })
    }
    setEnviando(false)
  }

  async function handleSalvarEBaixar() {
    if (enviando) return
    setEnviando(true)
    setFeedback(null)
    const cvId = await salvar()
    if (cvId !== null) {
      try {
        await service.baixarPdf(cvId)
        setFeedback({ variant: 'success', message: 'PDF gerado e baixado.' })
        if (!isEditando) navigate(`/editar/${cvId}`, { replace: true })
      } catch {
        setFeedback({
          variant: 'error',
          message: 'Salvou, mas falhou ao baixar o PDF.',
        })
      }
    }
    setEnviando(false)
  }

  const habilitado = nome.trim().length > 0 && podeEnviar(curriculo)

  if (carregando) {
    return (
      <div className="min-h-screen flex items-center justify-center text-slate-500">
        Carregando...
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-3xl mx-auto px-6 py-4 flex justify-between items-center">
          <button
            type="button"
            onClick={() => navigate('/')}
            className="text-sm text-slate-600 hover:text-slate-900"
          >
            ← Voltar
          </button>
          <h1 className="text-lg font-semibold text-slate-900">
            {isEditando ? 'Editar curriculo' : 'Novo curriculo'}
          </h1>
          <div className="w-16" />
        </div>
      </header>

      <form onSubmit={handleSalvar} className="max-w-3xl mx-auto px-6 py-10">
        {feedback && (
          <Banner
            variant={feedback.variant}
            message={feedback.message}
            onClose={() => setFeedback(null)}
            autoCloseMs={feedback.variant === 'success' ? 4000 : undefined}
          />
        )}

        <Section
          title="Nome do curriculo"
          description="So pra voce identificar este curriculo na sua lista. Nao aparece no PDF."
        >
          <Input
            label="Nome interno"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            placeholder="Ex: CV Backend, CV Geral, CV para vaga X"
            maxLength={120}
          />
        </Section>

        <Section
          title="Dados Pessoais"
          description="Os campos que recrutadores precisam para te contatar."
        >
          <DadosPessoaisFields
            dados={curriculo.dados_pessoais}
            onChange={atualizarDadosPessoais}
          />
        </Section>

        <Section
          title="Resumo Profissional"
          description="Um paragrafo (50 a 600 caracteres) com seu pitch. Inclua tecnologias e areas de interesse para o ATS extrair palavras-chave."
        >
          <Textarea
            label="Resumo"
            required
            value={curriculo.resumo_profissional}
            onChange={(e) =>
              setCurriculo({ ...curriculo, resumo_profissional: e.target.value })
            }
            maxLength={600}
            hint={`${curriculo.resumo_profissional.length}/600 caracteres (minimo 50)`}
          />
          <MelhorarResumoButton
            textoAtual={curriculo.resumo_profissional}
            onAceitar={(texto) =>
              setCurriculo({ ...curriculo, resumo_profissional: texto })
            }
          />
        </Section>

        <Section
          title="Experiencia Profissional"
          description="Pode ficar vazio se voce esta comecando."
        >
          <ExperienciaList
            experiencias={curriculo.experiencias}
            onChange={(novas) =>
              setCurriculo({ ...curriculo, experiencias: novas })
            }
          />
        </Section>

        <Section
          title="Formacao Academica"
          description="Pelo menos uma formacao e obrigatoria."
        >
          <FormacaoList
            formacoes={curriculo.formacoes}
            onChange={(novas) =>
              setCurriculo({ ...curriculo, formacoes: novas })
            }
          />
        </Section>

        <Section
          title="Habilidades Tecnicas"
          description="Palavras-chave que o ATS usa para casar com vagas."
        >
          <HabilidadesField
            habilidades={curriculo.habilidades}
            onChange={(novas) =>
              setCurriculo({ ...curriculo, habilidades: novas })
            }
          />
        </Section>

        <Section
          title="Projetos"
          description="Opcional, mas pesa pra quem esta comecando."
        >
          <ProjetoList
            projetos={curriculo.projetos}
            onChange={(novos) =>
              setCurriculo({ ...curriculo, projetos: novos })
            }
          />
        </Section>

        <Section
          title="Idiomas"
          description="Opcional. Inclua so se for relevante para a vaga."
        >
          <IdiomaList
            idiomas={curriculo.idiomas}
            onChange={(novos) =>
              setCurriculo({ ...curriculo, idiomas: novos })
            }
          />
        </Section>

        <Section
          title="Certificacoes"
          description="Opcional. Cursos, certificacoes profissionais e treinamentos relevantes."
        >
          <CertificacaoList
            certificacoes={curriculo.certificacoes}
            onChange={(novas) =>
              setCurriculo({ ...curriculo, certificacoes: novas })
            }
          />
        </Section>

        <div className="flex flex-col sm:flex-row justify-end gap-2 mt-10 pt-6 border-t border-slate-200">
          <Button
            variant="secondary"
            type="button"
            onClick={handleSalvarEBaixar}
            disabled={!habilitado || enviando}
          >
            Salvar e baixar PDF
          </Button>
          <Button type="submit" disabled={!habilitado || enviando}>
            {enviando ? 'Salvando...' : 'Salvar'}
          </Button>
        </div>
        {!habilitado && !enviando && (
          <p className="text-xs text-slate-500 text-right mt-2">
            Preencha o nome do curriculo e os campos obrigatorios (*).
          </p>
        )}
      </form>
    </div>
  )
}
