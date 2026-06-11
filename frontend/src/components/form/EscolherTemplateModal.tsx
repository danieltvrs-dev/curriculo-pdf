import { useState } from 'react'

import { TEMPLATES_PDF, TemplatePdf } from '../../services/meusCurriculos'
import { Button } from '../ui/Button'
import { Modal } from '../ui/Modal'

type Props = {
  isOpen: boolean
  onClose: () => void
  onConfirmar: (template: TemplatePdf) => void
}

/**
 * Modal de selecao de template do PDF.
 *
 * O onConfirmar dispara a geracao com o template escolhido.
 * O onClose fecha sem gerar nada.
 */
export function EscolherTemplateModal({ isOpen, onClose, onConfirmar }: Props) {
  const [selecionado, setSelecionado] = useState<TemplatePdf>('classico')

  function handleConfirmar() {
    onConfirmar(selecionado)
    onClose()
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Escolher template do PDF"
    >
      <div className="space-y-3">
        {TEMPLATES_PDF.map((op) => (
          <label
            key={op.id}
            className={`block p-4 border rounded-md cursor-pointer transition-colors ${
              selecionado === op.id
                ? 'border-slate-800 bg-slate-50'
                : 'border-slate-200 hover:border-slate-400'
            }`}
          >
            <div className="flex items-start gap-3">
              <input
                type="radio"
                name="template"
                value={op.id}
                checked={selecionado === op.id}
                onChange={() => setSelecionado(op.id)}
                className="mt-1"
              />
              <div className="flex-1">
                <h3 className="font-semibold text-slate-900">{op.nome}</h3>
                <p className="text-sm text-slate-600 mt-1">{op.descricao}</p>
              </div>
            </div>
          </label>
        ))}

        <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
          <Button variant="ghost" type="button" onClick={onClose}>
            Cancelar
          </Button>
          <Button type="button" onClick={handleConfirmar}>
            Baixar PDF
          </Button>
        </div>
      </div>
    </Modal>
  )
}
