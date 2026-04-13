---
name: spark-consumption
description: >
  Analisar e explorar dados em lakehouses do Microsoft Fabric via MCP.
  Use quando o usuário quiser: listar tabelas de um lakehouse, inspecionar schema,
  executar notebooks de análise, explorar arquivos no OneLake, verificar histórico Delta.
  Para queries SQL simples em lakehouse, prefira sqldw-consumption (SQL Endpoint é mais rápido).
  Triggers: "explorar lakehouse", "listar tabelas", "analisar dados com PySpark",
  "verificar schema", "Delta time travel", "inspecionar arquivos", "conteúdo do notebook".
---

# Spark Consumption — MCP Skill

> **REGRA**: Para queries SELECT simples em tabelas Delta, use `sqldw-consumption` (SQL Endpoint) — é mais rápido e não consome capacidade Spark.
> Use esta skill quando precisar de PySpark, DataFrames, análise cross-lakehouse ou time-travel Delta.

## Referência de Tools

`SDD.md § 6.2 (Lakehouses)`, `§ 6.4 (Notebooks)`, `§ 6.9 (OneLake)`.

---

## Must / Prefer / Avoid

### MUST DO
- Resolver IDs dinamicamente: `list_workspaces` → `list_lakehouses` → operar
- Verificar se workspace tem capacidade antes de executar notebooks de análise
- Usar `LIMIT`/`TOP` em queries exploratórias em tabelas Bronze

### PREFER
- SQL Endpoint (sqldw-consumption) para queries SELECT simples
- `list_lakehouse_tables` para descoberta de schema antes de escrever código
- `get_notebook_definition` + decode base64 para ler conteúdo de notebook existente
- `list_onelake_files` para entender estrutura antes de processar arquivos

### AVOID
- `SELECT *` sem LIMIT em tabelas Bronze
- Criar notebooks de análise com hardcoded lakehouse IDs
- Usar esta skill para queries simples que o SQL Endpoint resolve

---

## Fluxos Comuns

### Explorar estrutura de um lakehouse
```
1. list_workspaces() → obter workspace_id por nome
2. list_lakehouses(workspace_id) → obter lakehouse_id
3. list_lakehouse_tables(workspace_id, lakehouse_id) → tabelas disponíveis
4. list_onelake_files(workspace_name, lakehouse_name, "Files/") → arquivos raw
```

### Ler conteúdo de notebook existente
```
1. list_notebooks(workspace_id) → obter notebook_id por nome
2. get_notebook_definition(workspace_id, notebook_id) → payload base64
3. → Decodificar base64 → JSON do .ipynb → inspecionar células
```

### Verificar histórico de runs de um notebook
```
1. list_notebooks(workspace_id) → obter notebook_id
2. get_job_status(workspace_id, notebook_id, job_instance_id) → status de run específico
```

---

## Delta Time Travel

Para análise de histórico Delta, criar notebook com código:

```python
# Via notebook (run_notebook após create_notebook + update_notebook_definition)

# Histórico da tabela
display(spark.sql("DESCRIBE HISTORY lakehouse.tabela"))

# Leitura de versão específica
df = spark.read.format("delta").option("versionAsOf", 5).load("abfss://...")

# Leitura por timestamp
df = spark.read.format("delta").option("timestampAsOf", "2026-01-01").load("abfss://...")
```

---

**Version:** 1.0.0 | **Data:** 2026-04-09
