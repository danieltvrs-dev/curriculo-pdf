# Gerador de Currículo em PDF

Aplicação web para montar um currículo a partir de um formulário e baixar o resultado pronto em PDF. Projeto pessoal de estudo e portfólio, com foco em praticar o ciclo completo de desenvolvimento fullstack: do formulário no navegador até o arquivo gerado pelo servidor.

## Stack

**Frontend**
- React 18 com Vite
- TypeScript (configuração didática, strict desligado)
- TailwindCSS para a estilização
- Axios para conversar com a API

**Backend**
- Python com FastAPI
- ReportLab para gerar o PDF
- PostgreSQL com SQLAlchemy para persistência

## Estrutura do projeto

```
curriculo-pdf/
├── backend/     API em FastAPI
├── frontend/    Interface em React
└── README.md
```

Dentro de `backend/app` o código segue uma separação por responsabilidade:

- `routers/` reúne as rotas da API.
- `schemas/` define os formatos de entrada e saída (Pydantic).
- `models/` representa as tabelas do banco.
- `services/` concentra a lógica de negócio, incluindo a geração do PDF.

Do lado do frontend, `src/components` guarda peças reutilizáveis, `src/pages` agrupa telas e `src/services` isola as chamadas HTTP.

## Pré-requisitos

- Python 3.11 ou superior
- Node.js 18 ou superior
- PostgreSQL instalado e rodando (opcional nesta primeira etapa)

## Como rodar

### Backend

No Windows (PowerShell):

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

No Linux ou macOS:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000`. A documentação interativa fica em `http://localhost:8000/docs`.

### Frontend

Em qualquer sistema:

```bash
cd frontend
npm install
```

No Windows:

```powershell
copy .env.example .env
npm run dev
```

No Linux ou macOS:

```bash
cp .env.example .env
npm run dev
```

A interface sobe em `http://localhost:5173`.

## Onde estamos

Etapa atual: estrutura de pastas pronta, ambientes configurados, primeiros arquivos no lugar. Ainda não há funcionalidade implementada. As próximas etapas vão tratar de formulário, validação dos dados, integração entre as duas pontas e a geração do PDF propriamente dita.
