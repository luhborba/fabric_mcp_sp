---
name: powerbi-authoring
description: >
  Criar, atualizar, publicar e gerenciar Semantic Models e Reports do Power BI/Fabric via MCP.
  Use quando o usuário quiser: criar semantic models, fazer refresh, atualizar definição TMDL/BIM,
  criar relatórios, clonar relatórios, exportar relatórios, rebind de modelo, gerenciar datasources.
  Triggers: "criar modelo semântico", "refresh dataset", "publicar relatório", "criar report",
  "clonar relatório", "exportar PDF", "atualizar TMDL", "criar semantic model", "rebind relatório".
---

# Power BI Authoring — MCP Skill

> **LIMITAÇÃO CONHECIDA**: Service Principal NÃO pode criar Semantic Models em modo DirectLake via API v1. Use Import Mode ou Composite Mode.
> **REGRA**: Criar relatório do zero exige JSON completo do `.pbir`. Prefira `clone_report` de template.
> **REGRA**: `refresh_semantic_model` é assíncrono — usar `get_refresh_history` para polling.

## Referência de Tools

`SDD.md § 6.7 (Semantic Models)`, `§ 6.8 (Reports)`.
Parâmetros: `skills/fabric-mcp/SKILL.md § SEMANTIC MODELS` e `§ REPORTS`.

---

## Must / Prefer / Avoid

### MUST DO
- Verificar `get_refresh_history` após `refresh_semantic_model` até status `Completed`
- Usar `execute_dax` com `EVALUATE` para validar dados antes de publicar relatório
- Ao criar semantic model: enviar definição `.bim` ou TMDL em base64 válido
- Confirmar com usuário antes de `delete_semantic_model` ou `delete_report`

### PREFER
- `clone_report` para criar novos relatórios a partir de template — mais simples e confiável
- Refresh parcial (`DataOnly`) para tabelas que não tiveram mudança de schema
- `get_datasources` para verificar datasources configurados antes de refresh
- Nomear modelos com convenção: `sm_{dominio}_{granularidade}` (ex: `sm_vendas_mensal`)

### AVOID
- Tentar criar Semantic Model em modo DirectLake via SP — não funciona na API v1
- `refresh_semantic_model` sem verificar `get_datasources` configurados primeiro
- Criar relatório do zero via API sem ter o JSON `.pbir` completo — use `clone_report`
- Executar DAX com `EVALUATE` sem `TOP N` em fatos grandes

---

## Formato da Definição de Semantic Model

```json
// Estrutura do definition (BIM/TMSL em base64)
{
  "format": "TMSL",
  "parts": [
    {
      "path": "model.bim",
      "payload": "<base64 do JSON do modelo>",
      "payloadType": "InlineBase64"
    }
  ]
}
```

**Exemplo de model.bim mínimo:**
```json
{
  "name": "Model",
  "compatibilityLevel": 1550,
  "model": {
    "culture": "pt-BR",
    "dataSources": [],
    "tables": [
      {
        "name": "Vendas",
        "columns": [
          {"name": "ID", "dataType": "int64", "sourceColumn": "id"},
          {"name": "Valor", "dataType": "decimal", "sourceColumn": "valor"}
        ],
        "measures": [
          {
            "name": "Total Vendas",
            "expression": "SUM(Vendas[Valor])",
            "formatString": "R$ #,##0.00"
          }
        ],
        "partitions": [
          {
            "name": "Vendas-partition",
            "source": {
              "type": "m",
              "expression": "let\n    Fonte = Lakehouse{[Id=\"{lakehouse_id}\",Name=\"Vendas\"]}[Data],\n    Navegação = Fonte\nin\n    Navegação"
            }
          }
        ]
      }
    ]
  }
}
```

---

## Fluxos Comuns

### Criar Semantic Model e fazer refresh
```
1. list_lakehouses(workspace_id) → confirmar fonte de dados
2. create_semantic_model(workspace_id, display_name, definition_base64)
3. get_semantic_model_definition(workspace_id, model_id) → verificar criação
4. refresh_semantic_model(workspace_id, model_id, "Full")
5. get_refresh_history(workspace_id, model_id) → polling até "Completed"
6. execute_dax(workspace_id, model_id, "EVALUATE TOPN(5, Vendas)") → validar dados
```

### Clonar relatório para novo workspace
```
1. list_reports(workspace_id) → obter report_id do template
2. clone_report(workspace_id, report_id, "Relatório Vendas Q1", target_workspace_id)
3. get_report(target_workspace_id, new_report_id) → confirmar
```

### Exportar relatório como PDF
```
1. list_reports(workspace_id) → obter report_id
2. export_report(workspace_id, report_id, "PDF")
→ polling até job concluído
→ URL de download retornada no resultado
```

### Validar modelo com DAX antes de publicar
```
execute_dax(workspace_id, model_id, """
EVALUATE
SUMMARIZECOLUMNS(
    'Vendas'[Categoria],
    "Total", [Total Vendas],
    "Qtd", COUNTROWS('Vendas')
)
ORDER BY [Total] DESC
""")
```

---

## Tipos de Refresh

| Tipo | Quando usar |
|------|-------------|
| `Full` | Primeira vez ou mudança de schema |
| `DataOnly` | Atualização de dados sem mudança de schema |
| `Calculate` | Recalcular medidas calculadas sem recarregar dados |
| `Automatic` | Deixar o Fabric decidir o escopo |

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| `create_semantic_model` retorna 400 | BIM JSON inválido ou base64 malformado | Validar JSON antes de encodar |
| SP não consegue criar DirectLake | Limitação da API v1 | Usar Import ou Composite Mode |
| Refresh falha com "Data source not found" | Datasource não configurado | `get_datasources` → configurar credenciais no portal |
| `export_report` demora muito | Relatório grande com muitas páginas | Usar parâmetro `pages` para exportar só páginas necessárias |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
