# Gerador de Currículo em PDF

Aplicação fullstack para montar um currículo a partir de um formulário e baixar como PDF otimizado para sistemas ATS (Applicant Tracking Systems). Cada usuário tem sua conta, salva quantos currículos quiser, e pode regerar em três templates visuais diferentes.

Projeto pessoal de estudo e portfólio. Construído passo a passo, em conversa com IA, com foco em entender cada decisão técnica.

> Stack: React + TypeScript + Tailwind no front, Python + FastAPI + SQLAlchemy no back, ReportLab para gerar PDF, Google Gemini para melhorar textos com IA.

---

## Funcionalidades

- **Cadastro e login** com senha bcrypt, access token JWT curto + refresh token em cookie httpOnly (revogável no backend).
- **CRUD de currículos** por usuário, persistido em banco (SQLite local, PostgreSQL pronto para deploy).
- **Editor completo** com seções de Dados Pessoais, Resumo Profissional, Experiência, Formação, Habilidades, Projetos, Idiomas e Certificações.
- **Gerador de PDF ATS-friendly**: uma coluna, fonte Helvetica, hierarquia textual clara, sem ícones decorativos.
- **3 templates visuais**: Clássico (sóbrio), Moderno (azul, com linha decorativa) e Compacto (mais conteúdo por página). Todos ATS-compatíveis.
- **Melhorar com IA** no resumo profissional e descrições de experiência/projeto. Mostra "Antes / Depois" em um modal antes de aceitar.
- **TagInput** com chips removíveis para tecnologias e habilidades.
- **Autosave** em localStorage no editor, sem perder o que digitou.
- **Feedback visual** com banners e mensagens claras de erro/sucesso.
- **Validações automáticas** com Pydantic no backend, validação leve no frontend para UX rápida.

---

## Stack

### Frontend
- **React 18** com **Vite**
- **TypeScript** (configuração didática, strict desligado)
- **TailwindCSS** para estilização
- **React Router v6** para roteamento
- **Axios** com interceptor para anexar JWT automaticamente
- **Context API** para autenticação

### Backend
- **Python 3.13** com **FastAPI**
- **Pydantic** para validação de schemas
- **SQLAlchemy 2.0** (modo declarativo com `Mapped[]`)
- **SQLite** local, **PostgreSQL** pronto para produção (psycopg2-binary)
- **passlib + bcrypt** para hash de senha
- **python-jose** para JWT
- **ReportLab** para geração de PDF
- **google-genai** para chamadas ao Gemini

### IA
- **Google Gemini 2.5 Flash** via free tier oficial (sem cartão de crédito).
- Chave de API guardada apenas no `.env` do backend, nunca exposta ao frontend.

---

## Como rodar localmente

### Pré-requisitos

- **Python 3.11+**
- **Node.js 18+**
- **Git**

### 1. Clone o repositório

```bash
git clone https://github.com/danieltvrs-dev/curriculo-pdf.git
cd curriculo-pdf
```

### 2. Backend

**Em qualquer sistema:**

```bash
cd backend
python -m venv venv
```

**Ative o ambiente virtual:**

- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Linux/macOS:** `source venv/bin/activate`

Se aparecer `(venv)` no início do prompt, ativou.

**Instale as dependências e configure o `.env`:**

```bash
pip install -r requirements.txt
```

**Windows:** `copy .env.example .env`
**Linux/macOS:** `cp .env.example .env`

Edite o `backend/.env` e configure pelo menos:

