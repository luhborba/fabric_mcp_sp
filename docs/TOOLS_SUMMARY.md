# 🛠️ Tools Reference — 65+ Ferramentas Disponíveis

> Referência rápida de todas as tools MCP de fabric-mcp. Para exemplos e detalhes, ver o skill correspondente ou README.

---

## 📊 Resumo por domínio

| Domínio | Tools | Status |
|---------|-------|--------|
| **Workspaces** | 8 | ✅ Core |
| **Lakehouses** | 7 | ✅ Core |
| **Warehouses** | 5 | ✅ Core |
| **Notebooks** | 8 | ✅ Core |
| **Pipelines** | 6 | ✅ Core |
| **Spark Jobs** | 6 | ✅ Core |
| **Semantic Models** | 6 | ✅ Core |
| **Reports** | 5 | ✅ Core |
| **OneLake** | 8 | ✅ Core |
| **TOTAL** | **65+** | ✅ |

---

## 🏢 Workspaces (8 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_workspaces` | `capacity_id?` | `[Workspace]` | Listar todos os workspaces |
| `get_workspace` | `workspace_id` | `Workspace` | Obter detalhes de um workspace |
| `create_workspace` | `display_name, description?, capacity_id?` | `Workspace` | Criar novo workspace |
| `delete_workspace` | `workspace_id` | `{success: bool}` | Deletar workspace (⚠️ irreversível) |
| `update_workspace` | `workspace_id, display_name?, description?` | `Workspace` | Atualizar metadados |
| `list_role_assignments` | `workspace_id` | `[RoleAssignment]` | Ver quem tem acesso |
| `add_role_assignment` | `workspace_id, principal_id, principal_type, role` | `RoleAssignment` | Adicionar usuário/grupo |
| `remove_role_assignment` | `workspace_id, principal_id` | `{success: bool}` | Remover acesso |

**Exemplo**:
```
"Crie um workspace chamado 'analytics-prod' com capacidade [CAPACITY_ID]"
→ Claude chama create_workspace(...)
```

---

## 📁 Lakehouses (7 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_lakehouses` | `workspace_id` | `[Lakehouse]` | Listar lakehouses do workspace |
| `create_lakehouse` | `workspace_id, display_name, description?` | `Lakehouse` | Criar novo lakehouse |
| `get_lakehouse` | `workspace_id, lakehouse_id` | `Lakehouse` | Obter detalhes |
| `onelake_list_files` | `workspace_id, lakehouse_id, folder_path?` | `[File]` | Listar arquivos no OneLake |
| `onelake_read_file` | `workspace_id, lakehouse_id, file_path` | `File` (conteúdo) | Ler arquivo (CSV, Parquet, etc) |
| `onelake_write_file` | `workspace_id, lakehouse_id, file_path, content` | `{success: bool}` | Escrever arquivo no OneLake |
| `execute_lakehouse_query` | `workspace_id, lakehouse_id, query` | `[Row]` | Executar SQL no Lakehouse |

**Exemplo**:
```
"Leia o arquivo 'customers.parquet' do lakehouse 'bronze' no workspace [ID]"
→ Claude chama onelake_read_file(...)
→ Retorna conteúdo ou path para download
```

---

## 🏛️ Warehouses (5 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_warehouses` | `workspace_id` | `[Warehouse]` | Listar warehouses do workspace |
| `create_warehouse` | `workspace_id, display_name, description?` | `Warehouse` | Criar novo warehouse |
| `get_warehouse_connection` | `workspace_id, warehouse_id` | `Connection` (server, db, port) | Obter string de conexão |
| `execute_warehouse_query` | `workspace_id, warehouse_id, query` | `[Row]` | Executar query SQL T-SQL |
| `get_warehouse_status` | `workspace_id, warehouse_id` | `Status` (ready, paused, etc) | Ver status |

**Exemplo**:
```
"Execute a query SELECT COUNT(*) FROM customers WHERE active=1 no warehouse 'dwh-prod'"
→ Claude chama execute_warehouse_query(...)
→ Retorna resultado em segundos
```

---

## 📔 Notebooks (8 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_notebooks` | `workspace_id` | `[Notebook]` | Listar notebooks do workspace |
| `create_notebook` | `workspace_id, display_name, description?, code?` | `Notebook` | Criar novo notebook |
| `get_notebook` | `workspace_id, notebook_id` | `Notebook` (metadados) | Obter detalhes |
| `get_notebook_definition` | `workspace_id, notebook_id` | `Definition` (código completo) | Obter código-fonte |
| `update_notebook` | `workspace_id, notebook_id, code` | `Notebook` | Atualizar código |
| `execute_notebook` | `workspace_id, notebook_id, parameters?` | `Execution` (status, output) | Executar notebook |
| `get_notebook_execution` | `workspace_id, notebook_id, execution_id` | `Execution` (logs, result) | Ver resultado/logs |
| `delete_notebook` | `workspace_id, notebook_id` | `{success: bool}` | Deletar notebook |

