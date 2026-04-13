# fabric-mcp

Servidor MCP (Model Context Protocol) local em Python para o Microsoft Fabric.

Permite executar qualquer ação no Fabric — criar workspaces, lakehouses, notebooks, pipelines, semantic models, relatórios — diretamente pelo terminal do Claude Code, sem abrir o portal.

Autenticação via **Service Principal** (sem login interativo).

---

## Pré-requisitos

- Python 3.11+
- ODBC Driver 18 for SQL Server ([download](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))
- Claude Code CLI instalado
- Acesso de **Global Admin** ou **Fabric Admin** no tenant Azure AD

---

## Instalação

```powershell
cd mcp_fabric
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

---

## Permissões necessárias no Service Principal

### Azure AD — API Permissions (Application)

| API | Permissão | Finalidade |
|-----|-----------|-----------|
| Microsoft Fabric | `Workspace.ReadWrite.All` | Workspaces |
| Microsoft Fabric | `Item.ReadWrite.All` | Notebooks, lakehouses, warehouses, pipelines, spark jobs |
| Power BI Service | `Dataset.ReadWrite.All` | Semantic models, refresh, DAX |
| Power BI Service | `Report.ReadWrite.All` | Reports |

> Admin consent obrigatório após adicionar todas as permissões.

### Fabric Admin Portal — Tenant Settings

| Setting | Valor |
|---------|-------|
| Service principals can use Fabric APIs | Habilitado |
| Allow service principals to use Power BI APIs | Habilitado |

### Workspace Role

O SP precisa de role **Member** em cada workspace que o MCP vai operar.

> Role `Member` permite CRUD completo de itens. O acesso ao OneLake é herdado automaticamente desse role — não requer configuração adicional.

---

## Configuração do .env

```powershell
copy .env.example .env
```

Preencher `.env`:
```env
FABRIC_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
FABRIC_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
FABRIC_CLIENT_SECRET=seu_client_secret
FABRIC_DEFAULT_WORKSPACE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Registrar no Claude Code

```powershell
claude mcp add fabric -- .venv\Scripts\python.exe server.py
claude mcp list
# fabric: python server.py (stdio) - ✓ Connected
```

---

## Verificar instalação

Com o MCP conectado, no Claude Code:

```
Liste os workspaces do Fabric
```

Deve retornar a lista de workspaces disponíveis para o SP.

---

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `AuthError: Falha ao obter token` | Credenciais inválidas no `.env` | Verificar `FABRIC_CLIENT_ID`, `FABRIC_CLIENT_SECRET` e `FABRIC_TENANT_ID` |
| `403 Forbidden` em qualquer chamada | Admin consent não concedido | Azure AD → API permissions → Grant admin consent |
| `401` na API do Fabric | Tenant Settings não habilitado | Habilitar as 2 settings no Admin Portal do Fabric |
| `403` em workspace específico | SP sem role no workspace | Adicionar role `Member` no workspace |
| `execute_sql` falha com timeout | ODBC Driver 18 não instalado | Instalar o driver e reiniciar o terminal |
| `upload_file` retorna 403 | SP sem role no workspace do lakehouse | Verificar role do SP no workspace correto |

---

## Arquitetura

```
Claude Code (terminal)
    │ stdin/stdout (MCP protocol)
    ▼
server.py (MCP Server)
    ├── auth.py        → Token via MSAL (Service Principal, auto-refresh)
    ├── client.py      → HTTP client com retry e mapeamento de erros
    ├── config.py      → Variáveis de ambiente
    └── tools/
        ├── workspaces.py      → 8 tools
        ├── lakehouses.py      → 7 tools
        ├── warehouses.py      → 5 tools  (inclui execute_sql via ODBC)
        ├── notebooks.py       → 8 tools
        ├── pipelines.py       → 6 tools
        ├── spark_jobs.py      → 5 tools
        ├── semantic_models.py → 10 tools (inclui execute_dax)
        ├── reports.py         → 8 tools
        └── onelake.py         → 6 tools  (ADLS Gen2)
```

**Total: 63 tools MCP** cobrindo o ciclo completo do Fabric.

---

**Author:** Luciano Borba / PowerTuning
**Version:** 1.0.0
**Data:** 2026-04-09
