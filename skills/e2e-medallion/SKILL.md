---
name: e2e-medallion
description: >
  Implementar Arquitetura Medallion completa (Bronze/Silver/Gold) no Microsoft Fabric via MCP.
  Use quando o usuário quiser: projetar um data lakehouse multi-camadas, configurar infraestrutura
  completa de engenharia de dados, criar pipeline de ingestão até relatório.
  Triggers: "arquitetura medallion", "bronze silver gold", "lakehouse multi-camadas",
  "pipeline end-to-end", "data lakehouse completo", "configurar ambiente de dados",
  "ingestão até relatório", "setup medallion Fabric".
---

# End-to-End Medallion Architecture — MCP Skill

> **REGRA**: Cada camada DEVE ter seu próprio lakehouse separado — nunca misture Bronze, Silver e Gold no mesmo lakehouse.
> **REGRA**: Nunca leia de URLs externas direto no Spark — faça upload via OneLake primeiro.
> **REGRA**: Notebooks criados via MCP devem ter `.ipynb` válido — ver spark-authoring/SKILL.md.

## Referência Cruzada de Skills

Para implementação de cada componente, delegar às skills especializadas:

| Componente | Skill |
|-----------|-------|
| Criar workspaces e lakehouses | `workspace-management`, `spark-authoring` |
| Upload de arquivos raw | `onelake` |
| Notebooks PySpark por camada | `spark-authoring` |
| Queries de validação SQL | `sqldw-consumption` |
| Semantic Model e Reports | `powerbi-authoring` |

---

## Arquitetura de Referência

```
Bronze Workspace          Silver Workspace          Gold Workspace
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Lakehouse Bronze│──────▶│ Lakehouse Silver│──────▶│ Lakehouse Gold  │
│ Files/raw/      │       │ Tables/         │       │ Tables/         │
│ Tables/         │       │  - dim_*        │       │  - agg_*        │
│  - raw_*        │       │  - fct_*        │       │  - kpi_*        │
└─────────────────┘       └─────────────────┘       └────────┬────────┘
                                                             │
                                                    ┌────────▼────────┐
                                                    │ Semantic Model  │
                                                    │ Reports Power BI│
                                                    └─────────────────┘
```

---

## Must / Prefer / Avoid

### MUST DO
- Criar **workspace separado** por camada (Bronze, Silver, Gold)
- Adicionar **colunas de metadados** no Bronze: `_ingestion_timestamp`, `_source_file`, `_batch_id`
- Aplicar **regras de qualidade** na transição Bronze → Silver: deduplicação, nulos, ranges
- Usar **Delta Lake** em todas as camadas
- Executar notebooks em sequência e verificar sucesso de cada etapa antes da próxima
- **Não parar na criação** — executar o fluxo completo: Bronze → Silver → Gold → Semantic Model

### PREFER
- Processamento incremental com watermark (evitar full-refresh em produção)
- ZORDER nas colunas de filtro mais frequentes nas tabelas Gold
- `OPTIMIZE` após writes em Silver e Gold
- Notebooks paramétricos (receber workspace_id e lakehouse_id via parâmetros)
- Validação de contagem de linhas entre camadas

### AVOID
- Todos os lakehouses no mesmo workspace (perde isolamento de governança)
- Pular a camada Silver e ir direto Bronze → Gold
- Hardcoded IDs em notebooks
- Ler arquivos de HTTP externo direto no Spark sem fazer upload primeiro
- Executar `VACUUM` sem verificar dependências do downstream

---

## Plano de Implementação Completo

### Fase 1: Infraestrutura (workspace-management + spark-authoring)
```
1. create_workspace("{projeto}-bronze-{env}", capacity_id)
2. create_workspace("{projeto}-silver-{env}", capacity_id)
3. create_workspace("{projeto}-gold-{env}", capacity_id)
4. create_lakehouse(bronze_workspace_id, "bronze", enable_schemas=true)
5. create_lakehouse(silver_workspace_id, "silver", enable_schemas=true)
6. create_lakehouse(gold_workspace_id, "gold", enable_schemas=true)
```

### Fase 2: Upload de dados raw (onelake)
```
7. create_folder(bronze_workspace_name, "bronze", "Files/raw/2026/04")
8. upload_file(bronze_workspace_name, "bronze", "Files/raw/2026/04/dados.parquet", local_path)
```

### Fase 3: Notebooks por camada (spark-authoring)
```
9. create_notebook(bronze_workspace_id, "nb_bronze_ingestao")
   → Lê Files/raw → limpa → grava em Tables/raw_* com metadados de ingestão

10. create_notebook(silver_workspace_id, "nb_silver_transformacao")
    → Lê Bronze via 3-part name → valida → deduplica → grava Tables/fct_* e Tables/dim_*

11. create_notebook(gold_workspace_id, "nb_gold_agregacao")
    → Lê Silver → agrega → ZORDER → OPTIMIZE → grava Tables/agg_* e Tables/kpi_*
```

### Fase 4: Pipeline de orquestração (spark-authoring)
```
12. create_pipeline(gold_workspace_id, "pipeline_medallion_completo")
    → Atividades: bronze_ingestao → silver_transformacao → gold_agregacao (encadeado)
```

### Fase 5: Executar e validar
```
13. run_pipeline(gold_workspace_id, pipeline_id)
14. get_job_status(gold_workspace_id, pipeline_id, job_instance_id) → polling
15. execute_sql via sqldw-consumption → validar contagem de linhas em cada camada
```

### Fase 6: Semantic Model e Reports (powerbi-authoring)
```
16. create_semantic_model(gold_workspace_id, "sm_{projeto}", definition_base64)
17. refresh_semantic_model(gold_workspace_id, model_id, "Full")
18. get_refresh_history → aguardar "Completed"
19. execute_dax → validar medidas principais
20. create_report(gold_workspace_id, "Dashboard {projeto}", definition_base64, model_id)
```

---

## Perfis Spark por Camada

```python
# Bronze — Write-heavy (ingestão)
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.sql.parquet.vorder.enabled", "false")

# Silver — Balanced
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Gold — Read-heavy (analytics)
spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
# Após writes:
# spark.sql("OPTIMIZE gold.kpi_vendas ZORDER BY (data, categoria)")
```

---

## Colunas de Metadados Bronze (obrigatórias)

```python
from pyspark.sql import functions as F
from datetime import datetime

df_bronze = df_raw.withColumns({
    "_ingestion_timestamp": F.lit(datetime.utcnow().isoformat()),
    "_source_file": F.input_file_name(),
    "_batch_id": F.lit(f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}")
})
```

---

## Checklist de Qualidade por Camada

| Verificação | Bronze | Silver | Gold |
|-------------|--------|--------|------|
| Schema consistente | ✓ enforce | ✓ strict | ✓ strict |
| Sem duplicatas | - | ✓ obrigatório | ✓ obrigatório |
| Sem nulos em PKs | - | ✓ obrigatório | ✓ obrigatório |
| Ranges válidos | - | ✓ validar | - |
| Contagem vs fonte | ✓ logar | ✓ validar | ✓ validar |
| OPTIMIZE executado | - | ✓ após write | ✓ após write |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