**Exemplo**:
```
"Crie um notebook chamado 'ETL_Pipeline' com código Spark que leia CSV e escreva em Delta"
→ Claude gera código PySpark
→ chama create_notebook(...) com o código
```

---

## 🔄 Pipelines (6 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_pipelines` | `workspace_id` | `[Pipeline]` | Listar pipelines do workspace |
| `create_pipeline` | `workspace_id, display_name, description?` | `Pipeline` | Criar nova pipeline |
| `add_pipeline_activity` | `workspace_id, pipeline_id, activity_def` | `Activity` | Adicionar atividade (notebook, notebook, SQL, etc) |
| `run_pipeline` | `workspace_id, pipeline_id` | `Run` (run_id) | Executar pipeline |
| `get_pipeline_run` | `workspace_id, pipeline_id, run_id` | `Run` (status, logs) | Ver status/resultado |
| `list_pipeline_runs` | `workspace_id, pipeline_id` | `[Run]` | Histórico de execuções |

**Exemplo**:
```
"Crie uma pipeline que executa o notebook ETL_Pipeline a cada dia às 2 da manhã"
→ Claude chama create_pipeline(...)
→ chama add_pipeline_activity(...) com trigger diário
```

---

## ⚡ Spark Jobs (6 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_spark_jobs` | `workspace_id` | `[SparkJob]` | Listar spark jobs do workspace |
| `create_spark_job` | `workspace_id, display_name, main_file, parameters?` | `SparkJob` | Criar novo spark job |
| `get_spark_job` | `workspace_id, spark_job_id` | `SparkJob` (detalhes) | Obter definição |
| `run_spark_job` | `workspace_id, spark_job_id, parameters?` | `Run` (run_id) | Executar job |
| `get_spark_job_run` | `workspace_id, spark_job_id, run_id` | `Run` (status, logs, output) | Ver resultado |
| `list_spark_job_runs` | `workspace_id, spark_job_id` | `[Run]` | Histórico |

**Exemplo**:
```
"Execute o spark job 'data_processing' com o parâmetro date=2026-04-13"
→ Claude chama run_spark_job(...)
```

---

## 📊 Semantic Models (6 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_semantic_models` | `workspace_id` | `[SemanticModel]` | Listar modelos do workspace |
| `create_semantic_model` | `workspace_id, display_name, pbix_file?` | `SemanticModel` | Criar novo modelo |
| `get_semantic_model_schema` | `workspace_id, semantic_model_id` | `Schema` (tables, columns, types) | Explorar estrutura |
| `execute_dax_query` | `workspace_id, semantic_model_id, dax_query` | `[Row]` | Executar query DAX |
| `refresh_semantic_model` | `workspace_id, semantic_model_id` | `Refresh` (status, end_time) | Fazer refresh |
| `get_semantic_model_refresh_history` | `workspace_id, semantic_model_id` | `[Refresh]` | Ver histórico de refreshes |

**Exemplo**:
```
"Execute a query DAX: EVALUATE TOPN(10, 'Sales') para o modelo 'FinanceModel'"
→ Claude chama execute_dax_query(...)
→ Retorna top 10 linhas
```

---

## 📈 Reports (5 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `list_reports` | `workspace_id` | `[Report]` | Listar relatórios do workspace |
| `create_report` | `workspace_id, display_name, pbix_file` | `Report` | Fazer upload de relatório |
| `get_report` | `workspace_id, report_id` | `Report` (metadados, pages) | Obter detalhes |
| `update_report_datasource` | `workspace_id, report_id, semantic_model_id` | `Report` | Apontar para modelo diferente |
| `export_report` | `workspace_id, report_id, format` | `File` (PDF, PNG, PPTX) | Exportar relatório |

**Exemplo**:
```
"Exporte o relatório 'Sales Dashboard' em PDF"
→ Claude chama export_report(..., format='PDF')
```

---

## ☁️ OneLake (8 tools)

| Tool | Entrada | Saída | Caso de uso |
|------|---------|-------|-----------|
| `onelake_list_files` | `workspace_id, lakehouse_id, folder_path?` | `[File]` | Listar arquivos/pastas |
| `onelake_read_file` | `workspace_id, lakehouse_id, file_path` | `Content` (bytes) | Ler arquivo inteiro |
| `onelake_write_file` | `workspace_id, lakehouse_id, file_path, content` | `{success: bool}` | Escrever arquivo |
| `onelake_append_file` | `workspace_id, lakehouse_id, file_path, content` | `{success: bool}` | Append a arquivo |
| `onelake_copy_file` | `workspace_id, src_path, dst_path` | `{success: bool}` | Copiar arquivo |
| `onelake_delete_file` | `workspace_id, lakehouse_id, file_path` | `{success: bool}` | Deletar arquivo |
| `onelake_upload_batch` | `workspace_id, lakehouse_id, files` | `[Upload]` | Upload múltiplos arquivos |
| `onelake_get_file_properties` | `workspace_id, lakehouse_id, file_path` | `Properties` (size, modified, etc) | Metadados do arquivo |

