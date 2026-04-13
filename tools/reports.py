from mcp.types import Tool
from client import fabric

TOOLS = [
    Tool(name="list_reports", description="Lista todos os reports de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_report", description="Retorna metadados de um report.", inputSchema={"type": "object", "required": ["workspace_id", "report_id"], "properties": {"workspace_id": {"type": "string"}, "report_id": {"type": "string"}}}),
    Tool(name="create_report", description="Cria um report a partir de definição .pbir em base64.", inputSchema={"type": "object", "required": ["workspace_id", "display_name", "definition"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="delete_report", description="Deleta um report. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "report_id"], "properties": {"workspace_id": {"type": "string"}, "report_id": {"type": "string"}}}),
    Tool(name="get_report_definition", description="Retorna a definição .pbir do report em base64.", inputSchema={"type": "object", "required": ["workspace_id", "report_id"], "properties": {"workspace_id": {"type": "string"}, "report_id": {"type": "string"}}}),
    Tool(name="update_report_definition", description="Atualiza o conteúdo de um report com nova definição.", inputSchema={"type": "object", "required": ["workspace_id", "report_id", "definition"], "properties": {"workspace_id": {"type": "string"}, "report_id": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="clone_report", description="Clona um report para o mesmo workspace ou outro.", inputSchema={"type": "object", "required": ["workspace_id", "report_id", "new_name"], "properties": {"workspace_id": {"type": "string"}, "report_id": {"type": "string"}, "new_name": {"type": "string"}, "target_workspace_id": {"type": "string"}, "target_model_id": {"type": "string"}}}),
    Tool(name="export_report", description="Exporta um report como PDF, PPTX, PNG, CSV ou XLSX.", inputSchema={"type": "object", "required": ["workspace_id", "report_id", "format"], "properties": {"workspace_id": {"type": "string"}, "report_id": {"type": "string"}, "format": {"type": "string", "enum": ["PDF", "PPTX", "PNG", "CSV", "XLSX"]}, "pages": {"type": "array", "items": {"type": "string"}}}}),
]


async def _list_reports(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/reports")
    return {"success": True, "data": data.get("value", [])}


async def _get_report(args: dict) -> dict:
    wid, rid = args["workspace_id"], args["report_id"]
    data = await fabric.get(f"/workspaces/{wid}/reports/{rid}")
    return {"success": True, "data": data}


async def _create_report(args: dict) -> dict:
    wid = args["workspace_id"]
    body: dict = {
        "displayName": args["display_name"],
        "type": "Report",
        "definition": args["definition"],
    }
    if args.get("description"):
        body["description"] = args["description"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    return {"success": True, "data": data}


async def _delete_report(args: dict) -> dict:
    wid, rid = args["workspace_id"], args["report_id"]
    await fabric.delete(f"/workspaces/{wid}/reports/{rid}")
    return {"success": True, "message": f"Report {rid} deletado."}


async def _get_report_definition(args: dict) -> dict:
    wid, rid = args["workspace_id"], args["report_id"]
    resp = await fabric.post(f"/workspaces/{wid}/reports/{rid}/getDefinition", json={})
    return {"success": True, "data": resp}


async def _update_report_definition(args: dict) -> dict:
    wid, rid = args["workspace_id"], args["report_id"]
    body = {"definition": args["definition"]}
    resp = await fabric.post(f"/workspaces/{wid}/reports/{rid}/updateDefinition", json=body)
    return {"success": True, "message": f"Report {rid} atualizado.", "data": resp}


async def _clone_report(args: dict) -> dict:
    wid, rid = args["workspace_id"], args["report_id"]
    body: dict = {"name": args["new_name"]}
    if args.get("target_workspace_id"):
        body["targetWorkspaceId"] = args["target_workspace_id"]
    if args.get("target_model_id"):
        body["targetModelId"] = args["target_model_id"]
    data = await fabric.request(
        "POST",
        f"https://api.powerbi.com/v1.0/myorg/groups/{wid}/reports/{rid}/Clone",
        json=body,
    )
    return {"success": True, "data": data}


async def _export_report(args: dict) -> dict:
    wid, rid = args["workspace_id"], args["report_id"]
    body: dict = {"format": args["format"]}
    if args.get("pages"):
        body["paginatedReportConfiguration"] = {"pages": [{"pageName": p} for p in args["pages"]]}
    resp = await fabric.request(
        "POST",
        f"https://api.powerbi.com/v1.0/myorg/groups/{wid}/reports/{rid}/ExportTo",
        json=body,
    )
    export_id = (resp or {}).get("id")
    return {
        "success": True,
        "export_id": export_id,
        "message": f"Exportação iniciada (formato: {args['format']}). ID: {export_id}",
        "data": resp,
    }


HANDLERS = {
    "list_reports": _list_reports,
    "get_report": _get_report,
    "create_report": _create_report,
    "delete_report": _delete_report,
    "get_report_definition": _get_report_definition,
    "update_report_definition": _update_report_definition,
    "clone_report": _clone_report,
    "export_report": _export_report,
}
