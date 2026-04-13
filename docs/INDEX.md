# 📖 Índice de Documentação — fabric-mcp

> Guia para navegar toda a documentação do projeto. Escolha seu ponto de partida abaixo.

---

## 🚀 Primeiro acesso? Comece aqui

| Se você quer... | Leia... | Tempo |
|---|---|---|
| **Instalação passo-a-passo** | [INSTALLATION.md](INSTALLATION.md) | 10-30 min |
| **Instalar rapidinho** | [QUICK_START.md](QUICK_START.md) | 5 min |
| **Entender o quê é** | [README.md](README.md) § O que é fabric-mcp | 3 min |
| **Ver todos os exemplos** | [README.md](README.md) § Exemplos de uso | 10 min |
| **Usar com seu IDE favorito** | [README.md](README.md) § Integrações | 5 min |
| **Que tools existem?** | [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md) | 15 min |

---

## 🔧 Desenvolvimento & Troubleshooting

| Se você quer... | Leia... | Tempo |
|---|---|---|
| **Instalar passo-a-passo (por SO)** | [INSTALLATION.md](INSTALLATION.md) | 20-30 min |
| **Entender a arquitetura** | [ARCHITECTURE.md](ARCHITECTURE.md) | 20 min |
| **Adicionar uma tool nova** | [ARCHITECTURE.md](ARCHITECTURE.md) § Adding a New Tool | 10 min |
| **Contribuir código** | [CONTRIBUTING.md](CONTRIBUTING.md) | 10 min |
| **Resolver problema** | [README.md](README.md) § Troubleshooting rápido | 5-15 min |
| **Design detalhado** | [SDD.md](SDD.md) | 30 min |

---

## 🎓 Guias por domínio

### Data Engineering

- 🏢 **Workspaces**: [skills/workspace-management/SKILL.md](skills/workspace-management/SKILL.md)
- 📁 **Lakehouses & OneLake**: [skills/onelake/SKILL.md](skills/onelake/SKILL.md)
- ⚡ **Spark & Notebooks**: [skills/spark-authoring/SKILL.md](skills/spark-authoring/SKILL.md) + [spark-consumption](skills/spark-consumption/SKILL.md)
- 🛢️ **SQL & Warehouses**: [skills/sqldw-authoring/SKILL.md](skills/sqldw-authoring/SKILL.md) + [sqldw-consumption](skills/sqldw-consumption/SKILL.md)
- 🔄 **Pipelines & ETL**: https://github.com/seu-usuario/mcp_fabric/tree/main/skills/e2e-medallion

### Analytics & BI

- 📊 **Semantic Models & DAX**: [skills/powerbi-authoring/SKILL.md](skills/powerbi-authoring/SKILL.md) + [powerbi-consumption](skills/powerbi-consumption/SKILL.md)
- 📈 **Reports & Power BI**: [skills/powerbi-authoring/SKILL.md](skills/powerbi-authoring/SKILL.md)

### Administração

- 👨‍💼 **Fabric Admin Agent**: [agents/FabricAdmin.agent.md](agents/FabricAdmin.agent.md)
- 🔐 **Governança & Permissões**: [README.md](README.md) § Configuração Azure AD

---

## 📚 Roadmap por arquivo

### 📄 Arquivos principais

```
mcp_fabric/
├── README.md                    ← Documentação principal (novo/grande)
├── QUICK_START.md               ← Guia rápido (5 min)
├── ARCHITECTURE.md              ← Design técnico e como estender
├── CONTRIBUTING.md              ← Como contribuir
├── TOOLS_SUMMARY.md             ← Referência de todas as 65+ tools
├── INDEX.md                     ← Este arquivo
│
├── SDD.md                       ← Software Design Document (original)
├── README.md (antigo)           ← Ainda útil para troubleshooting
│
├── requirements.txt             ← Deps
├── .env.example                 ← Template de config
├── server.py                    ← Entry point MCP
├── auth.py                      ← Token manager
├── config.py                    ← Settings
├── client.py                    ← HTTP client
├── exceptions.py                ← Error handling
│
├── tools/                       ← 65+ tools implementadas
├── agents/                      ← 3 agentes especializados
├── skills/                      ← 9 domain guides
└── docs/                        ← Docs adicionais
```

