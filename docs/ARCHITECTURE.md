# 🏗️ Arquitetura — fabric-mcp v1.0

> Guia técnico da arquitetura de fabric-mcp: como funciona, onde estão as coisas, como estender.

---

## 📐 Fluxo de uma requisição

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. Claude Code                                                               │
│    User: "Liste os workspaces do Fabric"                                     │
│    Claude MCP Protocol: invoke_tool(name="list_workspaces", args={})          │
└─────────────────────────┬──────────────────────────────────────────────────────┘
                          │ stdin (MCP protocol)
                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 2. server.py (MCP Server)                                                    │
│    @app.call_tool()                                                          │
│    async def call_tool(name: str, arguments: dict):                          │
│      handler = TOOL_HANDLERS.get("list_workspaces")                          │
│      result = await handler(arguments)  ◄──── Chamar handler                  │
│      return result (JSON)                                                    │
└─────────────────────────┬──────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 3. tools/workspaces.py                                                       │
│    async def list_workspaces(args):                                          │
│      token = await token_manager.get_token()  ◄──── Get token (with cache)   │
│      async with httpx.AsyncClient() as client:                              │
│        r = await client.get(                                                │
│          "https://api.fabric.microsoft.com/v1/workspaces",                  │
│          headers={"Authorization": f"Bearer {token}"}                       │
│        )                                                                     │
│        return parse_response(r)  ◄──── Mapear erros, validar                │
└─────────────────────────┬──────────────────────────────────────────────────────┘
                          │ HTTP REST API call
                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 4. Azure AD (MSAL)                                                           │
│    OAuth2 client_credentials flow                                           │
│    Token cache + refresh automático                                        │
└─────────────────────────┬──────────────────────────────────────────────────────┘
                          │ ← Bearer token (3600s TTL)
                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 5. Microsoft Fabric REST API                                                │
│    GET /v1/workspaces                                                       │
│    Response: { "value": [ { id, displayName, ... } ] }                     │
└─────────────────────────┬──────────────────────────────────────────────────────┘
                          │ ← JSON response
                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 6. tools/workspaces.py (resposta)                                           │
│    Validar, parse, mapear a Pydantic model                                  │
│    return {"success": True, "data": [...]}                                  │
└─────────────────────────┬──────────────────────────────────────────────────────┘
                          │ stdout (MCP protocol)
                          ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 7. Claude Code                                                               │
│    Recebe resultado estruturado JSON                                        │
│    Claude exibe ao usuário: "Você tem 3 workspaces: ..."                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Estrutura de arquivos

### Core

```
mcp_fabric/
├── server.py       # MCP Server entry point
├── auth.py         # TokenManager (MSAL + cache)
├── config.py       # Settings (carrega .env, valida vars)
├── client.py       # httpx AsyncClient com retry + error mapping
└── exceptions.py   # FabricAPIError, AuthError, NotFoundError, etc.
```

**Responsabilidades**:

| Arquivo | O quê | Quem chamar |
|---------|-------|-----------|
| `server.py` | Inicializa MCP, registra tools, trata tool calls | `tools/*.py` |
| `auth.py` | Obter token OAuth2 (cache + refresh automático) | Qualquer tool que quer fazer request |
| `config.py` | Carregar e validar `.env` | `server.py`, `auth.py` |
| `client.py` | HTTP client com retry, timeout, error mapping | Cada tool que chama Fabric API |
| `exceptions.py` | Exceções customizadas com suggestions úteis | Qualquer um que quer reportar erro |

### Tools (domínios)

```
tools/
├── workspaces.py       # 8 tools: list, get, create, delete, update, role-assignments
├── lakehouses.py       # 7 tools: list, create, get files, write files, execute SQL
├── warehouses.py       # 5 tools: list, create, get connection, execute SQL
├── notebooks.py        # 8 tools: list, create, get definition, update, execute
├── pipelines.py        # 6 tools: list, create, run, get status, monitor
├── spark_jobs.py       # 6 tools: list, create, run, get status
├── semantic_models.py  # 6 tools: list, create, refresh, DAX queries, explore schema
├── reports.py          # 5 tools: list, create, share, export
├── onelake.py          # 7 tools: list files, upload, download, copy, delete
└── __init__.py         # Importar todos os TOOLS + HANDLERS
```

