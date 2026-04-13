# 🚀 Quick Start — fabric-mcp em 5 minutos

> Guia rápido para colocar fabric-mcp funcionando **agora mesmo**.  
> Para detalhes completos, ver [README.md](README.md).

---

## ⏱️ Timeline

- **~2 min**: Criar Service Principal no Azure
- **~1 min**: Clone + venv + pip install
- **~1 min**: Configurar `.env` + testar
- **~1 min**: Registrar MCP no Claude

---

## 1️⃣ Azure AD — Service Principal (2 min)

### No Azure Portal ([portal.azure.com](https://portal.azure.com))

1. **App Registrations → + New registration**
   - Name: `fabric-mcp-sp`
   - Click **Register**

2. **Copiar e guardar:**
   ```
   - Application (client) ID
   - Directory (tenant) ID
   ```

3. **Certificates & secrets → + New client secret**
   - Add
   - **Copiar o valor** (não consegue depois!)

4. **API Permissions → + Add a permission**
   - Microsoft Fabric → Application permissions
   - ☑️ `Workspace.ReadWrite.All`
   - ☑️ `Item.ReadWrite.All`
   - Add permissions

   - Power BI Service → Application permissions
   - ☑️ `Dataset.ReadWrite.All`
   - ☑️ `Report.ReadWrite.All`
   - Add permissions

5. **Grant admin consent** (botão no topo)
   - Confirmar: "Grant admin consent for MY_TENANT"

6. **[Fabric Admin Portal](https://fabric.microsoft.com) → Tenant settings**
   - ☑️ Service principals can use Fabric APIs
   - ☑️ Allow service principals to use Power BI APIs

---

## 2️⃣ Setup Local (2 min)

### Terminal (PowerShell / bash)

```powershell
# Clonar
git clone https://github.com/seu-usuario/mcp_fabric.git
cd mcp_fabric

# Python venv
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # macOS/Linux

# Instalar dependências
pip install -r requirements.txt

# Criar .env
copy .env.example .env   # Windows
# cp .env.example .env     # macOS/Linux
```

### Editar `.env`

Abrir `.env` e preencher com os valores do Step 1:

```env
FABRIC_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
FABRIC_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
FABRIC_CLIENT_SECRET=seu_client_secret_aqui
```

### Testar

```bash
python -c "from config import settings; print(f'✅ Config OK: Tenant {settings.tenant_id[:8]}...')"
```

---

## 3️⃣ Registrar no Claude (1 min)

### No terminal (venv ativo)

```bash
# Instalar Claude CLI
npm install -g @anthropic-ai/claude-cli

# Registrar MCP
claude mcp add fabric -- /CAMINHO/COMPLETO/.venv/Scripts/python.exe server.py
# macOS/Linux: claude mcp add fabric -- /CAMINHO/COMPLETO/.venv/bin/python server.py

# Verificar
claude mcp list
# Deve aparecer: fabric: ... ✓ Connected
```

⚠️ **Dica**: Usar `pwd` + `which python` para ter o caminho completo certo.

---

## 4️⃣ Primeiro Test (1 min)

### No Claude Code

```bash
claude code
```

Digitar no chat:

```
Liste todos os workspaces do Fabric
```

✅ Se funcionar, você verá a lista de workspaces!

❌ Se der erro, ver [Troubleshooting rápido](#troubleshooting-rápido).

---

## 📚 Próximos passos

| Quer fazer... | Leia... |
|------|---------|
| Documentar um workspace | [README § Exemplo 1](README.md#exemplo-1-documentar-um-workspace-inteiro) |
| Criar pipeline ETL | [README § Exemplo 2](README.md#exemplo-2-criar-pipeline-etl) |
| Executar query SQL | [README § Exemplo 3](README.md#exemplo-3-executar-query-sql-exploratória) |
| Usar no GitHub Copilot | [README § GitHub Copilot](README.md#github-copilot--cursor) |
| Entender arquitetura | [SDD.md](SDD.md) |

---

## 🐛 Troubleshooting rápido

### "Application not found in directory"
- ❌ Client ID errado ou não existe
- ✅ Verificar Application ID no Azure Portal

### "Invalid client secret provided"
- ❌ Secret expirou ou foi copiado errado
- ✅ Gerar novo secret em Certificates & Secrets

### "fabric: × Failed to connect"
- ❌ Servidor não rodando
- ✅ Rodar `python server.py` em outro terminal

### "Unauthorized (403)"
- ❌ SP não tem permissão no workspace
- ✅ Adicionar SP como `Member` no workspace (via Fabric)

### "ODBC Driver 18 not found" (ao usar Warehouse)
- ✅ Windows: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- ✅ macOS: `brew install microsoft-odbc-driver`
- ✅ Linux: Ver [docs](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)

---

## 💡 Dicas

- **Primeira vez?** Começar com prompts simples:
  ```
  Liste os workspaces
  Liste os lakehouses do workspace [ID]
  ```

- **Debug**: Ativar logs detalhados:
  ```env
  LOG_LEVEL=DEBUG
  ```

- **Segurança**: Nunca committar `.env`
  ```bash
  echo ".env" >> .gitignore
  git rm --cached .env  # se já foi commitado
  ```

- **Copilot**: Usar prefixo @fabric:
  ```
  @fabric Liste os workspaces
  ```

---

**Pronto? Boa sorte! 🎉**

Qualquer dúvida → abrir [issue no GitHub](https://github.com/seu-usuario/mcp_fabric/issues) ou ler [README.md](README.md) completo.
