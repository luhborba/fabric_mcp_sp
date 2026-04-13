# 🖥️ Guia de Instalação por Plataforma

> Instruções passo-a-passo para instalar fabric-mcp em Windows, macOS e Linux.

---

## 📋 Resumo

| Passo | Windows | macOS | Linux |
|------|---------|-------|-------|
| 1. Python | ✅ Nativo | ✅ Homo/brew | ✅ apt/yum |
| 2. ODBC Driver | ⏱️ Installer | ⏱️ brew | ⏱️ apt |
| 3. Clone repo | ✅ Git | ✅ Git | ✅ Git |
| 4. venv | `py -m venv` | `python3 -m venv` | `python3 -m venv` |
| 5. Ativar venv | `.venv\Sc\activate` | `source .venv/bin/activate` | `source .venv/bin/activate` |
| 6. pip install | ✅ Padrão | ✅ Padrão | ✅ Padrão |
| 7. .env | Copiar arquivo | Copiar arquivo | Copiar arquivo |
| 8. Claude MCP | `claude mcp add` | `claude mcp add` | `claude mcp add` |

---

## 🪟 Windows 10/11

### 1. Instalar Python 3.11+

```bash
# Opção A: Download direto
# Ir em https://www.python.org/downloads/
# Clicar "Download Python 3.x.x"
# Instalar + marcar "Add Python to PATH"

# Opção B: Usando Chocolatey (se tiver)
choco install python
```

Verificar:
```powershell
python --version
# Output: Python 3.11.x ou superior
```

### 2. Instalar ODBC Driver 18 for SQL Server

```powershell
# Ir em:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
# 
# Clicar no download para Windows
# Executar installer (.msi)
# Seguir wizard (Next, Next, Finish...)

# Ou via Chocolatey:
choco install odbc-driver-17-for-sql-server  # ou driver 18

# Verificar
odbcdiag -l
# Deve listar "ODBC Driver 18 for SQL Server"
```

### 3. Git & Clone

```powershell
# Se não tiver git:
choco install git
# ou: https://git-scm.com/download/win

# Clone
git clone https://github.com/seu-usuario/mcp_fabric.git
cd mcp_fabric
```

### 4. Virtual Environment

```powershell
# Criar
python -m venv .venv

# Ativar
.venv\Scripts\activate
# (prompt deve mostrar: (.venv) PS>)
```

### 5. Instalar Dependências

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configurar .env

```powershell
# Copiar template
copy .env.example .env

# Editar .env (abrir em notepad / VS Code)
notepad .env
# Preencher:
# - FABRIC_TENANT_ID
# - FABRIC_CLIENT_ID
# - FABRIC_CLIENT_SECRET
```

### 7. Testar

```powershell
# Ainda com venv ativo
python -c "from config import settings; print(f'✅ Tenant: {settings.tenant_id[:8]}...')"
```

### 8. Registrar no Claude

```powershell
# Encontrar caminho completo do Python
$python_path = (Get-Command .venv\Scripts\python).Source
Write-Host "Python path: $python_path"
# Copiar o path completo (ex: C:\Users\user\mcp_fabric\.venv\Scripts\python.exe)

npm install -g @anthropic-ai/claude-cli

claude mcp add fabric -- C:\Users\user\mcp_fabric\.venv\Scripts\python.exe server.py
# substituir C:\Users\user\ pelo seu caminho real

# Verificar
claude mcp list
# Deve aparecer: fabric: ... ✓ Connected
```

---

## 🍎 macOS (Intel & Apple Silicon)

### 1. Instalar Python 3.11+

```bash
# Opção A: Homebrew (recomendado)
brew install python@3.11
python3.11 --version

# Opção B: Download direto
# https://www.python.org/downloads/macos/
# Clicar "macOS Installer (Intel)" ou "ARM64"
# Executar .pkg
```

### 2. Instalar ODBC Driver 18 for SQL Server

```bash
# Via Homebrew
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install microsoft-odbc-driver

# Ou: Download direto
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
# Clicar "macOS"
# Executar .pkg

# Verificar
which isql
# Ou tentar:
python -c "import pyodbc; print(pyodbc.drivers())"
```

### 3. Git & Clone

```bash
# Git já vem em macOS normalmente
git clone https://github.com/seu-usuario/mcp_fabric.git
cd mcp_fabric
```

### 4. Virtual Environment

```bash
# Intel Mac
python3.11 -m venv .venv

# Apple Silicon (M1/M2/M3)
python3 -m venv .venv

# Ativar
source .venv/bin/activate
# (prompt deve mostrar: (.venv) $)
```

### 5. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt

