from mcp.types import Tool
from client import fabric

TOOLS = [
    Tool(name="list_lakehouses", description="Lista todos os lakehouses de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_lakehouse", description="Retorna metadados de um lakehouse específico.", inputSchema={"type": "object", "required": ["workspace_id", "lakehouse_id"], "properties": {"workspace_id": {"type": "string"}, "lakehouse_id": {"type": "string"}}}),
    Tool(name="create_lakehouse", description="Cria um novo lakehouse no workspace.", inputSchema={"type": "object", "required": ["workspace_id", "display_name"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "enable_schemas": {"type": "boolean", "default": True}}}),
    Tool(name="delete_lakehouse", description="Deleta um lakehouse. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "lakehouse_id"], "properties": {"workspace_id": {"type": "string"}, "lakehouse_id": {"type": "string"}}}),
    Tool(name="list_lakehouse_tables", description="Lista as tabelas Delta de um lakehouse.", inputSchema={"type": "object", "required": ["workspace_id", "lakehouse_id"], "properties": {"workspace_id": {"type": "string"}, "lakehouse_id": {"type": "string"}}}),
    Tool(name="load_table", description="Registra um arquivo do OneLake como tabela Delta.", inputSchema={"type": "object", "required": ["workspace_id", "lakehouse_id", "table_name", "path_type", "relative_path", "format"], "properties": {"workspace_id": {"type": "string"}, "lakehouse_id": {"type": "string"}, "table_name": {"type": "string"}, "path_type": {"type": "string", "enum": ["File", "Folder"]}, "relative_path": {"type": "string"}, "format": {"type": "string", "enum": ["Csv", "Parquet", "Delta"]}, "header": {"type": "boolean"}}}),
    Tool(name="run_table_maintenance", description="Executa OPTIMIZE e/ou VACUUM em uma tabela Delta.", inputSchema={"type": "object", "required": ["workspace_id", "lakehouse_id", "table_name"], "properties": {"workspace_id": {"type": "string"}, "lakehouse_id": {"type": "string"}, "table_name": {"type": "string"}, "optimize": {"type": "boolean", "default": True}, "vacuum_retention_hours": {"type": "integer", "minimum": 168}}}),
]


async def _list_lakehouses(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/lakehouses")
    return {"success": True, "data": data.get("value", [])}


async def _get_lakehouse(args: dict) -> dict:
    wid, lid = args["workspace_id"], args["lakehouse_id"]
    data = await fabric.get(f"/workspaces/{wid}/lakehouses/{lid}")
    return {"success": True, "data": data}


async def _create_lakehouse(args: dict) -> dict:
    wid = args["workspace_id"]
    enable_schemas = args.get("enable_schemas", True)
    body = {
        "displayName": args["display_name"],
        "type": "Lakehouse",
        "creationPayload": {"enableSchemas": enable_schemas},
    }
    if args.get("description"):
        body["description"] = args["description"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    if data is None:
        lakehouses = await fabric.get(f"/workspaces/{wid}/lakehouses")
        created = next(
            (lh for lh in lakehouses.get("value", []) if lh.get("displayName") == args["display_name"]),
            None,
        )
        return {"success": True, "data": created, "message": "Lakehouse criado (sem body na resposta — confirmado via list)."}
    return {"success": True, "data": data}


async def _delete_lakehouse(args: dict) -> dict:
    wid, lid = args["workspace_id"], args["lakehouse_id"]
    await fabric.delete(f"/workspaces/{wid}/lakehouses/{lid}")
    return {"success": True, "message": f"Lakehouse {lid} deletado."}


async def _list_lakehouse_tables(args: dict) -> dict:
    wid, lid = args["workspace_id"], args["lakehouse_id"]
    data = await fabric.get(f"/workspaces/{wid}/lakehouses/{lid}/tables")
    return {"success": True, "data": data.get("data", [])}


async def _load_table(args: dict) -> dict:
    wid, lid = args["workspace_id"], args["lakehouse_id"]
    table = args["table_name"]
    body = {
        "relativePath": args["relative_path"],
        "pathType": args["path_type"],
        "format": args["format"],
    }
    if "header" in args:
        body["header"] = args["header"]
    resp = await fabric.post(f"/workspaces/{wid}/lakehouses/{lid}/tables/{table}/load", json=body)
    return {"success": True, "data": resp, "message": f"Tabela '{table}' carregada."}


async def _run_table_maintenance(args: dict) -> dict:
    wid, lid = args["workspace_id"], args["lakehouse_id"]
    table = args["table_name"]
    body: dict = {}
    if args.get("optimize", True):
        body["optimizeSettings"] = {"vOrder": True}
    if args.get("vacuum_retention_hours"):
        body["vacuumSettings"] = {"retentionPeriod": f"{args['vacuum_retention_hours']}:00:00"}
    resp = await fabric.post(f"/workspaces/{wid}/lakehouses/{lid}/tables/{table}/maintenance", json=body)
    return {"success": True, "data": resp, "message": f"Manutenção iniciada para tabela '{table}'."}


HANDLERS = {
    "list_lakehouses": _list_lakehouses,
    "get_lakehouse": _get_lakehouse,
    "create_lakehouse": _create_lakehouse,
    "delete_lakehouse": _delete_lakehouse,
    "list_lakehouse_tables": _list_lakehouse_tables,
    "load_table": _load_table,
    "run_table_maintenance": _run_table_maintenance,
}
