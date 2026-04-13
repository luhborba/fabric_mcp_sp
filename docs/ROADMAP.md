# 🗺️ Roadmap — fabric-mcp

> Visão de futuro, features planejadas e parcerias para fabric-mcp.

---

## 📌 Versão Atual: v1.0.0

**Status**: Ativo  
**Data**: Abril 2026  
**Suporte**: Community-driven

### O que está em v1.0.0

✅ 65+ tools cobrindo 9 domínios  
✅ Autenticação Service Principal  
✅ 3 agentes especializados  
✅ 9 skills temáticos  
✅ Documentação completa  
✅ Supporte para Claude Code, Copilot, Cursor, Gemini

---

## 🚀 Versão v1.1.0 (Q2 2026)

### Features planejadas

| Feature | Dominios Afetados | Complexidade | Status |
|---------|------------------|----------|--------|
| **Dataflows Gen2** | Pipelines, ETL | 🟠 Médium | ⏳ Planejado |
| **KQL Databases / Eventhouses** | Analytics | 🟠 Médium | ⏳ Planejado |
| **Batch operations** | Todos | 🟢 Fácil | ⏳ Planejado |
| **Caching layer** | Performance | 🟡 Médium-High | ⏳ Planejado |
| **Retry policy tunning** | Robustez | 🟢 Fácil | ⏳ Planejado |
| **Rate limit handling** | Performance | 🟡 Médium | ⏳ Planejado |

### Por quê?

- Dataflows Gen2 é workload importante em ETL/ELT
- KQL é crescente em Analytics
- Batch operations melhoram UX para operações em massa
- Caching reduz latência + custo de API

### Contribuidores buscados

- Especialista em Dataflows Gen2
- Especialista em KQL

---

## 📈 Versão v2.0.0 (Q4 2026)

### Objectives

**Suportar não apenas Fabric, mas todo ecossistema Microsoft Analytics**

| Produto | Tools | Novidade |
|---------|-------|---------|
| **Fabric** | 65+ (atalhos) | Já existe |
| **Power BI** | 15+ | Novo |
| **Analysis Services** | 8+ | Novo |
| **Data Factory** | 10+ | Novo |
| **Synapse** | 12+ | Novo |

### Tarefas

- ✅ Decompor MCP server em módulos
  - `mcp_fabric/` — Fabric-only (migrar)
  - `mcp_microsoft_analytics/` — Wrapper principal
  - `mcp_powerbi/` — Tools Power BI
  - `mcp_aas/` — Tools Analysis Services
  - `mcp_synapse/` — Tools Azure Synapse
  - `mcp_adf/` — Tools Data Factory

- ✅ Shared auth layer (MSAL para todos)
- ✅ Unified config (`.env` suporta todos)
- ✅ Unified error handling

### Benefício

Uma ferramenta para governar todo analytics stack Microsoft

---

## 💻 Infraestrutura

### CI/CD

**Planejado para v1.1.0**:
- ✅ GitHub Actions para lint + test
- ✅ Pre-commit hooks (black, ruff)
- ✅ Automated docs building
- ✅ Release automation

### Deployment

**Planejado para v2.0.0**:
- ☐ Docker image
- ☐ helm charts para Kubernetes
- ☐ Azure Container Instances
- ☐ Disponibilidade global (não apenas stdio local)

### Testes

**v1.1.0+**:
- ☐ pytest suite (unit tests)
- ☐ Integration tests contra Fabric sandbox
- ☐ Performance benchmarks

---

## 📚 Documentação

### Planejado

| Documento | Versão | Contribuidor |
|-----------|--------|--------------|
| **Tutorial: Criar Medallion Architecture** | 1.1.0 | TBD |
| **Best Practices: Governança** | 1.1.0 | TBD |
| **Case Studies: Real deployments** | 1.2.0 | TBD |
| **Video series** | 1.2.0 | TBD |
| **Webinar: architecture deep-dive** | 1.0.5 | Planejado |

---

## 🌐 Comunidade & Parcerias

### Buscamos parceiros para

| Área | Objetivo | Status |
|------|--------|--------|
| **Enterprise adoption** | Ganhar usuários corporativos | 🟡 Em andamento |
| **Microsoft partnership** | Integração oficial? | 🔴 Não iniciado |
| **Community contributions** | PRs, skills, agents | 🟢 Ativo |
| **Consultoria** | Suporte corporativo | 🟡 Interesse demonstrado |

### Como ajudar?

- ⭐ Star no GitHub (mostra support)
- 📝 Contribuir skill temático
- 🐛 Reportar bugs detalhadamente
- 💬 Feedback no Discussions
- 👥 Recrutar em sua empresa

---

## 🎯 Métricas de sucesso (Q4 2026)

| Métrica | Alvo | Atual |
|---------|------|--------|
| GitHub Stars | 500+ | Varia |
| Contributors | 10+ | TBD |
| Monthly downloads | 500+ | TBD |
| Real deployments | 20+ | TBD |
| Enterprise users | 5+ | TBD |

---

## ❓ FAQs sobre roadmap

**P: Quando v1.1.0 sai?**  
R: Tentamos Q2 2026. Contribuições podem acelerar.

**P: Podem adicionar [minha feature]?**  
R: Sim! Abra [GitHub Issue](https://github.com/seu-usuario/mcp_fabric/issues/new) com proposta.

**P: Quando vai suportar [produto Microsoft]?**  
R: v2.0.0 tem plano maior. Para Q4 2026, seja paciente ou contribua!

**P: Posso ajudar com [tarefas]?**  
R: Absolutamente! [CONTRIBUTING.md](CONTRIBUTING.md) tem workflow.

**P: Vão monetizar?**  
R: Não. MIT license para sempre. Enterprise support pode ser eventual escopo.

---

## 📞 Influenciar prioridades

Se você quer influenciar roadmap:

1. 👍 React em de GitHub Issues prioritárias
2. 💬 Comentar em Discussions
3. 🤝 Contribuir código
4. 📊 Usar em production (case study?)

---

## 🏁 Visão de longo prazo (2027+)

**fabric-mcp torna-se**:
- ✅ **Standard de facto** para programação Microsoft Analytics via IA
- ✅ **Parte de Microsoft learning** (docs oficiais)
- ✅ **Toolkit de consultores** (adotado por Big 3)
- ✅ **Base para startups** (Produtos construídos em cima)

---

**Quer contribuir para essa visão? Veja [CONTRIBUTING.md](CONTRIBUTING.md)! 🚀**
