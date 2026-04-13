from mcp.types import Tool
from client import fabric
from config import settings

TOOLS = [
    Tool(name="list_semantic_models", description="Lista todos os semantic models de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_semantic_model", description="Retorna metadados de um semantic model.", inputSchema={"type": "object", "required": ["workspace_id", "model_id"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}}}),
    Tool(name="create_semantic_model", description="Cria um semantic model a partir de definição BIM/TMDL em base64.", inputSchema={"type": "object", "required": ["workspace_id", "display_name", "definition"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="delete_semantic_model", description="Deleta um semantic model. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "model_id"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}}}),
    Tool(name="get_semantic_model_definition", description="Retorna a definição BIM/TMDL do modelo em base64.", inputSchema={"type": "object", "required": ["workspace_id", "model_id"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}}}),
    Tool(name="update_semantic_model_definition", description="Atualiza a definição do modelo com novo BIM/TMDL.", inputSchema={"type": "object", "required": ["workspace_id", "model_id", "definition"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="refresh_semantic_model", description="Dispara refresh do semantic model. Operação assíncrona.", inputSchema={"type": "object", "required": ["workspace_id", "model_id"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}, "refresh_type": {"type": "string", "enum": ["Full", "ClearValues", "Calculate", "DataOnly", "Automatic"], "default": "Full"}}}),
    Tool(name="get_refresh_history", description="Retorna histórico de refreshes do semantic model.", inputSchema={"type": "object", "required": ["workspace_id", "model_id"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}, "top": {"type": "integer", "default": 10}}}),
    Tool(name="execute_dax", description="Executa uma query DAX em um semantic model.", inputSchema={"type": "object", "required": ["workspace_id", "model_id", "query"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}, "query": {"type": "string"}}}),
    Tool(name="get_datasources", description="Lista os datasources configurados em um semantic model.", inputSchema={"type": "object", "required": ["workspace_id", "model_id"], "properties": {"workspace_id": {"type": "string"}, "model_id": {"type": "string"}}}),
]


async def _list_semantic_models(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/semanticModels")
    return {"success": True, "data": data.get("value", [])}


async def _get_semantic_model(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    data = await fabric.get(f"/workspaces/{wid}/semanticModels/{mid}")
    return {"success": True, "data": data}


async def _create_semantic_model(args: dict) -> dict:
    wid = args["workspace_id"]
    body: dict = {
        "displayName": args["display_name"],
        "type": "SemanticModel",
        "definition": args["definition"],
    }
    if args.get("description"):
        body["description"] = args["description"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    return {"success": True, "data": data}


async def _delete_semantic_model(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    await fabric.delete(f"/workspaces/{wid}/semanticModels/{mid}")
    return {"success": True, "message": f"Semantic Model {mid} deletado."}


async def _get_semantic_model_definition(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    resp = await fabric.post(f"/workspaces/{wid}/semanticModels/{mid}/getDefinition", json={})
    return {"success": True, "data": resp}


async def _update_semantic_model_definition(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    body = {"definition": args["definition"]}
    resp = await fabric.post(f"/workspaces/{wid}/semanticModels/{mid}/updateDefinition", json=body)
    return {"success": True, "message": f"Definição do modelo {mid} atualizada.", "data": resp}


async def _refresh_semantic_model(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    refresh_type = args.get("refresh_type", "Full")
    # API Power BI REST para refresh
    body = {"notifyOption": "NoNotification", "type": refresh_type}
    resp = await fabric.request(
        "POST",
        f"https://api.powerbi.com/v1.0/myorg/groups/{wid}/datasets/{mid}/refreshes",
        json=body,
    )
    return {
        "success": True,
        "message": f"Refresh '{refresh_type}' disparado. Use get_refresh_history para acompanhar.",
        "data": resp,
    }


async def _get_refresh_history(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    top = args.get("top", 10)
    data = await fabric.request(
        "GET",
        f"https://api.powerbi.com/v1.0/myorg/groups/{wid}/datasets/{mid}/refreshes?$top={top}",
    )
    return {"success": True, "data": (data or {}).get("value", [])}


async def _execute_dax(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    body = {"queries": [{"query": args["query"]}], "serializerSettings": {"includeNulls": True}}
    data = await fabric.request(
        "POST",
        f"https://api.powerbi.com/v1.0/myorg/groups/{wid}/datasets/{mid}/executeQueries",
        json=body,
    )
    results = (data or {}).get("results", [])
    tables = results[0].get("tables", []) if results else []
    return {"success": True, "data": tables}


async def _get_datasources(args: dict) -> dict:
    wid, mid = args["workspace_id"], args["model_id"]
    data = await fabric.request(
        "GET",
        f"https://api.powerbi.com/v1.0/myorg/groups/{wid}/datasets/{mid}/datasources",
    )
    return {"success": True, "data": (data or {}).get("value", [])}


HANDLERS = {
    "list_semantic_models": _list_semantic_models,
    "get_semantic_model": _get_semantic_model,
    "create_semantic_model": _create_semantic_model,
    "delete_semantic_model": _delete_semantic_model,
    "get_semantic_model_definition": _get_semantic_model_definition,
    "update_semantic_model_definition": _update_semantic_model_definition,
    "refresh_semantic_model": _refresh_semantic_model,
    "get_refresh_history": _get_refresh_history,
    "execute_dax": _execute_dax,
    "get_datasources": _get_datasources,
}
