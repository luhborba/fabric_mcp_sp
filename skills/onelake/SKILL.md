---
name: onelake
description: >
  Gerenciar arquivos e pastas no OneLake (ADLS Gen2) de lakehouses do Fabric via MCP.
  Use quando o usuário quiser: fazer upload de arquivos, listar arquivos, baixar arquivos,
  criar estrutura de pastas, deletar arquivos, preparar arquivos para ingestão no lakehouse.
  Triggers: "upload arquivo", "listar arquivos OneLake", "criar pasta", "baixar arquivo",
  "estrutura Files", "preparar ingestão", "arquivo CSV/Parquet no lakehouse".
---

# OneLake — MCP Skill

> **REGRA CRÍTICA**: Tools OneLake usam **workspace_name** e **lakehouse_name** (nomes, não IDs).
> **REGRA**: Arquivos na pasta `Files/` são raw storage. Arquivos na pasta `Tables/` são gerenciados pelo Delta Engine — não manipule `Tables/` diretamente.

## Referência de Tools

`SDD.md § 6.9 (OneLake)`. Parâmetros: `skills/fabric-mcp/SKILL.md § ONELAKE`.

---

## Estrutura do OneLake

```
{workspace_name}/
└── {lakehouse_name}.Lakehouse/
    ├── Files/                 ← upload/download aqui (raw storage)
    │   ├── raw/               ← dados brutos (CSV, JSON, Parquet)
    │   ├── processed/         ← arquivos processados
    │   └── temp/              ← staging temporário
    └── Tables/                ← NÃO MANIPULAR DIRETAMENTE
        └── {table_name}/      ← gerenciado pelo Delta Engine
```

---

## Must / Prefer / Avoid

### MUST DO
- Usar `workspace_name` e `lakehouse_name` (strings), não IDs, nas tools OneLake
- Fazer upload para `Files/` (nunca `Tables/`)
- Verificar com `list_onelake_files` antes de `upload_file` para evitar sobrescrever

### PREFER
- Estrutura de pastas com particionamento por data: `Files/raw/2026/04/10/`
- Nomes de arquivo com timestamp: `vendas_20260409_143000.parquet`
- `create_folder` para criar hierarquia antes de `upload_file`

### AVOID
- Escrever diretamente na pasta `Tables/` — corromperia tabelas Delta
- Nomes de pasta com espaços ou caracteres especiais
- Arquivos muito grandes (> 500MB) em upload único — fragmentar em partes

---

## Fluxos Comuns

### Preparar estrutura e fazer upload para ingestão
```
1. list_workspaces() → obter workspace_name
2. list_lakehouses(workspace_id) → confirmar lakehouse_name
3. create_folder(workspace_name, lakehouse_name, "Files/raw/2026/04")
4. upload_file(workspace_name, lakehouse_name, "Files/raw/2026/04/dados.parquet", local_path)
5. list_onelake_files(workspace_name, lakehouse_name, "Files/raw/2026/04") → confirmar upload
6. → Chamar load_table() ou create_notebook() para ingerir no Delta
```

### Listar e inspecionar arquivos
```
1. list_onelake_files(workspace_name, lakehouse_name, "Files/") → estrutura raiz
2. list_onelake_files(workspace_name, lakehouse_name, "Files/raw/") → arquivos raw
3. get_file_properties(workspace_name, lakehouse_name, "Files/raw/dados.parquet") → size, lastModified
```

### Baixar arquivo para inspeção local
```
1. list_onelake_files(workspace_name, lakehouse_name, "Files/raw/")
2. download_file(workspace_name, lakehouse_name, "Files/raw/dados.csv", "C:/temp/dados.csv")
```

---

## Gotchas

| Problema | Causa | Solução |
|---------|-------|---------|
| `upload_file` retorna 403 | SP sem permissão no workspace | Verificar role — precisa de Member ou Contributor |
| `list_onelake_files` retorna vazio | Pasta não existe | Criar com `create_folder` primeiro |
| Tabela não aparece após upload | Arquivo em `Files/`, não registrado como tabela | Usar `load_table` para registrar como tabela Delta |
| Arquivo corrompido após download | Encoding binary vs text | Garantir modo binário no download |

---

**Version:** 1.0.0 | **Data:** 2026-04-09