- `JWT_SECRET` — qualquer string longa e aleatória (gere com `python -c "import secrets; print(secrets.token_urlsafe(64))"`).
- `GOOGLE_API_KEY` — opcional. Necessária só para a feature de "Melhorar com IA". Pegue em [aistudio.google.com](https://aistudio.google.com/apikey) (free tier, sem cartão).

**Suba o servidor:**

```bash
uvicorn app.main:app --reload --reload-dir app
```

API em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

### 3. Frontend

**Em outro terminal:**

```bash
cd frontend
npm install
```

**Windows:** `copy .env.example .env`
**Linux/macOS:** `cp .env.example .env`

```bash
npm run dev
```

Interface em `http://localhost:5173`.

---

## Variáveis de ambiente

### `backend/.env`

| Variável | Obrigatório | Descrição |
|---|---|---|
| `APP_ENV` | não | Ambiente da aplicação (development/production) |
| `DATABASE_URL` | não | URL do banco. Padrão: SQLite local (`sqlite:///./curriculo_pdf.db`) |
| `CORS_ORIGINS` | não | Origens permitidas no CORS. Padrão: `http://localhost:5173` |
| `JWT_SECRET` | **sim** | Chave para assinar tokens JWT |
| `JWT_ALGORITHM` | não | Algoritmo do JWT. Padrão: `HS256` |
| `ACCESS_TOKEN_EXPIRA_MINUTOS` | não | Validade do access token. Padrão: `15` |
| `REFRESH_TOKEN_EXPIRA_MINUTOS` | não | Validade do refresh token. Padrão: `43200` (30 dias) |
| `COOKIE_SECURE` | não | `true` em produção (HTTPS), `false` em dev local |
| `COOKIE_SAMESITE` | não | `lax` em mesmo site, `none` em cross-site (exige HTTPS) |
| `GOOGLE_API_KEY` | apenas para IA | Chave do Google AI Studio |
| `GEMINI_MODEL` | não | Modelo Gemini. Padrão: `gemini-2.5-flash` |

### `frontend/.env`

| Variável | Obrigatório | Descrição |
|---|---|---|
| `VITE_API_URL` | não | URL base do backend. Padrão: `http://localhost:8000` |

---

## Estrutura do projeto

```
curriculo-pdf/
├── backend/
│   ├── app/
│   │   ├── main.py                 ponto de entrada do FastAPI
│   │   ├── database.py             engine + SessionLocal + get_db
│   │   ├── dependencies.py         get_current_user (proteção de rotas)
│   │   ├── models/                 modelos SQLAlchemy (User, Curriculo, RefreshToken)
│   │   ├── schemas/                schemas Pydantic
│   │   ├── routers/                endpoints HTTP por tema
│   │   │   ├── auth.py             /auth/registrar, /auth/login, /auth/refresh, /auth/logout, /auth/me
│   │   │   ├── curriculo.py        /curriculos (anônimo, legado)
│   │   │   ├── meus_curriculos.py  /meus-curriculos (CRUD protegido)
│   │   │   └── ia.py               /ia/melhorar-* (proxy seguro pro Gemini)
│   │   └── services/               regras de negócio
│   │       ├── auth.py             hash bcrypt + access JWT + refresh token + config cookie
│   │       ├── gerador_pdf.py      despachador de templates
│   │       ├── templates/          comum.py + classico.py + moderno.py + compacto.py
│   │       └── melhorador_ia.py    chamadas ao Gemini
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 BrowserRouter + AuthProvider
│   │   ├── main.tsx                ponto de entrada do Vite
│   │   ├── contexts/               AuthContext
│   │   ├── hooks/                  usePersistencia (localStorage)
│   │   ├── pages/                  Login, Cadastro, MeusCurriculos, EditorCurriculo
│   │   ├── components/
│   │   │   ├── ProtectedRoute.tsx
│   │   │   ├── form/               sub-componentes das seções do editor
│   │   │   └── ui/                 Input, Textarea, Select, Button, Modal, Banner, TagInput
│   │   ├── services/               api (axios), auth, meusCurriculos, ia
│   │   ├── types/                  tipos espelhando schemas do back
│   │   └── utils/                  curriculoVazio, prepararEnvio, validacao
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.example
└── README.md
```

---

## Decisões de design

### Por que ATS-friendly?

Grandes empresas usam software para filtrar currículos antes de um humano olhar. Layouts em duas colunas, ícones decorativos e fontes exóticas confundem o parser. Um currículo bonito mas mal parseado é descartado.

Por isso o gerador segue regras estritas:
- Uma única coluna
- Fonte Helvetica padrão
- Cabeçalhos textuais em MAIÚSCULAS (parser reconhece como seção)
- Datas em formato consistente (`MM/AAAA`)
- Tecnologias e habilidades como texto separado por vírgula, nunca como tabelas ou tags coloridas
- Margens generosas (≥ 1,5 cm)

O template "Moderno" adiciona cor decorativa mas mantém todas as regras de parsing.

### Por que SQLite local?

Em desenvolvimento, instalar PostgreSQL é fricção desnecessária. SQLite é um arquivo, criado automaticamente pelo SQLAlchemy no primeiro startup. O código é idêntico ao do PostgreSQL graças ao ORM. Para produção, basta trocar a `DATABASE_URL`.

### Por que Google Gemini para a IA?

Anthropic Claude e OpenAI exigem cartão de crédito para gerar chave da API. Gemini tem free tier oficial (15 chamadas/min, 1500/dia) sem cobrança. Para um projeto de portfólio, é mais que suficiente.

### Por que access token + refresh token em cookie httpOnly?

A primeira versão da auth usava um JWT longo guardado em `localStorage`. Era didática mas tinha duas fragilidades reais: vulnerável a XSS (qualquer JS injetado lê o token) e não permitia logout efetivo (o token continuava válido até expirar).

A versão atual usa o padrão moderno da indústria:

- **Access token** (JWT) com vida **curta** (15 min). Vive em memória do React, anexado no header `Authorization` automaticamente. Se vazar, janela de risco é curta.
- **Refresh token** opaco com vida **longa** (30 dias). Vai num **cookie httpOnly**, inacessível por JavaScript. O backend armazena só o hash SHA-256, igual senha.
- **Rotação a cada refresh:** o token antigo é revogado, um novo é emitido. Defesa contra replay.
- **Logout real:** o backend marca o refresh como `revogado_em` no banco. Próxima tentativa de refresh falha.

O interceptor do axios faz o refresh transparente quando uma request volta 401: chama `/auth/refresh`, recebe novo access, retenta a request original. O usuário não percebe nada.

### Por que `dados: JSON` em vez de normalizar?

Cada currículo é usado todo de uma vez (gerar PDF). Não tem caso de uso de consultar "todos os usuários com habilidade X". Por isso o `dados` é uma coluna JSON, evitando 6 tabelas relacionais que ninguém consulta separadamente. Trade-off claro: ganho em simplicidade, perda em consultas analíticas (não precisamos).

---

## Como funciona o fluxo principal

1. Usuário cadastra/loga → backend devolve **access token** no body (vai pra memória do React) e **refresh token** num cookie httpOnly.
2. Interceptor do axios anexa `Authorization: Bearer <access_token>` em toda request.
3. Backend valida o JWT em `get_current_user` (dependência), busca o User no banco.
4. Quando o access expira, o interceptor pega o 401, chama `/auth/refresh` (browser envia o cookie automaticamente), recebe novo access e retenta a request original. O usuário não percebe.
4. Usuário preenche o formulário, clica em **Salvar e baixar PDF**.
5. Frontend faz `POST /meus-curriculos` com os dados e recebe o registro persistido.
6. Modal abre para escolher o template (Clássico, Moderno, Compacto).
7. Frontend faz `GET /meus-curriculos/{id}/pdf?template=X` com `responseType: 'blob'`.
8. Backend valida ownership (currículo pertence ao usuário), gera bytes do PDF com o template escolhido, retorna com `Content-Disposition: attachment`.
9. Frontend cria URL temporária do Blob, simula clique em anchor invisível, baixa o arquivo.

Para a feature de IA:
1. Usuário escreve um resumo no editor.
2. Clica em **✨ Melhorar com IA**.
3. Frontend chama `POST /ia/melhorar-resumo` com o texto.
4. Backend monta o prompt (mantenha o sentido, não invente nada, otimize para ATS), chama Gemini, devolve só o texto.
5. Frontend mostra modal "Antes / Depois" para o usuário aceitar ou descartar.

---

## Roadmap

### Concluído

**Fase 1 — MVP anônimo end-to-end:**
- Schemas Pydantic do currículo
- Rota POST de geração de PDF
- Gerador ATS-friendly com ReportLab
- Formulário no React
- Integração axios + download
- Banner de feedback + autosave + botão limpar
- Botão "Melhorar com IA" no resumo profissional

**Fase 2 — Autenticação e persistência:**
- Modelos User e Curriculo (SQLAlchemy + SQLite)
- Hash bcrypt + JWT + endpoints `/auth/*`
- CRUD protegido em `/meus-curriculos`
- React Router + Context de autenticação + rotas protegidas
- Telas Login, Cadastro, Meus Currículos, Editor

**Extras:**
- IA também em descrição de Experiência e Projeto
- Campos de Idiomas e Certificações
- 3 templates de PDF (Clássico, Moderno, Compacto)
- Refresh token + cookie httpOnly com rotação a cada refresh

### Próximos

- Deploy: backend em Render/Railway, frontend em Vercel, banco PostgreSQL
- Mais templates de PDF
- Preview do PDF antes de baixar
- Exportar/importar currículo em JSON
- Compartilhar currículo via link público (read-only)
- Internacionalização (currículo em inglês)

---

## Autoria

Construído por [Daniel Tavares](https://github.com/danieltvrs-dev) como projeto de estudo durante a graduação em Análise e Desenvolvimento de Sistemas. 