# Se houver erro com pyodbc em Apple Silicon:
# pip install --no-binary :all: pyodbc
```

### 6. Configurar .env

```bash
# Copiar
cp .env.example .env

# Editar
nano .env
# ou: open -t .env   (abrir em TextEdit)
# Preencher variáveis obrigatórias
```

### 7. Testar

```bash
python -c "from config import settings; print(f'✅ Tenant: {settings.tenant_id[:8]}...')"
```

### 8. Instalar Node.js + Claude CLI

```bash
# Se não tem Node
brew install node

npm install -g @anthropic-ai/claude-cli
claude --version
```

### 9. Registrar no Claude

```bash
# Encontrar path do python venv
python_path=$(which python)  # dentro de venv ativo
echo $python_path
# Output exemplo: /Users/user/mcp_fabric/.venv/bin/python

# Copiar o path + registrar
claude mcp add fabric -- /Users/user/mcp_fabric/.venv/bin/python server.py

# Verificar
claude mcp list
```

---

## 🐧 Linux (Ubuntu / Debian / RHEL / CentOS)

### 1. Instalar Python 3.11+

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# RHEL / CentOS
sudo yum install python3.11 python3.11-devel

# Verificar
python3.11 --version
```

### 2. Instalar ODBC Driver 18 for SQL Server

#### Ubuntu / Debian

```bash
# Adicionar Microsoft PPA
sudo curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | \
  sudo tee /etc/apt/sources.list.d/mssql-release.list

# Instalador
sudo apt update
sudo ACCEPT_EULA=Y apt install msodbcsql18

# Verificar
dpkg -l | grep msodbcsql18
```

#### RHEL / CentOS

```bash
sudo curl https://packages.microsoft.com/config/rhel/8/prod.repo | \
  sudo tee /etc/yum.repos.d/mssql-release.repo

sudo ACCEPT_EULA=Y yum install msodbcsql18

# Verificar
rpm -qa | grep msodbcsql18
```

### 3. Git & Clone

```bash
# Git já deve estar instalado
git clone https://github.com/seu-usuario/mcp_fabric.git
cd mcp_fabric
```

### 4. Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
# (prompt deve mostrar: (.venv) $)
```

### 5. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt

# Se houver erro com pyodbc:
# sudo apt install unixodbc unixodbc-dev
# pip install --no-binary :all: pyodbc
```

### 6. Configurar .env

```bash
cp .env.example .env
nano .env
# Preencher variáveis
```

### 7. Testar

```bash
python -c "from config import settings; print(f'✅ Tenant: {settings.tenant_id[:8]}...')"
```

### 8. Instalar Node.js + Claude CLI

```bash
# Node via NodeSource (recomendado)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs

# ou via apt (pode ser versão antiga)
sudo apt install nodejs npm

npm install -g @anthropic-ai/claude-cli
claude --version
```

### 9. Registrar no Claude

```bash
# Encontrar python path
python_path=$(which python)  # dentro de venv ativo
echo $python_path
# Output: /home/user/mcp_fabric/.venv/bin/python

# Registrar
claude mcp add fabric -- /home/user/mcp_fabric/.venv/bin/python server.py

# Verificar
claude mcp list
```

---

## �️ Cursor (Windows, macOS, Linux)

> Cursor é um IDE baseado em VS Code com suporte nativo a MCP

### Passos

1. **Instalar Cursor**: https://www.cursor.com/
   ```bash
   # macOS
   brew install cursor
   
   # Windows
   # Download em https://www.cursor.com/
   
   # Linux
   # Download AppImage em https://www.cursor.com/
   ```

2. **Completar setup fabric-mcp** (Python, ODBC, clone, venv, .env)
   - Seguir seções Windows/macOS/Linux acima (passos 1-7)

3. **Configurar MCP no Cursor**
   - Abrir Cursor
   - Ir em: **Settings** → **Extensions** ou **Command Palette** (Ctrl+Shift+P)
   - Procurar por MCP Server
   - Adicionar servidor MCP

   **Opção A: Via settings.json**
   ```bash
   # macOS/Linux: ~/.cursor/settings.json
   # Windows: %APPDATA%\Cursor\User\settings.json
   
   {
     "codeium_command_completions_alternative_completions_base_url": ...,
     "mcp.servers": {
       "fabric": {
         "command": "C:\\Users\\user\\mcp_fabric\\.venv\\Scripts\\python.exe",
         "args": ["server.py"],
         "cwd": "C:\\Users\\user\\mcp_fabric"
       }
     }
   }
   ```

   **Opção B: Via UI**
   - Ir em Settings → MCP Servers
   - Clicar "Add New"
   - Nome: `fabric`
   - Tipo: `StdIO`
   - Comando: `/path/to/.venv/bin/python server.py`
   - Diretório: `/path/to/mcp_fabric`

