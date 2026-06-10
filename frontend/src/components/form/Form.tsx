import { FormEvent, useState } from 'react'

import { CurriculoEntrada, DadosPessoais } from '../../types/curriculo'
import { curriculoVazio } from '../../utils/curriculoVazio'
import { podeEnviar } from '../../utils/validacao'

import { Button } from '../ui/Button'
import { Section } from '../ui/Section'
import { Textarea } from '../ui/Textarea'

import { DadosPessoaisFields } from './DadosPessoaisFields'
import { ExperienciaList } from './ExperienciaList'
import { FormacaoList } from './FormacaoList'
import { HabilidadesField } from './HabilidadesField'
import { ProjetoList } from './ProjetoList'

/**
 * Formulario principal do curriculo.
 *
 * Mantem o estado completo em um objeto (curriculo). Cada secao recebe
 * um pedaco desse estado e uma callback para atualizar. O envio so loga
 * no console por enquanto: a integracao com o backend entra na peca 1.5.
 */
export function Form() {
  const [curriculo, setCurriculo] = useState<CurriculoEntrada>(curriculoVazio)

  function atualizarDadosPessoais(
    campo: keyof DadosPessoais,
    valor: string
  ) {
    setCurriculo({
      ...curriculo,
      dados_pessoais: { ...curriculo.dados_pessoais, [campo]: valor },
    })
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    // Por enquanto, so loga. Na peca 1.5 substituimos pela chamada axios.
    console.log('Curriculo pronto para envio:', curriculo)
    alert('Formulario validado! A integracao com o backend entra na proxima peca.')
  }

  const habilitado = podeEnviar(curriculo)

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-3xl mx-auto px-6 py-10"
    >
      <header className="mb-10">
        <h1 className="text-2xl font-bold text-slate-900">
          Gerador de Curriculo em PDF
        </h1>
        <p className="mt-1 text-sm text-slate-600">
          Preencha os campos abaixo e baixe seu curriculo otimizado para ATS.
        </p>
      </header>

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

      <div className="flex flex-col items-end gap-2 mt-10 pt-6 border-t border-slate-200">
        <Button type="submit" disabled={!habilitado}>
          Gerar PDF
        </Button>
        {!habilitado && (
          <p className="text-xs text-slate-500">
            Preencha os campos obrigatorios para habilitar o botao.
          </p>
        )}
      </div>
    </form>
  )
}
