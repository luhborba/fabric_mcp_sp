import pyodbc
import struct
from mcp.types import Tool
from client import fabric
from auth import token_manager
from config import settings

TOOLS = [
    Tool(name="list_warehouses", description="Lista todos os warehouses de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_warehouse", description="Retorna metadados de um warehouse.", inputSchema={"type": "object", "required": ["workspace_id", "warehouse_id"], "properties": {"workspace_id": {"type": "string"}, "warehouse_id": {"type": "string"}}}),
    Tool(name="create_warehouse", description="Cria um novo Fabric Data Warehouse.", inputSchema={"type": "object", "required": ["workspace_id", "display_name"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}}),
    Tool(name="delete_warehouse", description="Deleta um warehouse. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "warehouse_id"], "properties": {"workspace_id": {"type": "string"}, "warehouse_id": {"type": "string"}}}),
    Tool(name="execute_sql", description="Executa T-SQL em um Fabric Warehouse via TDS. Retorna até 10.000 linhas.", inputSchema={"type": "object", "required": ["workspace_id", "warehouse_id", "sql"], "properties": {"workspace_id": {"type": "string"}, "warehouse_id": {"type": "string"}, "sql": {"type": "string"}}}),
]


async def _list_warehouses(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/warehouses")
    return {"success": True, "data": data.get("value", [])}


async def _get_warehouse(args: dict) -> dict:
    wid, whid = args["workspace_id"], args["warehouse_id"]
    data = await fabric.get(f"/workspaces/{wid}/warehouses/{whid}")
    return {"success": True, "data": data}


async def _create_warehouse(args: dict) -> dict:
    wid = args["workspace_id"]
    body = {"displayName": args["display_name"], "type": "Warehouse"}
    if args.get("description"):
        body["description"] = args["description"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    return {"success": True, "data": data}


async def _delete_warehouse(args: dict) -> dict:
    wid, whid = args["workspace_id"], args["warehouse_id"]
    await fabric.delete(f"/workspaces/{wid}/warehouses/{whid}")
    return {"success": True, "message": f"Warehouse {whid} deletado."}


async def _execute_sql(args: dict) -> dict:
    wid, whid = args["workspace_id"], args["warehouse_id"]

    # Obter connection string do warehouse
    wh_data = await fabric.get(f"/workspaces/{wid}/warehouses/{whid}")
    conn_string = wh_data.get("properties", {}).get("connectionString")
    if not conn_string:
        # Montar endpoint padrão se não disponível via API
        conn_string = f"{whid}.datawarehouse.fabric.microsoft.com"

    # Token para SQL (audience: database.windows.net)
    token = await token_manager.get_token("https://database.windows.net/.default")
    token_bytes = token.encode("UTF-16-LE")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

    odbc_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={conn_string},1433;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

    import asyncio
    loop = asyncio.get_event_loop()

    def _run_query():
        conn = pyodbc.connect(odbc_str, attrs_before={1256: token_struct})
        cursor = conn.cursor()
        cursor.execute(args["sql"])
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            rows = [list(row) for row in cursor.fetchmany(10000)]
            conn.close()
            return {"columns": columns, "rows": rows, "row_count": len(rows)}
        conn.commit()
        conn.close()
        return {"rows_affected": cursor.rowcount}

    result = await loop.run_in_executor(None, _run_query)
    return {"success": True, "data": result}


HANDLERS = {
    "list_warehouses": _list_warehouses,
    "get_warehouse": _get_warehouse,
    "create_warehouse": _create_warehouse,
    "delete_warehouse": _delete_warehouse,
    "execute_sql": _execute_sql,
}
