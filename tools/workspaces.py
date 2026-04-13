from mcp.types import Tool
from client import fabric
from exceptions import ValidationError

# ─── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    Tool(name="list_workspaces", description="Lista todos os workspaces do tenant Fabric.", inputSchema={"type": "object", "properties": {}}),
    Tool(name="get_workspace", description="Retorna metadados de um workspace específico.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="create_workspace", description="Cria um novo workspace no Fabric.", inputSchema={"type": "object", "required": ["display_name"], "properties": {"display_name": {"type": "string"}, "description": {"type": "string"}, "capacity_id": {"type": "string"}}}),
    Tool(name="update_workspace", description="Atualiza nome ou descrição de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}}}),
    Tool(name="delete_workspace", description="Deleta um workspace. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="assign_to_capacity", description="Atribui um workspace a uma capacidade Fabric.", inputSchema={"type": "object", "required": ["workspace_id", "capacity_id"], "properties": {"workspace_id": {"type": "string"}, "capacity_id": {"type": "string"}}}),
    Tool(name="list_role_assignments", description="Lista os role assignments de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="add_role_assignment", description="Adiciona um role assignment a um workspace.", inputSchema={"type": "object", "required": ["workspace_id", "principal_id", "principal_type", "role"], "properties": {"workspace_id": {"type": "string"}, "principal_id": {"type": "string"}, "principal_type": {"type": "string", "enum": ["User", "Group", "ServicePrincipal"]}, "role": {"type": "string", "enum": ["Admin", "Member", "Contributor", "Viewer"]}}}),
]

# ─── Handlers ──────────────────────────────────────────────────────────────────

async def _list_workspaces(args: dict) -> dict:
    data = await fabric.get("/workspaces")
    return {"success": True, "data": data.get("value", [])}


async def _get_workspace(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}")
    return {"success": True, "data": data}


async def _create_workspace(args: dict) -> dict:
    body = {"displayName": args["display_name"]}
    if args.get("description"):
        body["description"] = args["description"]
    if args.get("capacity_id"):
        body["capacityId"] = args["capacity_id"]
    data = await fabric.post("/workspaces", json=body)
    return {"success": True, "data": data}


async def _update_workspace(args: dict) -> dict:
    wid = args["workspace_id"]
    body = {}
    if args.get("display_name"):
        body["displayName"] = args["display_name"]
    if args.get("description") is not None:
        body["description"] = args["description"]
    if not body:
        raise ValidationError("Nenhum campo para atualizar.")
    await fabric.patch(f"/workspaces/{wid}", json=body)
    return {"success": True, "message": f"Workspace {wid} atualizado."}


async def _delete_workspace(args: dict) -> dict:
    wid = args["workspace_id"]
    await fabric.delete(f"/workspaces/{wid}")
    return {"success": True, "message": f"Workspace {wid} deletado."}


async def _assign_to_capacity(args: dict) -> dict:
    wid = args["workspace_id"]
    body = {"capacityId": args["capacity_id"]}
    await fabric.post(f"/workspaces/{wid}/assignToCapacity", json=body)
    return {"success": True, "message": f"Workspace {wid} atribuído à capacidade {args['capacity_id']}."}


async def _list_role_assignments(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/roleAssignments")
    return {"success": True, "data": data.get("value", [])}


async def _add_role_assignment(args: dict) -> dict:
    wid = args["workspace_id"]
    body = {
        "principal": {"id": args["principal_id"], "type": args["principal_type"]},
        "role": args["role"],
    }
    await fabric.post(f"/workspaces/{wid}/roleAssignments", json=body)
    return {"success": True, "message": f"Role {args['role']} adicionado para {args['principal_id']}."}


HANDLERS = {
    "list_workspaces": _list_workspaces,
    "get_workspace": _get_workspace,
    "create_workspace": _create_workspace,
    "update_workspace": _update_workspace,
    "delete_workspace": _delete_workspace,
    "assign_to_capacity": _assign_to_capacity,
    "list_role_assignments": _list_role_assignments,
    "add_role_assignment": _add_role_assignment,
}