4. **Testar**
   - Abrir nova conversa no Cursor
   - Digitar: "Liste os workspaces do Fabric"
   - Se funcionar ✅ — MCP está conectado!

---

## 💼 GitHub Copilot (VS Code, Visual Studio, JetBrains)

> GitHub Copilot suporta MCP via extensão `Copilot Chat` + configuração

### Setup via VS Code (recomendado)

1. **Instalar extensões**
   ```bash
   # Via VS Code Marketplace ou CLI
   code --install-extension GitHub.copilot
   code --install-extension GitHub.copilot-chat
   ```

2. **Completar setup fabric-mcp** (Python, ODBC, clone, venv, .env)
   - Seguir seções Windows/macOS/Linux acima (passos 1-7)

3. **Configurar MCP no VS Code**
   - Abrir VS Code
   - Ir em **Settings** (Ctrl+,) → JSON
   - Añadir configuração MCP:

   ```json
   {
     "copilotChat.mcp.servers": {
       "fabric": {
         "command": "C:\\Users\\user\\mcp_fabric\\.venv\\Scripts\\python.exe",
         "args": ["server.py"],
         "cwd": "C:\\Users\\user\\mcp_fabric"
       }
     }
   }
   ```

   **Substituir paths para sua máquina:**
   ```powershell
   # Windows - encontrar caminho:
   (Get-Command .venv\Scripts\python).Source
   # Output: C:\Users\user\mcp_fabric\.venv\Scripts\python.exe
   ```

4. **Testar**
   - Abrir Copilot Chat (Ctrl+Shift+L)
   - Digitar: "Liste os workspaces do Fabric"
   - Se funcionar ✅ — MCP está conectado!

### Setup via Visual Studio 2022+

1. **Instalar Copilot**
   - Extensions → Manage Extensions
   - Procurar por "GitHub Copilot"
   - Instalar

2. **Configurar MCP**
   - Tools → Options → GitHub Copilot → MCP Servers
   - Adicionar novo servidor
   - Nome: `fabric`
   - Comando: `python.exe` (caminho completo)
   - Args: `server.py`

3. **Testar** igual ao VS Code

### Setup via JetBrains (IntelliJ, PyCharm, WebStorm)

1. **Instalar Copilot**
   - Settings → Plugins
   - Procurar "GitHub Copilot"
   - Instalar + Restart

2. **Configurar MCP**
   - Settings → Tools → GitHub Copilot → MCP Servers
   - Adicionar servidor com mesmos dados acima

---

## 🚀 Gemini (Antigravity) via MCP Bridge

> Gemini não suporta MCP nativamente ainda, mas pode usar via ponte (bridge)

### Opção 1: Google AI Studio (experimental)

1. **Ir em**: https://aistudio.google.com/app/
2. **Criar notebook Python**
3. **Adicionar bridge MCP**:

   ```python
   # Na célula do Gemini
   import subprocess
   import json
   
   # Iniciar servidor MCP
   proc = subprocess.Popen(
       ["python", "/path/to/mcp_fabric/server.py"],
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE,
       cwd="/path/to/mcp_fabric"
   )
   
   # Conectar ao Gemini via API
   import google.generativeai as genai
   
   genai.configure(api_key="YOUR_API_KEY")
   
   # Usar tools do fabric-mcp
   # (Documentação Gemini MCP integration: 
   #  https://ai.google.dev/gemini-api/docs/mcp)
   ```

### Opção 2: Cursor como proxy (recomendado)

> Usar Cursor como intermediário entre Gemini e fabric-mcp

1. Configurar Cursor com MCP (ver seção Cursor acima)
2. No Gemini, usar API do Cursor para acessar ferramentas
3. Pipe de dados: **Gemini → Cursor API → fabric-mcp → Fabric**

   ```python
   import requests
   
   # Chamar Cursor API (via localhost se rodando localmente)
   response = requests.post(
       "http://localhost:3000/mcp/call",
       json={
           "server": "fabric",
           "tool": "list_workspaces",
           "args": {}
       }
   )
   
   print(response.json())
   ```

### Opção 3: Notebook local com bridge Python

> Script que faz bridge entre Gemini API + fabric-mcp