---

## 🗺️ Mapa mental

```
fabric-mcp
│
├─ O QUÊ?
│  └─ README.md § O que é fabric-mcp?
│
├─ COMO USAR?
│  ├─ QUICK_START.md (5 min)
│  ├─ INSTALLATION.md (detalhado por SO)
│  ├─ README.md § Instalação local
│  ├─ README.md § Integrações (Claude / Copilot / Cursor / Gemini)
│  └─ TOOLS_SUMMARY.md (procurar tool)
│
├─ FERRAMENTAS (65+ tools)
│  ├─ Workspaces (8)
│  ├─ Lakehouses (7)
│  ├─ Warehouses (5)
│  ├─ Notebooks (8)
│  ├─ Pipelines (6)
│  ├─ Spark Jobs (6)
│  ├─ Semantic Models (6)
│  ├─ Reports (5)
│  └─ OneLake (8)
│
├─ AGENTES & SKILLS
│  ├─ FabricAdmin (administração)
│  ├─ FabricDataEngineer (orchestração)
│  ├─ FabricAppDev (desenvolvimento)
│  └─ 9 skills temáticos
│
├─ ARQUITETURA
│  ├─ ARCHITECTURE.md (fluxos, design)
│  └─ SDD.md (design completo)
│
└─ CONTRIBUIR
   ├─ CONTRIBUTING.md (workflow)
   └─ ARCHITECTURE.md § Adding a New Tool
```

---

## 🎯 Cenários de uso

### Cenário 1: Quero usar fabric-mcp rapidinho

1. Ler [QUICK_START.md](QUICK_START.md) (5 min)
2. Seguir setup (2 min)
3. Rodar primeiro comando no Claude (1 min)

**Total: 8 min** ✅

---

### Cenário 2: Quero explorar todas as possibilidades

1. Ler [README.md](README.md) completo
2. Procurar na [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md)
3. Testar exemplos de cada skill

**Total: 1-2 horas** 📚

---

### Cenário 3: Encontrei um bug / erro