**Pattern em cada arquivo**:

```python
# tools/workspaces.py

TOOLS: list[Tool] = [
    Tool(
        name="list_workspaces",
        description="Listar todos os workspaces do tenant",
        inputSchema={
            "type": "object",
            "properties": {
                "capacity_id": {"type": "string", "description": "(opcional)"}
            },
            "required": []
        }
    ),
    # ... mais tools
]

HANDLERS: dict[str, Callable] = {
    "list_workspaces": handle_list_workspaces,
    # ... mais handlers
}

async def handle_list_workspaces(args: dict) -> dict:
    """Implementação da tool."""
    try:
        token = await token_manager.get_token()
        # fazer chamada API
        # mapear resultado
        return {"success": True, "data": []}
    except Exception as e:
        return {"success": False, "error": {...}}
```

### Agents (especializ personalizações)

```
agents/
├── FabricAdmin.agent.md      # Administração: workspaces, governança, auditoria
├── FabricAppDev.agent.md     # App development: criar apps, relatórios Power BI
└── FabricDataEngineer.agent.md # ETL/ELT: orquestração Medallion, pipelines
```

**O que cada agente faz:**
- Define `name`, `description`, `delegates_to` (skills para delegar)
- Instruções de personalidade e workflow

### Skills (guias temáticos)

```
skills/
├── workspace-management/SKILL.md    # Como gerenciar workspaces
├── spark-authoring/SKILL.md         # Como criar notebooks + Spark jobs
├── spark-consumption/SKILL.md       # Como explorar dados em notebooks
├── sqldw-authoring/SKILL.md         # Como criar/atualizar tabelas SQL
├── sqldw-consumption/SKILL.md       # Como executar queries SQL
├── powerbi-authoring/SKILL.md       # Como criar modelos + relatórios
├── powerbi-consumption/SKILL.md     # Como explorar modelo com DAX
├── e2e-medallion/SKILL.md           # Padrão Medallion completo
└── onelake/SKILL.md                 # Como gerenciar OneLake
```

**O que cada skill faz:**
- Instrui Claude **quando** usar cada tool
- Exemplos de prompts
- Must/Prefer/Avoid rules para cada domínio
- Fluxos de trabalho (workflows)

---

## 🔄 Fluxo de autenticação

### Token Manager

```
┌─ get_token() ──────────────────────────────────────────┐
│                                                        │
│  1. Verificar cache[scope]                            │
│     └─ Token não expirou nos próximos 5 min?         │
│        ├─ Sim → Return cached_token                  │
│        └─ Não → Adquirir novo                        │
│                                                        │
│  2. _acquire(scope)                                   │
│     ├─ Run MSAL async: acquire_token_for_client()    │
│     ├─ Checar resposta                               │
│     │  ├─ Sucesso → Cache + Return token             │
│     │  └─ Erro → Raise AuthError com suggestion      │
│     └─ TTL = expires_in (typically 3600s)            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Por quê esse design?**
- **Cache**: Evita N chamadas ao Azure AD para mesma scope
- **Refresh proativo**: Renova 5 min antes de expirar (não deixa expirar no meio de request)
- **Async lock**: Evita race condition se 2 coroutines pedem token ao mesmo tempo

---

## 🛡️ Tratamento de erros

### Fluxo de erro

```
Tool chama API REST
    ↓
httpx Client recebe response
    ↓
client.py → _handle_response()
    ├─ 2xx → Parse JSON + return
    ├─ 4xx → Raise FabricAPIError (client-side)
    │  ├─ 401 → AuthError ("token expirou?")
    │  ├─ 403 → PermissionError ("role insuficiente?")
    │  ├─ 404 → NotFoundError ("workspace não existe?")
    │  └─ 400 → ValidationError ("parâmetro inválido?")
    └─ 5xx → Retry automático (via tenacity)
        ├─ Retry 3x com backoff exponencial
        └─ Se falhar → ServerError ("Fabric API down?")

Exception → Tool handler captura
    ↓
Tool return {"success": False, "error": {..., "suggestion": "..."}}
    ↓