**Exemplo**:
```
"Faça upload de todos os arquivos CSV da pasta '/dados/raw' pro OneLake"
→ Claude chama onelake_upload_batch(...)
```

---

## 🔍 Como encontrar a tool certa

| Você quer... | Procure em... | Tool |
|------|------|------|
| Listar coisas | Domínio relevante | `list_{domain}` |
| Criar item novo | Domínio relevante | `create_{item}` |
| Editar / atualizar | Domínio relevante | `update_{item}` |
| Deletar | Domínio relevante | `delete_{item}` |
| Executar código | `notebooks`, `spark_jobs`, `pipelines` | `execute_*`, `run_*` |
| Ler resultado | Domínio relevante | `get_*_result`, `get_*_execution`, `execute_*_query` |
| Monitorar andamento | Domínio relevante | `get_pipeline_run`, `get_spark_job_run`, etc |
| Gerenciar arquivos | `onelake` | `onelake_*` |
| Ler/escrever SQL | `lakehouses`, `warehouses` | `execute_*_query` |
| Gerenciar permissões | `workspaces` | `add_role_assignment`, `list_role_assignments` |

---

## 💡 Dicas de combinação

### 1️⃣ Documentar workspace completamente

```
Claude prompt:
"Documente o workspace [ID]: 
 - Todos os lakehouses, notebooks, pipelines, semantic models, reports
 - Quem tem acesso a cada item
 - Use timestamps: 'last modified'"

Claude sequence:
get_workspace() → list_lakehouses() → list_notebooks() → list_pipelines() 
→ list_semantic_models() → list_reports() → list_role_assignments()
→ Para cada item relevante: get_notebook_definition(), get_semantic_model_schema()
```

### 2️⃣ Criar pipeline ETL end-to-end

```
Claude prompt:
"Crie uma pipeline que:
 1. Leia dados de /raw/customers.parquet no OneLake
 2. Processe com Spark (limpeza)
 3. Salve em /silver/customers_clean
 4. Rode diariamente às 2 AM"

Claude sequence:
onelake_read_file() → create_notebook() → upload código PySpark
→ create_pipeline() → add_pipeline_activity() (notebook + schedule)
```

### 3️⃣ Explorar dados interativamente

```
Claude prompt:
"Qual é o schema da tabela 'customers' no warehouse 'dwh-prod'?
Mostre top 10 registros."

Claude sequence:
get_warehouse_connection() → execute_warehouse_query(SELECT * LIMIT 10)
→ Retorna dados + tipos
```

---

## 🚀 Performance

| Tool | Tempo típico | Notas |
|------|-------------|-------|
| `list_workspace*` | ~200ms | API call simples |
| `create_notebook` | ~1-2s | Async, need wait |
| `execute_warehouse_query` | ~1-30s | Depend on query |
| `onelake_read_file` (small) | ~500ms | Até 10 MB |
| `onelake_upload_batch` | ~1s por arquivo | Async parallelized |
| `run_pipeline` / `run_spark_job` | ~200ms (start) + runtime | Enfileira na Fabric |
| `execute_dax_query` | ~1-5s | Depend on complexity |

---

## ⚠️ Limitações conhecidas (v1.0)

- ❌ Sem suporte a **Dataflows Gen2**
- ❌ Sem suporte a **KQL databases / Eventhouses**
- ❌ Sem suporte a **Capacities management** (criar/deletar/monitorar capacidades)
- ❌ Sem suporte a **Shared datasets** (modelar)
- ❌ OneLake read/write limitado a ~50 MB por call (use batch para files grandes)

---

## 📚 Exemplo completo

```
User: "Quero uma arquitetura Medallion: Bronze → Silver → Gold

Claude:
1. create_lakehouse(name='bronze')       → raw data
2. create_lakehouse(name='silver')       → processed
3. create_lakehouse(name='gold')         → final /analytics
4. create_notebook(name='bronze_ingestion_job')   → SQL insert
5. create_notebook(name='silver_transform_job')   → Spark transform
6. create_notebook(name='gold_aggregation_job')   → SQL aggregate
7. create_pipeline(name='medallion_etl')
8. add_pipeline_activity(bronze_ingestion) → every 1 hour
9. add_pipeline_activity(silver_transform) → after bronze clear
10. add_pipeline_activity(gold_aggregation) → after silver clear
11. create_semantic_model(source=gold)
12. create_report(source=semantic_model)

Result: End-to-end data pipeline + analytics ready!
```

---

**Todas as ferramentas documentadas? Quer contribuir? Vă [CONTRIBUTING.md](CONTRIBUTING.md)** 🎯
