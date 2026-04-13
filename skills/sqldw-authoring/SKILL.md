---
name: sqldw-authoring
description: >
  Criar e gerenciar Fabric Data Warehouses, executar T-SQL de escrita (DDL/DML) via MCP.
  Use quando o usuário quiser: criar warehouses, criar tabelas (DDL), inserir/atualizar/deletar dados,
  criar views/procedures/schemas no warehouse, executar scripts de ETL via SQL.
  Para queries SELECT de leitura, use sqldw-consumption.
  Triggers: "criar warehouse", "CREATE TABLE", "INSERT INTO", "MERGE", "schema SQL",
  "stored procedure warehouse", "ETL via SQL", "DDL Fabric", "criar view warehouse".
---

# SQL DW Authoring — MCP Skill

> **REGRA CRÍTICA**: Fabric Warehouse usa **Snapshot Isolation** — sem dirty reads, mas write-write conflicts são possíveis. Transações longas aumentam o risco.
> **REGRA CRÍTICA**: `execute_sql` retorna máximo 10.000 linhas. Para ETL em volume use notebooks PySpark.

## Referência de Tools

`SDD.md § 6.3 (Warehouses)`. Parâmetros: `skills/fabric-mcp/SKILL.md § WAREHOUSES`.

---

## Must / Prefer / Avoid

### MUST DO
- Resolver warehouse_id via `list_warehouses` antes de `execute_sql`
- Usar **tipos de dados suportados**: `VARCHAR`, `INT`, `BIGINT`, `DECIMAL`, `DATE`, `DATETIME2`, `BIT`
- **Evitar**: `NVARCHAR`, `DATETIME`, `MONEY` — não suportados no Fabric Warehouse
- Usar CTAS (CREATE TABLE AS SELECT) para criação de tabelas de staging
- Tratar erros 409 (conflict) em DML pesado com retry + backoff

### PREFER
- Schemas para organizar objetos: `CREATE SCHEMA bronze`, `CREATE SCHEMA gold`
- `MERGE` para upserts — mais eficiente que DELETE + INSERT
- `TRUNCATE TABLE` antes de full refresh — mais rápido que DELETE sem WHERE
- Views no SQL Endpoint para expor dados do lakehouse sem duplicação

### AVOID
- Transações longas (> 30 segundos) — aumentam chance de write-write conflict
- `SELECT *` em INSERT — especifique colunas explicitamente
- `NVARCHAR` ou `DATETIME` — causam erro silencioso ou type mismatch
- DDL no SQL Endpoint de Lakehouse (somente leitura — use warehouse para escrita)

---

## T-SQL Suportado no Fabric Warehouse

```sql
-- Tipos de dados seguros
CREATE TABLE vendas (
    id          INT NOT NULL,
    cliente_id  BIGINT,
    valor       DECIMAL(18,2),
    data_venda  DATE,
    descricao   VARCHAR(500),
    ativo       BIT DEFAULT 1
)

-- CTAS — criar tabela a partir de SELECT
CREATE TABLE gold.resumo_mensal AS
SELECT 
    YEAR(data_venda) AS ano,
    MONTH(data_venda) AS mes,
    SUM(valor) AS total
FROM silver.vendas
GROUP BY YEAR(data_venda), MONTH(data_venda)

-- MERGE (Upsert)
MERGE INTO gold.clientes AS target
USING staging.clientes_novos AS source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET target.nome = source.nome
WHEN NOT MATCHED THEN INSERT (id, nome) VALUES (source.id, source.nome)
```

---

## Fluxos Comuns

### Criar warehouse e estrutura inicial
```
1. list_workspaces() → obter workspace_id
2. get_workspace(workspace_id) → verificar capacityId
3. create_warehouse(workspace_id, "dw_analytics", description)
4. execute_sql(workspace_id, warehouse_id, "CREATE SCHEMA bronze")
5. execute_sql(workspace_id, warehouse_id, "CREATE SCHEMA silver")
6. execute_sql(workspace_id, warehouse_id, "CREATE SCHEMA gold")
```

### ETL com MERGE
```
1. execute_sql(workspace_id, warehouse_id, "CREATE TABLE staging.vendas (...)")
2. execute_sql(workspace_id, warehouse_id, "INSERT INTO staging.vendas SELECT ...")
3. execute_sql(workspace_id, warehouse_id, "MERGE INTO gold.vendas USING staging.vendas ...")
4. execute_sql(workspace_id, warehouse_id, "TRUNCATE TABLE staging.vendas")
```

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| Erro de tipo ao criar tabela | `NVARCHAR`/`DATETIME`/`MONEY` não suportados | Usar `VARCHAR`/`DATETIME2`/`DECIMAL` |
| Write-write conflict (409) | Transações paralelas na mesma tabela | Serializar writes ou usar retry com backoff |
| DDL no SQL Endpoint falha | SQLEP é read-only | Usar Warehouse para DDL/DML |
| `execute_sql` retorna dados truncados | Limite de 10.000 linhas | Paginar query com `OFFSET`/`FETCH NEXT` |

---

## Time Travel no Warehouse

```sql
-- Leitura em ponto no tempo (retenção: 30 dias)
SELECT * FROM gold.vendas
FOR TIMESTAMP AS OF '2026-03-01 10:00:00'

-- Comparar versões
SELECT * FROM gold.vendas FOR TIMESTAMP AS OF '2026-03-01'
EXCEPT
SELECT * FROM gold.vendas FOR TIMESTAMP AS OF '2026-02-28'
```

---

**Version:** 1.0.0 | **Data:** 2026-04-09