Claude vê sugestão + tenta corrigir automaticamente
```

**Exceções custom** (em `exceptions.py`):

```python
class FabricMCPError(Exception):
    """Base error com .to_dict() que retorna JSON estruturado."""
    def to_dict(self) -> dict:
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "suggestion": self.suggestion
            }
        }
```

---

## 🔌 Adding a New Tool

Se você quer adicionar uma nova ferramenta, siga esse padrão:

### 1. Determinar domínio

Sua tool é sobre:
- Workspaces? → `tools/workspaces.py`
- Lakehouses? → `tools/lakehouses.py`
- Novo domínio? → Criar `tools/novo_dominio.py`

### 2. Definir Tool schema

```python
# tools/novo_dominio.py

TOOLS: list[Tool] = [
    Tool(
        name="minha_tool",
        description="O que a tool faz",
        inputSchema={
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "..."},
                "param2": {"type": "integer", "description": "..."},
            },
            "required": ["param1"]
        }
    )
]
```

### 3. Implementar handler

```python
async def handle_minha_tool(args: dict) -> dict:
    """Implementação."""
    try:
        param1 = args["param1"]
        param2 = args.get("param2")
        
        token = await token_manager.get_token()
        
        # Chamar Fabric API
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{settings.api_base_url}/meu_endpoint",
                headers={"Authorization": f"Bearer {token}"},
                params={"q": param1}
            )
            r.raise_for_status()
            data = r.json()
        
        return {
            "success": True,
            "data": data
        }
    except FabricAPIError as e:
        return e.to_dict()
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_ERROR",
                "message": str(e)
            }
        }

HANDLERS: dict[str, Callable] = {
    "minha_tool": handle_minha_tool,
}
```

### 4. Registrar em `__init__.py`

```python
# tools/__init__.py
from . import novo_dominio

# Em server.py, imports já existem:
# from tools import novo_dominio
```

---

## 📊 Dados em trânsito

### Exemplo: list_workspaces response

```json
{
  "success": true,
  "data": [
    {
      "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "displayName": "analytics-prod",
      "description": "Production analytics workspace",
      "type": "Workspace",
      "state": "Active",
      "capacityId": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
    },
    {
      "id": "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
      "displayName": "dev-workspace",
      "description": null,
      "type": "Workspace",
      "state": "Active",
      "capacityId": null
    }
  ]
}
```

### Exemplo: error response

```json
{
  "success": false,
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "Você não tem permissão para acessar este workspace",
    "details": "Service principal não está como Member do workspace",
    "suggestion": "Adicione o Service Principal como Member no workspace via Fabric UI"
  }
}
```

---

## 🧪 Testing

### Teste manual de uma tool

```bash
# Terminal com venv ativo
python -c "
import asyncio
from tools.workspaces import handle_list_workspaces

result = asyncio.run(handle_list_workspaces({}))
print(result)
"
```

### Teste do server

```bash
# Terminal 1: Rodar server
python server.py

# Terminal 2: Testar com curl
curl -X POST http://localhost:3000/invoke \
  -H 'Content-Type: application/json' \
  -d '{"tool": "list_workspaces", "args": {}}'
```

---

## 🚀 Performance

### Bottlenecks conhecidos

| Operação | Tempo típico | Como otimizar |
|----------|-------------|--------------|
| get_token (1ª vez) | ~500ms | Cache + async MSAL |
| get_token (cached) | <1ms | LRU cache por scope |
| list_workspaces | ~200ms | REST call serial |
| create_notebook | ~1-2s | Wait for operation async |
| execute_warehouse_query | ~5-30s | Depend on query complexity |

### Boas práticas

- ✅ Usar `asyncio` para parallelizar múltiplas chamadas
- ✅ Cache token agressivamente (5 min antes de expirar)
- ✅ Batch operações de leitura quando possível
- ✅ Usar pagination para listas grandes
- ✅ Nunca fazer polling síncrono (usar async/await)

---

## 📚 Referências

- **MCP Spec**: https://spec.modificationprotocol.org
- **Fabric REST API docs**: https://learn.microsoft.com/en-us/rest/api/fabric
- **MSAL Python**: https://github.com/AzureAD/microsoft-authentication-library-for-python
- **httpx async docs**: https://www.python-httpx.org/async/

---

**Entendeu a arquitetura? Pronto para contribuir!** 🎉