```python
# bridge.py
import json
import subprocess
import socket

class GeminiFabricBridge:
    def __init__(self, mcp_path: str, gemini_api_key: str):
        self.mcp_proc = subprocess.Popen(
            ["python", f"{mcp_path}/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            cwd=mcp_path
        )
        self.gemini_key = gemini_api_key
    
    def list_tools(self):
        """Lista ferramentas disponíveis no fabric-mcp"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }
        self.mcp_proc.stdin.write(json.dumps(request).encode() + b"\n")
        self.mcp_proc.stdin.flush()
        response = self.mcp_proc.stdout.readline().decode()
        return json.loads(response)
    
    def call_tool(self, tool_name: str, args: dict):
        """Chama ferramenta específica"""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        self.mcp_proc.stdin.write(json.dumps(request).encode() + b"\n")
        self.mcp_proc.stdin.flush()
        response = self.mcp_proc.stdout.readline().decode()
        return json.loads(response)

# Usar:
bridge = GeminiFabricBridge(
    mcp_path="/path/to/mcp_fabric",
    gemini_api_key="YOUR_API_KEY"
)
tools = bridge.list_tools()
result = bridge.call_tool("list_workspaces", {})
print(result)
```

**Usar no Gemini**:
```python
# No notebook Gemini
exec(open('bridge.py').read())
workspaces = bridge.call_tool("list_workspaces", {})
print(f"Workspaces: {workspaces}")
```

---

## 📊 Comparação: Claude vs Cursor vs Copilot vs Gemini

| Aspecto | Claude | Cursor | Copilot | Gemini |
|---------|--------|--------|---------|--------|
| MCP Nativo | ✅ Sim | ✅ Sim | ✅ Sim | ❌ Não (bridge) |
| Setup | Easy | Easy | Médio | Complexo |
| Performance | Rápido | Rápido | Rápido | Depende bridge |
| IDE Support | Browser | Standalone | VS/Studio/JB | Google Studios |
| Recomendado | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## �🔧 Troubleshooting de Instalação

### Windows

| Erro | Solução |
|------|---------|
| `python not found` | Adicionar Python ao PATH: Settings → Environment Variables → Path → adicionar `C:\Python311` |
| `ODBC Driver 18 not found` | Reinstalar ODBC driver de https://learn.microsoft.com/en-us/sql/connect/odbc |
| `pip permission denied` | Rodar PS como Admin ou usar `py -m pip` |
| `.venv\Scripts\activate failing` | Executar PowerShell como Admin |

### macOS

| Erro | Solução |
|------|---------|
| `pyodbc import error (Apple Silicon)` | `pip install --no-binary :all: pyodbc` |
| `ODBC driver not found` | `brew install microsoft-odbc-driver` |
| `python3 not found` | `brew install python@3.11` |
| `zsh: command not found: brew` | Instalar Homebrew: `/bin/bash -c "$(curl ...)` |

### Linux

| Erro | Solução |
|------|---------|
| `python3.11 not found (Ubuntu)` | `sudo apt install python3.11` |
| `ODBC driver not found` | Ver seção 2 acima (adicionar PPA + install) |
| `unixodbc not installed` | `sudo apt install unixodbc unixodbc-dev` |
| `pip permission denied` | Adicionar `--user` ou usar venv (recomendado) |

---

## ✅ Verificação pós-instalação

Após seguir passos acima, rodar:

```bash
# 1. Check Python
python --version
# Output: Python 3.11.x ou superior

# 2. Check venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
which python  # ou where python (Windows)
# Output deve ter .venv no path

# 3. Check dependências
pip list | grep mcp
# Output: mcp 1.0.0 (ou superior)

# 4. Check ODBC (se usar Warehouse)
python -c "import pyodbc; print(pyodbc.drivers())"
# Output deve listar "ODBC Driver 18 for SQL Server"

# 5. Check config
python -c "from config import settings; print('✅ Config OK')"
# Se der erro de variáveis, .env não está configurado

# 6. Check Claude CLI
claude --version
# Output: claude cli version ...

# 7. Check MCP registration
claude mcp list
# Output deve incluir: fabric: ... ✓ Connected
```

---

## 🚀 Primeiro teste

```bash
# Terminal 1: Rodar server MCP
python server.py
# Output deve mostrar: MCP Server iniciado

# Terminal 2: Testar com Claude
claude code

# No editor Claude, digitar:
"Liste os workspaces do Fabric"

# Se funcionar: ✅ Tudo OK!
# Se não: Ver README.md § Troubleshooting
```

---

## 📖 Próximas etapas

1. ✅ Instalação completa? → [QUICK_START.md](QUICK_START.md)
2. Quer usar? → [README.md](README.md) § Integrações
3. Quer entender? → [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Sucesso na instalação! Alguma dúvida, abra [issue no GitHub](https://github.com/seu-usuario/mcp_fabric/issues).** 🎉
