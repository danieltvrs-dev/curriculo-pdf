import { FormEvent, useState } from 'react'

import { usePersistencia } from '../../hooks/usePersistencia'
import { gerarCurriculoPdf } from '../../services/curriculo'
import { CurriculoEntrada, DadosPessoais } from '../../types/curriculo'
import { curriculoVazio } from '../../utils/curriculoVazio'
import { podeEnviar } from '../../utils/validacao'

import { Banner } from '../ui/Banner'
import { Button } from '../ui/Button'
import { Section } from '../ui/Section'
import { Textarea } from '../ui/Textarea'

import { DadosPessoaisFields } from './DadosPessoaisFields'
import { ExperienciaList } from './ExperienciaList'
import { FormacaoList } from './FormacaoList'
import { HabilidadesField } from './HabilidadesField'
import { ProjetoList } from './ProjetoList'

type Feedback = { variant: 'success' | 'error'; message: string }

const CHAVE_RASCUNHO = 'curriculo-pdf:rascunho'

export function Form() {
  const [curriculo, setCurriculo, limparCurriculo] =
    usePersistencia<CurriculoEntrada>(CHAVE_RASCUNHO, curriculoVazio)
  const [enviando, setEnviando] = useState(false)
  const [feedback, setFeedback] = useState<Feedback | null>(null)

  function atualizarDadosPessoais(
    campo: keyof DadosPessoais,
    valor: string
  ) {
    setCurriculo({
      ...curriculo,
      dados_pessoais: { ...curriculo.dados_pessoais, [campo]: valor },
    })
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (enviando) return

    setEnviando(true)
    setFeedback(null)
    try {
      await gerarCurriculoPdf(curriculo)
      setFeedback({
        variant: 'success',
        message: 'PDF gerado e baixado com sucesso.',
      })
    } catch (err: any) {
      console.error('Erro ao gerar PDF:', err)
      if (err?.response?.status === 422) {
        setFeedback({
          variant: 'error',
          message:
            'O servidor nao aceitou algum campo. Verifique os campos com asterisco (*) e tente novamente.',
        })
      } else {
        setFeedback({
          variant: 'error',
          message:
            'Nao foi possivel gerar o PDF. Verifique se a API esta rodando em http://localhost:8000.',
        })
      }
    } finally {
      setEnviando(false)
    }
  }

  function handleLimpar() {
    const confirma = window.confirm(
      'Tem certeza que quer limpar todo o formulario? Os dados serao perdidos.'
    )
    if (!confirma) return
    limparCurriculo()
    setFeedback({ variant: 'success', message: 'Formulario limpo.' })
  }

  const habilitado = podeEnviar(curriculo)

  return (
    <form onSubmit={handleSubmit} className="max-w-3xl mx-auto px-6 py-10">
      <header className="mb-10">
        <h1 className="text-2xl font-bold text-slate-900">
          Gerador de Curriculo em PDF
        </h1>
        <p className="mt-1 text-sm text-slate-600">
          Preencha os campos abaixo e baixe seu curriculo otimizado para ATS.
          Suas alteracoes sao salvas automaticamente neste navegador.
        </p>
      </header>

      {feedback && (
        <Banner
          variant={feedback.variant}
          message={feedback.message}
          onClose={() => setFeedback(null)}
          autoCloseMs={feedback.variant === 'success' ? 4000 : undefined}
        />
      )}

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
      </Section>

      <Section
        title="Experiencia Profissional"
        description="Pode ficar vazio se voce esta comecando. Sem problema."
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
        description="Palavras-chave que o ATS usa para casar com vagas. Quanto mais relevantes, melhor."
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
        description="Opcional, mas pesa muito para quem esta comecando."
      >
        <ProjetoList
          projetos={curriculo.projetos}
          onChange={(novos) =>
            setCurriculo({ ...curriculo, projetos: novos })
          }
        />
      </Section>

      <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-end gap-3 mt-10 pt-6 border-t border-slate-200">
        <Button variant="ghost" type="button" onClick={handleLimpar}>
          Limpar formulario
        </Button>
        <div className="flex flex-col items-end gap-2">
          <Button type="submit" disabled={!habilitado || enviando}>
            {enviando ? 'Gerando PDF...' : 'Gerar PDF'}
          </Button>
          {!habilitado && !enviando && (
            <p className="text-xs text-slate-500">
              Preencha os campos obrigatorios para habilitar o botao.
            </p>
          )}
        </div>
      </div>
    </form>
  )
}
