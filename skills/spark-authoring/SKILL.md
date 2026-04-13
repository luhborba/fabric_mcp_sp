---
name: spark-authoring
description: >
  Desenvolver workflows de engenharia de dados com Spark no Microsoft Fabric via MCP.
  Use quando o usuário quiser: criar/atualizar notebooks PySpark, criar lakehouses,
  configurar tabelas Delta, fazer upload de arquivos, executar notebooks, criar pipelines,
  criar Spark Job Definitions. Triggers: "criar notebook", "desenvolver PySpark",
  "criar lakehouse", "Delta Lake", "configurar ingestão", "criar pipeline", "executar notebook",
  "Spark Job", "infraestrutura Fabric", "provisionar ambiente".
---

# Spark Authoring — MCP Skill

> **REGRA CRÍTICA 1**: Verificar `capacityId` do workspace antes de criar lakehouses — sem capacidade Fabric não há Spark.
> **REGRA CRÍTICA 2**: Verificar jobs recentes antes de `run_notebook` — nunca crie runs duplicados.
> **REGRA CRÍTICA 3**: Conteúdo de notebook deve ser `.ipynb` válido em base64. Cada linha de célula DEVE terminar com `\n`.

## Referência de Tools

Parâmetros completos: `SDD.md § 6.3 (Lakehouses)`, `§ 6.4 (Notebooks)`, `§ 6.5 (Pipelines)`, `§ 6.6 (Spark Jobs)`.
Skill anti-alucinação: `skills/fabric-mcp/SKILL.md`.

---

## Must / Prefer / Avoid

### MUST DO
- Verificar se workspace tem capacidade antes de qualquer operação Spark
- Checar jobs recentes (últimos 5 min) com `get_job_status` antes de `run_notebook`
- Capturar `job_instance_id` imediatamente após `run_notebook`/`run_pipeline`
- Fazer polling com `get_job_status` até status terminal: `Succeeded`, `Failed`, `Cancelled`
- Usar `enable_schemas: true` ao criar lakehouses para suporte a SQL Analytics Endpoint
- Células de notebook: cada linha no array `source` DEVE terminar com `\n`

### PREFER
- Notebooks separados por camada (bronze_ingestao, silver_transformacao, gold_agregacao)
- Nomear notebooks com convenção: `nb_{camada}_{funcao}` (ex: `nb_bronze_vendas_raw`)
- Parametrizar caminhos, workspace IDs e lakehouse names via variáveis no início do notebook
- Lakehouses com schemas habilitados para organização em Bronze/Silver/Gold

### AVOID
- Hardcoded workspace IDs ou lakehouse IDs no código dos notebooks
- Criar novo run se já existe job em andamento para o mesmo notebook
- `SELECT *` sem `LIMIT` em tabelas Bronze (crescem indefinidamente)
- Executar `VACUUM` sem verificar dependências downstream

---

## Formato do Notebook (.ipynb em base64)

```python
# Estrutura mínima de uma célula de código válida
{
  "cell_type": "code",
  "execution_count": null,       # OBRIGATÓRIO — null, não omitir
  "outputs": [],                  # OBRIGATÓRIO — lista vazia, não omitir
  "source": [
    "df = spark.read.parquet('Files/raw/dados.parquet')\n",  # \n obrigatório
    "df.show(10)"                  # última linha sem \n
  ],
  "metadata": {}
}
```

**Erros comuns com notebooks:**
- Omitir `"execution_count": null` → falha silenciosa no Fabric
- Omitir `"outputs": []` → `Job instance failed without detail error`
- Linhas sem `\n` → código se mescla em uma linha só

---

## Fluxos Comuns

### Criar e executar notebook simples
```
1. get_workspace(workspace_id) → verificar capacityId
2. list_notebooks(workspace_id) → verificar se já existe
3. create_notebook(workspace_id, display_name, description)
4. update_notebook_definition(workspace_id, notebook_id, definition_base64)
5. run_notebook(workspace_id, notebook_id)
6. get_job_status(workspace_id, notebook_id, job_instance_id) → polling
```

### Criar lakehouse com estrutura de camadas
```
1. create_lakehouse(workspace_id, "bronze", enable_schemas=true)
2. create_lakehouse(workspace_id, "silver", enable_schemas=true)
3. create_lakehouse(workspace_id, "gold", enable_schemas=true)
```

### Criar pipeline orquestrando notebooks
```
1. list_notebooks(workspace_id) → obter IDs dos notebooks
2. create_pipeline(workspace_id, "pipeline_medallion")
→ Definição da pipeline referencia os notebook IDs em atividades encadeadas
3. run_pipeline(workspace_id, pipeline_id)
4. get_job_status(workspace_id, pipeline_id, job_instance_id)
```

---

## Configurações Spark por Camada

| Camada | Perfil | Configurações-chave |
|--------|--------|---------------------|
| Bronze | Write-heavy | `spark.microsoft.delta.optimizeWrite.enabled=true`, V-Order desabilitado |
| Silver | Balanced | `spark.microsoft.delta.optimizeWrite.enabled=true`, V-Order habilitado |
| Gold | Read-heavy | V-Order habilitado, ZORDER por colunas de filtro frequente, OPTIMIZE após writes |

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| Notebook falha sem mensagem de erro | `.ipynb` malformado | Verificar `execution_count` e `outputs` em todas as células |
| Job duplicado criado | `run_notebook` chamado sem verificar recentes | Checar `get_job_status` antes de novo run |
| Lakehouse sem SQL Analytics Endpoint | `enable_schemas=false` | Recriar com `enable_schemas=true` |
| `load_table` retorna 404 | Arquivo não existe no OneLake | Upload o arquivo via `upload_file` primeiro |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
