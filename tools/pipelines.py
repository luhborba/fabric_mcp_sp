from mcp.types import Tool
from client import fabric
from config import settings

TOOLS = [
    Tool(name="list_pipelines", description="Lista todos os data pipelines de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_pipeline", description="Retorna metadados de um pipeline.", inputSchema={"type": "object", "required": ["workspace_id", "pipeline_id"], "properties": {"workspace_id": {"type": "string"}, "pipeline_id": {"type": "string"}}}),
    Tool(name="create_pipeline", description="Cria um novo data pipeline no workspace.", inputSchema={"type": "object", "required": ["workspace_id", "display_name"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="delete_pipeline", description="Deleta um pipeline. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "pipeline_id"], "properties": {"workspace_id": {"type": "string"}, "pipeline_id": {"type": "string"}}}),
    Tool(name="run_pipeline", description="Executa um pipeline. Retorna job_instance_id para polling.", inputSchema={"type": "object", "required": ["workspace_id", "pipeline_id"], "properties": {"workspace_id": {"type": "string"}, "pipeline_id": {"type": "string"}}}),
    Tool(name="get_job_status", description="Retorna o status de um job (notebook, pipeline, spark job).", inputSchema={"type": "object", "required": ["workspace_id", "item_id", "job_instance_id"], "properties": {"workspace_id": {"type": "string"}, "item_id": {"type": "string"}, "job_instance_id": {"type": "string"}}}),
]


async def _list_pipelines(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/dataPipelines")
    return {"success": True, "data": data.get("value", [])}


async def _get_pipeline(args: dict) -> dict:
    wid, pid = args["workspace_id"], args["pipeline_id"]
    data = await fabric.get(f"/workspaces/{wid}/dataPipelines/{pid}")
    return {"success": True, "data": data}


async def _create_pipeline(args: dict) -> dict:
    wid = args["workspace_id"]
    body: dict = {"displayName": args["display_name"], "type": "DataPipeline"}
    if args.get("description"):
        body["description"] = args["description"]
    if args.get("definition"):
        body["definition"] = args["definition"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    return {"success": True, "data": data}


async def _delete_pipeline(args: dict) -> dict:
    wid, pid = args["workspace_id"], args["pipeline_id"]
    await fabric.delete(f"/workspaces/{wid}/dataPipelines/{pid}")
    return {"success": True, "message": f"Pipeline {pid} deletado."}


async def _run_pipeline(args: dict) -> dict:
    wid, pid = args["workspace_id"], args["pipeline_id"]
    resp = await fabric.post(f"/workspaces/{wid}/items/{pid}/jobs/instances?jobType=Pipeline", json={})
    job_id = (resp or {}).get("id") if resp else None
    return {
        "success": True,
        "job_instance_id": job_id,
        "message": "Pipeline em execução. Use get_job_status para acompanhar.",
    }


async def _get_job_status(args: dict) -> dict:
    wid = args["workspace_id"]
    item_id = args["item_id"]
    job_id = args["job_instance_id"]
    data = await fabric.get(f"/workspaces/{wid}/items/{item_id}/jobs/instances/{job_id}")
    return {"success": True, "data": data}


HANDLERS = {
    "list_pipelines": _list_pipelines,
    "get_pipeline": _get_pipeline,
    "create_pipeline": _create_pipeline,
    "delete_pipeline": _delete_pipeline,
    "run_pipeline": _run_pipeline,
    "get_job_status": _get_job_status,
}
