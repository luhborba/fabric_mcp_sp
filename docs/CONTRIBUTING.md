# 🤝 Contribuindo para fabric-mcp

> Obrigado por querer contribuir! Este guia explica como participar do projeto.

---

## 📋 Tipos de contribuição

### 🐛 Reportar bugs

1. Checar [issues existentes](https://github.com/seu-usuario/mcp_fabric/issues) — talvez alguém já reportou
2. Criar nova issue com:
   - **Título claro**: "ODBC Driver 18 not found on macOS ARM64"
   - **Steps to reproduce**: Passos exatos para reproduzir
   - **Expected vs Actual**: O que deveria acontecer vs o que aconteceu
   - **Environment**: Python version, OS, Fabric API version

### 💡 Sugerir features

1. Checar [discussions](https://github.com/seu-usuario/mcp_fabric/discussions)
2. Descrever:
   - **Use case**: Por quê precisa dessa feature?
   - **Proposta**: Como você imagina que funcione?
   - **Alternativas**: Existe forma de fazer agora?

### 📖 Melhorar documentação

Encontrou erro na doc? Typo? Exemplo confuso?
- Editar direto via GitHub (botão "Edit") ou
- Fork + PR

### 💻 Código

Ver seção [Workflow de desenvolvimento](#workflow-de-desenvolvimento).

---

## 🔧 Workflow de desenvolvimento

### 1. Fork + Clone

```bash
git clone https://github.com/SEU_USUARIO/mcp_fabric.git
cd mcp_fabric
git remote add upstream https://github.com/autor-original/mcp_fabric.git
```

### 2. Criar branch

```bash
git checkout -b feature/sua-feature
# ou
git checkout -b fix/seu-bug
# ou
git checkout -b docs/melhoria-doc
```

### 3. Setup local (se primeira vez)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Preencher .env com credenciais de teste
```

### 4. Fazer mudanças

#### Se adicionando **nova tool**

Exemplo: adicionar `delete_workspace(workspace_id)` em `tools/workspaces.py`

```python
# tools/workspaces.py

# 1. Adicionar ao TOOLS
Tool(
    name="delete_workspace",
    description="Deletar um workspace (irreversível)",
    inputSchema={
        "type": "object",
        "properties": {
            "workspace_id": {"type": "string", "description": "ID do workspace"}
        },
        "required": ["workspace_id"]
    }
),

# 2. Adicionar ao HANDLERS
"delete_workspace": handle_delete_workspace,

# 3. Implementar handler
async def handle_delete_workspace(args: dict) -> dict:
    """Deletar workspace."""
    try:
        workspace_id = args["workspace_id"]
        # Validar
        if not workspace_id:
            raise ValidationError("workspace_id é obrigatório")
        
        token = await token_manager.get_token()
        
        # Chamar API
        async with httpx.AsyncClient() as client:
            r = await client.delete(
                f"{settings.api_base_url}/workspaces/{workspace_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
        
        return {"success": True, "message": f"Workspace {workspace_id} deletado"}
    except FabricAPIError as e:
        return e.to_dict()
```

#### Se melhorando **documentação**

```markdown
# QUICK_START.md / README.md / skill files

- Typos: Corrigir + commitar
- Exemplos: Testar localmente antes de adicionar
- Seções: Manter consistência de formato (markdown headers, bullets)
```

#### Se adicionando **skill** ou **agent**

```markdown
# skills/meu-topico/SKILL.md

---
name: meu-topico
description: >
  Descrição curta do quê esse skill faz.
  Use quando o usuário...
  Triggers: palavra-chave1, palavra-chave2
delegates_to:
  - skill-1
  - skill-2
---

# Meu Tópico — Skill

[Conteúdo estruturado com padrão Must/Prefer/Avoid]
```

### 5. Teste local

```bash
# Se mudou Python code
python -m pytest tests/  # se houver testes

# Se mudou documentação
# Ler no markdown editor (VS Code, GitHub)

# Se adicionou tool
python -c "
import asyncio
from tools.outro_modulo import handle_sua_tool
result = asyncio.run(handle_sua_tool({'param': 'valor'}))
print(result)
"

# Se testando com Claude
python server.py
# Em outro terminal:
claude code
# Digitar prompt que usa a nova tool
```

### 6. Commit

```bash
git add .
git commit -m "feat: adicionar delete_workspace tool"
# ou
git commit -m "docs: melhorar QUICK_START.md"
# ou
git commit -m "fix: corrigir cache de token em edge case"
```

**Mensagens de commit** (Conventional Commits):
- `feat:` — nova feature
- `fix:` — bug fix
- `docs:` — documentação
- `refactor:` — refatoração de código (sem feature/fix)
- `test:` — adicionar testes
- `chore:` — atualizações de deps, config, etc

### 7. Push + PR

```bash
git push origin feature/sua-feature
```

Abrir Pull Request no GitHub:
- **Título**: Breve resumo
- **Description**: Explique:
  - O quê muda?
  - Por quê?
  - Como testar?
  - Screenshots se aplicável

---

## 📐 Code style

### Python

- **PEP 8**: Usar black/ruff para formatting
  ```bash
  pip install black ruff
  black tools/
  ruff check tools/
  ```

- **Type hints**: Sempre tipificar
  ```python
  async def my_function(arg1: str, arg2: int) -> dict:
      pass
  ```

- **Docstrings**: Usar format padrão
  ```python
  async def my_function(workspace_id: str) -> dict:
      """Descrição breve.
      
      Args:
          workspace_id: UUID do workspace
      
      Returns:
          {"success": True, "data": {...}} ou {"success": False, "error": {...}}
      
      Raises:
          FabricAPIError: Se workspace não existe
      """
  ```

### Markdown

- **Headers**: 1-2-3 hífens (`#` `##` `###`)
- **Code blocks**: Sempre com language tag (```python, ```bash, etc)
- **Links**: Texto → URL (não hardcoded URLs inline)
- **Tabelas**: Markdown format com `|` delimitador

---

## ✅ Checklist antes de PR

- ☑️ Code não tem print() de debug
- ☑️ .env.example atualizado (se config nova)
- ☑️ README / skill atualizado (se feature nova)
- ☑️ Commits com mensagens claras (Conventional Commits)
- ☑️ Testei localmente (pytest, manual, ou com Claude)
- ☑️ Não commitei `.env` ou `.venv/`
- ☑️ PR description explica o quê + por quê

---

## 🚀 Depois da PR aceita

1. Seu branch é merged ao `main`
2. GitHub Actions roda (se houver CI)
3. Você vira **contributor** oficial! 🎉

---

## ❓ Dúvidas?

- Comentar na issue/discussão
- Abrir "Draft PR" para feedback antes de finalizar
- Perguntar no Discord/Slack da comunidade (se houver)

---

**Obrigado por contribuir! ❤️**
