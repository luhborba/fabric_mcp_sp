---
name: sqldw-consumption
description: >
  Consultar e explorar dados em Fabric Warehouses e SQL Endpoints de Lakehouses via MCP.
  Use para: SELECT queries, exploração de schema, descoberta de metadados, queries analíticas,
  validação de dados, relatórios ad-hoc via SQL.
  Esta skill é READ-ONLY — para DDL/DML use sqldw-authoring.
  Triggers: "consultar warehouse", "SELECT no Fabric", "explorar schema", "contar registros",
  "validar dados", "query analítica SQL", "listar tabelas do warehouse", "SQL Endpoint".
---

# SQL DW Consumption — MCP Skill

> **REGRA**: Esta skill é read-only. Não execute DDL, DML ou operações de escrita.
> **REGRA**: Máximo 10.000 linhas por query. Use `TOP`/`OFFSET FETCH` para paginar.

## Referência de Tools

`SDD.md § 6.3 (Warehouses)`. Parâmetros: `skills/fabric-mcp/SKILL.md § WAREHOUSES`.

---

## Must / Prefer / Avoid

### MUST DO
- Resolver `warehouse_id` com `list_warehouses(workspace_id)` antes de `execute_sql`
- Sempre incluir `TOP N` ou `WHERE` em queries exploratórias
- Usar `sys.tables`, `sys.columns` para descoberta de schema antes de queries de dados

### PREFER
- Cross-database queries com 3-part naming: `workspace.database.schema.tabela`
- `INFORMATION_SCHEMA.COLUMNS` para exploração de schema amigável
- `COUNT(*)` antes de `SELECT *` para estimar volume
- `queryinsights.exec_requests_history` para diagnóstico de performance

### AVOID
- `SELECT *` sem `TOP` ou `WHERE` — pode retornar volumes imensos truncados
- Queries sem estimativa de volume prévia em tabelas Bronze
- DDL ou DML nesta skill — usar sqldw-authoring

---

## Queries de Descoberta de Schema

```sql
-- Listar todas as tabelas e views
SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_SCHEMA, TABLE_NAME

-- Colunas de uma tabela específica
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'vendas'
ORDER BY ORDINAL_POSITION

-- Contagem de registros por tabela (discovery)
SELECT 
    t.name AS tabela,
    p.rows AS total_registros
FROM sys.tables t
JOIN sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0, 1)
ORDER BY p.rows DESC
```

---

## Fluxos Comuns

### Explorar warehouse desconhecido
```
1. list_warehouses(workspace_id) → obter warehouse_id
2. execute_sql(workspace_id, warehouse_id,
   "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
3. execute_sql(workspace_id, warehouse_id,
   "SELECT TOP 5 * FROM schema.tabela") → amostra
4. execute_sql(workspace_id, warehouse_id,
   "SELECT COUNT(*) FROM schema.tabela") → volume
```

### Query analítica com agregação
```
execute_sql(workspace_id, warehouse_id, """
    SELECT 
        YEAR(data_venda) AS ano,
        MONTH(data_venda) AS mes,
        SUM(valor) AS total,
        COUNT(*) AS qtd_pedidos
    FROM gold.vendas
    WHERE data_venda >= '2026-01-01'
    GROUP BY YEAR(data_venda), MONTH(data_venda)
    ORDER BY ano, mes
""")
```

### Diagnóstico de performance (histórico 30 dias)
```sql
SELECT TOP 20
    start_time,
    end_time,
    DATEDIFF(second, start_time, end_time) AS duracao_segundos,
    command,
    status
FROM queryinsights.exec_requests_history
WHERE status = 'Succeeded'
ORDER BY duracao_segundos DESC
```

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| Query retorna exatamente 10.000 linhas | Truncamento do `execute_sql` | Paginar com `OFFSET 0 ROWS FETCH NEXT 10000 ROWS ONLY` |
| 3-part query falha | Workspace diferente não acessível via cross-DB | Cross-DB só funciona no mesmo workspace |
| `sys.stats` vazio | Estatísticas não geradas automaticamente | Executar `UPDATE STATISTICS tabela` |
| SQL Endpoint desatualizado após ETL | Cache de metadados stale | Aguardar sync automático (~5 min) ou recarregar |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
