---
name: powerbi-consumption
description: >
  Explorar e consultar Semantic Models do Power BI/Fabric via DAX usando MCP.
  Use para: descoberta de schema (tabelas, colunas, medidas, relacionamentos),
  execução de queries DAX analíticas, validação de dados, auditoria de modelo.
  Esta skill é READ-ONLY — para criar/atualizar modelos use powerbi-authoring.
  Triggers: "consultar modelo semântico", "DAX query", "listar medidas", "listar tabelas do modelo",
  "metadados do modelo", "executar DAX", "validar semantic model", "INFO.VIEW".
---

# Power BI Consumption — MCP Skill

> **REGRA**: Esta skill é read-only — apenas DAX de consulta e descoberta de metadados.
> **REGRA**: Use `INFO.VIEW.*` para descoberta de schema — requer apenas permissão de leitura.
> **REGRA**: `INFO.*` (sem VIEW) pode exigir permissões elevadas — testar com `INFO.VIEW.*` primeiro.

## Referência de Tools

`SDD.md § 6.7 (Semantic Models)`. Parâmetros: `skills/fabric-mcp/SKILL.md § SEMANTIC MODELS`.

---

## Must / Prefer / Avoid

### MUST DO
- Resolver `model_id` com `list_semantic_models(workspace_id)` antes de `execute_dax`
- Usar `INFO.VIEW.*` para descoberta inicial — mais permissivo que `INFO.*`
- Adicionar `TOP N` ou `TOPN()` em queries de dados para limitar resultados (máx 100.000 linhas)

### PREFER
- Sequência de descoberta: tabelas → colunas → medidas → relacionamentos
- `SUMMARIZECOLUMNS` para análises multidimensionais
- `CALCULATETABLE` + filtros para subsets analíticos
- `COUNTROWS` antes de queries de dados para estimar volume

### AVOID
- `INFO.*` sem `VIEW` como primeira tentativa — pode falhar por permissão
- `EVALUATE tabela` sem `TOPN()` em fatos grandes
- Operações de escrita nesta skill

---

## Queries de Descoberta de Schema

```dax
-- 1. Descobrir tabelas
EVALUATE
INFO.VIEW.TABLES()
ORDER BY [Name]

-- 2. Descobrir colunas (filtrar por tabela)
EVALUATE
SELECTCOLUMNS(
    FILTER(INFO.VIEW.COLUMNS(), [TableID] = 1),
    "Tabela", [TableName],
    "Coluna", [ExplicitName],
    "Tipo", [DataType]
)

-- 3. Descobrir medidas
EVALUATE
SELECTCOLUMNS(
    INFO.VIEW.MEASURES(),
    "Tabela", [TableName],
    "Medida", [Name],
    "Expressão", [Expression],
    "Formato", [FormatString]
)
ORDER BY [TableName], [Name]

-- 4. Descobrir relacionamentos
EVALUATE
INFO.VIEW.RELATIONSHIPS()

-- 5. Estimar cardinalidade das tabelas
EVALUATE
SELECTCOLUMNS(
    INFO.VIEW.TABLES(),
    "Tabela", [Name],
    "Linhas", [RowsCount]
)
ORDER BY [Linhas] DESC
```

---

## Queries DAX Analíticas

```dax
-- Análise de vendas por categoria
EVALUATE
SUMMARIZECOLUMNS(
    'Produto'[Categoria],
    "Total Vendas", [Total Vendas],
    "Qtd Pedidos", COUNTROWS('Vendas')
)
ORDER BY [Total Vendas] DESC

-- Top 10 clientes
EVALUATE
TOPN(
    10,
    SUMMARIZECOLUMNS(
        'Cliente'[Nome],
        "Total", [Total Vendas]
    ),
    [Total], DESC
)

-- Variação MoM (Month over Month)
EVALUATE
VAR _tabela =
    SUMMARIZECOLUMNS(
        'Data'[AnoMes],
        "Atual", [Total Vendas],
        "Anterior", CALCULATE([Total Vendas], DATEADD('Data'[Data], -1, MONTH))
    )
RETURN
    ADDCOLUMNS(_tabela, "Variação %", DIVIDE([Atual] - [Anterior], [Anterior]))
ORDER BY 'Data'[AnoMes] DESC
```

---

## Fluxo de Descoberta Recomendado

```
1. list_semantic_models(workspace_id) → obter model_id por nome
2. execute_dax(model_id, "EVALUATE INFO.VIEW.TABLES()") → inventário de tabelas
3. execute_dax(model_id, "EVALUATE INFO.VIEW.MEASURES()") → medidas disponíveis
4. execute_dax(model_id, "EVALUATE INFO.VIEW.RELATIONSHIPS()") → modelo de relacionamentos
5. execute_dax(model_id, "EVALUATE TOPN(5, 'TabelaFato')") → amostra de dados
6. → Construir queries analíticas baseadas no schema descoberto
```

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| `INFO.*` retorna erro de permissão | SP sem permissão elevada | Usar `INFO.VIEW.*` |
| `execute_dax` retorna 100.000 linhas exatamente | Truncamento | Usar `TOPN()` ou filtros |
| Medida retorna BLANK | Filtro sem match | Verificar relacionamentos com `INFO.VIEW.RELATIONSHIPS()` |
| `SUMMARIZECOLUMNS` lento | Modelo sem estatísticas ou refresh pendente | Disparar refresh primeiro |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