1. Ler [README.md](README.md) § Troubleshooting rápido
2. Se não resolver → [README.md](README.md) § Verificação e Troubleshooting
3. Ainda não? → Abrir [GitHub Issue](https://github.com/seu-usuario/mcp_fabric/issues) com detalhes

**Total: 10-30 min** 🔧

---

### Cenário 4: Quero adicionar uma tool

1. Ler [ARCHITECTURE.md](ARCHITECTURE.md) § Fluxo de uma requisição
2. Ler [ARCHITECTURE.md](ARCHITECTURE.md) § Adding a New Tool
3. Implementar + testar
4. Ler [CONTRIBUTING.md](CONTRIBUTING.md)
5. Abrir PR

**Total: 1-2 horas** 💻

---

### Cenário 5: Quero entender tudo sobre arquitetura

1. Ler [ARCHITECTURE.md](ARCHITECTURE.md) (completo)
2. Ler [SDD.md](SDD.md) (detalhes)
3. Explorar código em `tools/`, `auth.py`, `server.py`

**Total: 2-3 horas** 🏗️

---

## 🔍 Procurar por tópico

### Autenticação & Segurança

- Como funciona token? → [ARCHITECTURE.md](ARCHITECTURE.md) § Fluxo de autenticação
- Como setup Service Principal? → [README.md](README.md) § Configuração Azure AD
- Versioning secrets? → [CONTRIBUTING.md](CONTRIBUTING.md) § Workflow de desenvolvimento

### Integrações

- Usar no Claude Code? → [README.md](README.md) § Claude Code (Recommended)
- Usar no GitHub Copilot? → [README.md](README.md) § GitHub Copilot / Cursor
- Usar no Gemini? → [README.md](README.md) § Google Gemini (via MCP Bridge)

### Tools

- Qual tool para criar workspace? → `workspaces.py` / [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md) § Workspaces
- Qual tool para ler arquivo Parquet? → `onelake.py` / [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md) § OneLake
- Qual tool para executar SQL? → `warehouses.py` ou `lakehouses.py` / [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md)

### Troubleshooting

- Erro de autenticação? → [README.md](README.md) § Troubleshooting rápido
- MCP não conecta? → [README.md](README.md) § Verificação e Troubleshooting
- ODBC error? → [README.md](README.md) § Erro: ODBC Driver 18 not found

### Estrutura de código

- Onde estão os handlers? → `tools/*.py` (cada arquivo tem `HANDLERS`)
- Como é feito erro handling? → [ARCHITECTURE.md](ARCHITECTURE.md) § Tratamento de erros
- Como adicionar ferramenta? → [ARCHITECTURE.md](ARCHITECTURE.md) § Adding a New Tool

---

## 📊 Estatísticas de documentação

| Documento | Linhas | Tópicos | Onde vive |
|-----------|--------|---------|-----------|
| README.md | ~800 | Guia completo | Raiz |
| QUICK_START.md | ~150 | 5 min setup | Raiz |
| ARCHITECTURE.md | ~400 | Design + código | Raiz |
| TOOLS_SUMMARY.md | ~400 | Referência de tools | Raiz |
| CONTRIBUTING.md | ~300 | Como contribuir | Raiz |
| SDD.md | ~1000 | Design completo | Raiz |
| skill files | ~200 cada | Domain guides | skills/ |
| agent files | ~150 cada | Agentes | agents/ |

**Total: 4500+ linhas de documentação** 📖

---

## 🎓 Aprenda ontem ordem recomendada

1. ⏱️ [QUICK_START.md](QUICK_START.md) — Colocar funcionando rapidinho
2. 📖 [README.md](README.md) — Entender o projeto como um todo
3. 🛠️ [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md) — Conhecer ferramentas disponíveis
4. 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) — Entender design interno
5. 💻 [CONTRIBUTING.md](CONTRIBUTING.md) — Se quer contribuir

**Tempo total**: ~2-4 horas para expertise completo

---

## ❓ FAQ

**P: Por onde começo?**  
R: [QUICK_START.md](QUICK_START.md) se tem pressa, ou [README.md](README.md) se quer entender antes.

**P: Como sei qual tool usar?**  
R: [TOOLS_SUMMARY.md](TOOLS_SUMMARY.md) tem tabela com exemplos para cada tool.

**P: Posso rodar em [meu OS]?**  
R: Windows, macOS, Linux all suportados. Ver requirements em [README.md](README.md).

**P: Posso usar com [meu IDE]?**  
R: Claude Code (recommended), Copilot, Cursor, Gemini (via bridge). Ver [README.md](README.md) § Integrações.

**P: Posso adicionar minha própria tool?**  
R: Sim! [ARCHITECTURE.md](ARCHITECTURE.md) § Adding a New Tool tem tutorial.

**P: Preciso estar conectado à empresa?**  
R: Sim, precisa de Service Principal válido + acesso ao Fabric no tenant.

---

## 🆘 Apoio & Comunidade

- **🐛 Encontrou bug?** → Abrir [GitHub Issue](https://github.com/seu-usuario/mcp_fabric/issues)
- **💡 Sugestão?** → [GitHub Discussions](https://github.com/seu-usuario/mcp_fabric/discussions)
- **🗺️ Roadmap?** → [ROADMAP.md](ROADMAP.md)
- **🤝 Quer contribuir?** → [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Pronto para explorar? Escolha um documento acima e comece! 🚀**
