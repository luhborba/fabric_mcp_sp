import httpx
from mcp.types import Tool
from client import fabric
from config import settings

TOOLS = [
    Tool(name="list_notebooks", description="Lista todos os notebooks de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_notebook", description="Retorna metadados de um notebook.", inputSchema={"type": "object", "required": ["workspace_id", "notebook_id"], "properties": {"workspace_id": {"type": "string"}, "notebook_id": {"type": "string"}}}),
    Tool(name="create_notebook", description="Cria um novo notebook no workspace.", inputSchema={"type": "object", "required": ["workspace_id", "display_name"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="update_notebook", description="Atualiza nome ou descrição de um notebook.", inputSchema={"type": "object", "required": ["workspace_id", "notebook_id"], "properties": {"workspace_id": {"type": "string"}, "notebook_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}}),
    Tool(name="delete_notebook", description="Deleta um notebook. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "notebook_id"], "properties": {"workspace_id": {"type": "string"}, "notebook_id": {"type": "string"}}}),
    Tool(name="get_notebook_definition", description="Retorna o conteúdo do notebook em base64 (.ipynb).", inputSchema={"type": "object", "required": ["workspace_id", "notebook_id"], "properties": {"workspace_id": {"type": "string"}, "notebook_id": {"type": "string"}}}),
    Tool(name="update_notebook_definition", description="Atualiza o conteúdo de um notebook com definição .ipynb em base64.", inputSchema={"type": "object", "required": ["workspace_id", "notebook_id", "definition"], "properties": {"workspace_id": {"type": "string"}, "notebook_id": {"type": "string"}, "definition": {"type": "object", "description": "Objeto com format e parts (payload base64)"}}}),
    Tool(name="run_notebook", description="Executa um notebook. Retorna job_instance_id. Use get_job_status (em pipelines) com item_id=notebook_id para acompanhar.", inputSchema={"type": "object", "required": ["workspace_id", "notebook_id"], "properties": {"workspace_id": {"type": "string"}, "notebook_id": {"type": "string"}, "parameters": {"type": "object"}}}),
]


async def _list_notebooks(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/notebooks")
    return {"success": True, "data": data.get("value", [])}


async def _get_notebook(args: dict) -> dict:
    wid, nid = args["workspace_id"], args["notebook_id"]
    data = await fabric.get(f"/workspaces/{wid}/notebooks/{nid}")
    return {"success": True, "data": data}


async def _create_notebook(args: dict) -> dict:
    wid = args["workspace_id"]
    body: dict = {"displayName": args["display_name"], "type": "Notebook"}
    if args.get("description"):
        body["description"] = args["description"]
    if args.get("definition"):
        body["definition"] = args["definition"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    # Fabric pode retornar 201 com body vazio — confirma via list
    if data is None:
        notebooks = await fabric.get(f"/workspaces/{wid}/notebooks")
        created = next(
            (n for n in notebooks.get("value", []) if n.get("displayName") == args["display_name"]),
            None,
        )
        return {"success": True, "data": created, "message": "Notebook criado (sem body na resposta — confirmado via list)."}
    return {"success": True, "data": data}


async def _update_notebook(args: dict) -> dict:
    wid, nid = args["workspace_id"], args["notebook_id"]
    body = {}
    if args.get("display_name"):
        body["displayName"] = args["display_name"]
    if args.get("description") is not None:
        body["description"] = args["description"]
    await fabric.patch(f"/workspaces/{wid}/notebooks/{nid}", json=body)
    return {"success": True, "message": f"Notebook {nid} atualizado."}


async def _delete_notebook(args: dict) -> dict:
    wid, nid = args["workspace_id"], args["notebook_id"]
    await fabric.delete(f"/workspaces/{wid}/notebooks/{nid}")
    return {"success": True, "message": f"Notebook {nid} deletado."}


async def _get_notebook_definition(args: dict) -> dict:
    wid, nid = args["workspace_id"], args["notebook_id"]
    # LRO: POST getDefinition
    resp = await fabric.request(
        "POST",
        f"{settings.api_base_url}/workspaces/{wid}/notebooks/{nid}/getDefinition?format=ipynb",
        json={},
    )
    if resp is None:
        return {"success": True, "data": None, "message": "Sem conteúdo retornado."}
    # Se retornou 202, fazer polling
    if isinstance(resp, dict) and resp.get("status") == "Running":
        location = resp.get("Location") or resp.get("location")
        if location:
            result = await fabric.poll_lro(location)
            return {"success": True, "data": result.get("definition")}
    return {"success": True, "data": resp.get("definition", resp)}


async def _update_notebook_definition(args: dict) -> dict:
    wid, nid = args["workspace_id"], args["notebook_id"]
    body = {"definition": args["definition"]}
    resp = await fabric.post(f"/workspaces/{wid}/notebooks/{nid}/updateDefinition", json=body)
    return {"success": True, "message": f"Definição do notebook {nid} atualizada.", "data": resp}


async def _run_notebook(args: dict) -> dict:
    wid, nid = args["workspace_id"], args["notebook_id"]
    body: dict = {"executionData": {}}
    if args.get("parameters"):
        body["executionData"]["parameters"] = args["parameters"]
    resp = await fabric.post(f"/workspaces/{wid}/items/{nid}/jobs/instances?jobType=RunNotebook", json=body)
    job_id = (resp or {}).get("id") if resp else None
    return {
        "success": True,
        "job_instance_id": job_id,
        "message": "Notebook em execução. Use get_job_status para acompanhar.",
    }


HANDLERS = {
    "list_notebooks": _list_notebooks,
    "get_notebook": _get_notebook,
    "create_notebook": _create_notebook,
    "update_notebook": _update_notebook,
    "delete_notebook": _delete_notebook,
    "get_notebook_definition": _get_notebook_definition,
    "update_notebook_definition": _update_notebook_definition,
    "run_notebook": _run_notebook,
}
