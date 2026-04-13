# fabric-mcp — Gerenciador MCP para Microsoft Fabric

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0%2B-green.svg)](https://spec.modificationprotocol.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Um servidor **MCP (Model Context Protocol)** em Python para automatizar Microsoft Fabric via Claude Code, GitHub Copilot, Cursor ou Gemini.  
> **65+ ferramentas** para workspaces, lakehouses, notebooks, pipelines, warehouses, semantic models e reports.

---

## 📚 Documentação Completa

**Toda a documentação está em [`docs/`](docs/) — comece por aí!**

| 🚀 Começar | 🖥️ Instalar | 📖 Aprender | 🔍 Referenciar |
|---|---|---|---|
| 👉 [GET_STARTED.md](docs/GET_STARTED.md) | [INSTALLATION.md](docs/INSTALLATION.md) | [INDEX.md](docs/INDEX.md) | [TOOLS_SUMMARY.md](docs/TOOLS_SUMMARY.md) |
| [QUICK_START.md](docs/QUICK_START.md) | Windows, macOS, Linux | [ARCHITECTURE.md](docs/ARCHITECTURE.md) | 65+ ferramentas catálogadas |

---

## ⚡ 5-Minuto Setup

```bash
git clone https://github.com/seu-usuario/mcp_fabric.git
cd mcp_fabric

# Python (3.11+)
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Linux/macOS
pip install -r requirements.txt

# Config
cp .env.example .env
# Preencher: FABRIC_TENANT_ID, FABRIC_CLIENT_ID, FABRIC_CLIENT_SECRET

# Registrar no Claude
npm install -g @anthropic-ai/claude-cli
claude mcp add fabric -- /CAMINHO/COMPLETO/.venv/Scripts/python.exe server.py

# Usar!
claude code
# Digitar: "Liste os workspaces do Fabric"
```

👉 **Detalhes em [docs/INSTALLATION.md](docs/INSTALLATION.md)**

---

## 🎯 O Quê é Isto?

**fabric-mcp** é um servidor MCP que torna as APIs do Microsoft Fabric acessíveis como **tools** para agentes de IA:

```
Claude / Copilot / Cursor
    ↓ tool call
fabric-mcp (Python)
    ↓ REST API
Microsoft Fabric + Azure AD  
    ↓ resultado
Claude / Copilot / Cursor
```

### Casos de uso

- ✅ Documentar automaticamente todos os workspaces
- ✅ Criar pipeline Medallion (Bronze/Silver/Gold) end-to-end
- ✅ Auditar permissões e governança
- ✅ Executar queries DAX/SQL interativamente  
- ✅ Orquestrar pipelines ETL/ELT

---

## 🚀 65+ Ferramentas

- **Workspaces** (8): list, create, delete, manage roles
- **Lakehouses** (7): create, read files, write files, SQL
- **Warehouses** (5): create, execute SQL, connection info
- **Notebooks** (8): create, update, execute, logs
- **Pipelines** (6): create, run, monitor
- **Spark Jobs** (6): create, run, track status
- **Semantic Models** (6): create, refresh, DAX queries
- **Reports** (5): create, share, export
- **OneLake** (8): list, upload, download, copy files

📋 **[Ver catálogo completo em docs/TOOLS_SUMMARY.md](docs/TOOLS_SUMMARY.md)**

---

## 📋 Pré-requisitos

- **Python 3.11+** 
- **ODBC Driver 18** for SQL Server (se usar Warehouse)
- **Service Principal** (Tenant ID, Client ID, Secret)
- **Claude CLI**, Copilot ou Cursor

👉 **[Setup por plataforma em docs/INSTALLATION.md](docs/INSTALLATION.md)**

---

## 🏗️ Estrutura

```
mcp_fabric/
├── README.md                 (este arquivo — landing page)
├── requirements.txt
├── .env.example
├── server.py, auth.py, config.py, client.py
├── tools/                    (65+ ferramentas)
├── agents/                   (3 agentes especializados)
├── skills/                   (9 domain guides)
└── docs/                     (📚 DOCUMENTAÇÃO COMPLETA)
    ├── GET_STARTED.md        ← Comece aqui!
    ├── QUICK_START.md
    ├── INSTALLATION.md
    ├── INDEX.md
    ├── ARCHITECTURE.md
    ├── TOOLS_SUMMARY.md
    ├── CONTRIBUTING.md
    ├── ROADMAP.md
    └── ... (+ 5 arquivos)
```

---

## 🎓 Próximas Etapas

1. **👉 [docs/GET_STARTED.md](docs/GET_STARTED.md)** (5 minutos)
2. Escolha seu caminho:
   - **Quer instalar?** → [docs/INSTALLATION.md](docs/INSTALLATION.md)
   - **Quer explorar?** → [docs/TOOLS_SUMMARY.md](docs/TOOLS_SUMMARY.md)
   - **Quer entender tudo?** → [docs/INDEX.md](docs/INDEX.md)
   - **Quer contribuir?** → [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 🤝 Contribuindo

Ver [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## 📄 Licença

MIT — Use livremente.

---

**Pronto? 👉 [Comece com docs/GET_STARTED.md](docs/GET_STARTED.md)**
# fabric-mcp — Gerenciador MCP para Microsoft Fabric

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0%2B-green.svg)](https://spec.modificationprotocol.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **O quê?** Um servidor MCP (Model Context Protocol) em Python que expõe todas as operações do Microsoft Fabric como ferramentas invocáveis por agentes de IA.  
> **Por quê?** Automatize qualquer ação no Fabric diretamente via Claude Code, GitHub Copilot ou Cursor — workspaces, lakehouses, notebooks, pipelines, warehouses, semantic models, relatórios — **sem abrir o portal**.  
> **Como?** Autenticação nativa via **Service Principal** (sem login interativo) + protocolo **stdio** (processo local).

---

## � Documentação

**Toda a documentação está em [`docs/`](docs/)**

👉 **[Comece aqui: GET_STARTED.md](docs/GET_STARTED.md)** (5 minutos)

| Você quer... | Documento |
|---|---|
| **Começar rápido** | [docs/QUICK_START.md](docs/QUICK_START.md) |
| **Setup completo (por SO)** | [docs/INSTALLATION.md](docs/INSTALLATION.md) |
| **Guia completo** | [docs/INDEX.md](docs/INDEX.md) |
| **Referência de tools** | [docs/TOOLS_SUMMARY.md](docs/TOOLS_SUMMARY.md) |
| **Design técnico** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **Como contribuir** | [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) |
| **Roadmap** | [docs/ROADMAP.md](docs/ROADMAP.md) |
| **Mapa de docs** | [docs/DOCS_MAP.md](docs/DOCS_MAP.md) |

---

## ⚡ Quick Start

```bash
# 1. Ver prérequísitos
# 👉 docs/INSTALLATION.md (seu SO)

# 2. Instalar
git clone https://github.com/seu-usuario/mcp_fabric.git
cd mcp_fabric
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Configurar
cp .env.example .env
# Preencher .env com credenciais

# 4. Registrar no Claude
claude mcp add fabric -- /caminho/completo/.venv/Scripts/python.exe server.py

# 5. Usar
claude code
```

---

## 🚀 Features

**fabric-mcp** é um servidor que implementa o protocolo MCP (Model Context Protocol) para oferecer ao Claude (ou outro agente de IA) acesso total às APIs do Microsoft Fabric através de **tools** — funções invocáveis com parâmetros tipados e respostas estruturadas.
