---
name: workspace-management
description: >
  Gerenciar workspaces, capacidades e permissões no Microsoft Fabric via MCP.
  Use quando o usuário quiser: criar/listar/deletar workspaces, atribuir capacidades,
  gerenciar roles (Admin, Member, Contributor, Viewer), documentar inventário de workspace.
  Triggers: "criar workspace", "listar workspaces", "atribuir capacidade", "gerenciar permissões",
  "adicionar membro", "documentar workspace", "inventário Fabric".
---

# Workspace Management — MCP Skill

> **REGRA CRÍTICA**: Nunca invente IDs. Use `list_workspaces` para obter IDs reais antes de qualquer operação.
> **REGRA CRÍTICA**: Sempre confirme com o usuário antes de `delete_workspace` — é irreversível.

## Referência de Tools

Parâmetros completos: ver `mcp_fabric/SDD.md § 6.1` e `skills/fabric-mcp/SKILL.md § WORKSPACES`.

---

## Must / Prefer / Avoid

### MUST DO
- Sempre resolver workspace por nome com `list_workspaces` antes de operar por ID
- Confirmar explicitamente antes de `delete_workspace`
- Verificar `capacityId` antes de criar itens Fabric (Lakehouse, Warehouse, etc.) — workspace sem capacidade não suporta Spark
- Usar `least-privilege` nas roles: padrão Viewer, escalar com justificativa

### PREFER
- Convencionar nomes: `{projeto}-{camada}-{env}` (ex: `analytics-gold-prod`)
- Adicionar `description` descritivo ao criar workspaces
- Checar `list_role_assignments` antes de `add_role_assignment` para evitar duplicatas

### AVOID
- Hardcoded IDs em qualquer instrução ao usuário
- Misturar workspaces de dev e prod na mesma capacidade
- Conceder `Admin` ou `Member` sem justificativa de negócio

---

## Fluxos Comuns

### Criar workspace com capacidade e times
```
1. list_workspaces() → verificar se nome já existe
2. create_workspace(display_name, description, capacity_id?)
3. add_role_assignment(workspace_id, principal_id, "User"|"Group", "Member")
4. add_role_assignment(workspace_id, principal_id, "User", "Viewer") → para analistas
```

### Documentar inventário completo de workspace
```
1. get_workspace(workspace_id) → metadados e tipo
2. list_lakehouses(workspace_id)
3. list_warehouses(workspace_id)
4. list_notebooks(workspace_id)
5. list_pipelines(workspace_id)
6. list_semantic_models(workspace_id)
7. list_reports(workspace_id)
→ Consolidar em relatório markdown com contagens e papéis de cada artefato
```

### Atribuir workspace a capacidade Fabric
```
1. list_workspaces() → obter workspace_id
2. get_workspace(workspace_id) → verificar estado "Active"
3. assign_to_capacity(workspace_id, capacity_id)
```

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| Workspace sem capacidade não aceita Lakehouse/Warehouse | Fabric items exigem F-SKU ou Trial | Verificar `capacityId` com `get_workspace` |
| `add_role_assignment` falha com 400 | `principal_id` inválido ou já tem role | Checar `list_role_assignments` primeiro |
| `delete_workspace` retorna 409 | Workspace tem itens ativos | Deletar itens individualmente antes |
| Nome de workspace duplicado retorna 400 | Nomes são únicos por tenant | Verificar com `list_workspaces` antes de criar |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
