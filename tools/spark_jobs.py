from mcp.types import Tool
from client import fabric

TOOLS = [
    Tool(name="list_spark_jobs", description="Lista todos os Spark Job Definitions de um workspace.", inputSchema={"type": "object", "required": ["workspace_id"], "properties": {"workspace_id": {"type": "string"}}}),
    Tool(name="get_spark_job", description="Retorna metadados de um Spark Job Definition.", inputSchema={"type": "object", "required": ["workspace_id", "job_id"], "properties": {"workspace_id": {"type": "string"}, "job_id": {"type": "string"}}}),
    Tool(name="create_spark_job", description="Cria um novo Spark Job Definition.", inputSchema={"type": "object", "required": ["workspace_id", "display_name"], "properties": {"workspace_id": {"type": "string"}, "display_name": {"type": "string"}, "description": {"type": "string"}, "definition": {"type": "object"}}}),
    Tool(name="delete_spark_job", description="Deleta um Spark Job Definition. IRREVERSÍVEL.", inputSchema={"type": "object", "required": ["workspace_id", "job_id"], "properties": {"workspace_id": {"type": "string"}, "job_id": {"type": "string"}}}),
    Tool(name="run_spark_job", description="Executa um Spark Job Definition. Retorna job_instance_id.", inputSchema={"type": "object", "required": ["workspace_id", "job_id"], "properties": {"workspace_id": {"type": "string"}, "job_id": {"type": "string"}}}),
]


async def _list_spark_jobs(args: dict) -> dict:
    wid = args["workspace_id"]
    data = await fabric.get(f"/workspaces/{wid}/sparkJobDefinitions")
    return {"success": True, "data": data.get("value", [])}


async def _get_spark_job(args: dict) -> dict:
    wid, jid = args["workspace_id"], args["job_id"]
    data = await fabric.get(f"/workspaces/{wid}/sparkJobDefinitions/{jid}")
    return {"success": True, "data": data}


async def _create_spark_job(args: dict) -> dict:
    wid = args["workspace_id"]
    body: dict = {"displayName": args["display_name"], "type": "SparkJobDefinition"}
    if args.get("description"):
        body["description"] = args["description"]
    if args.get("definition"):
        body["definition"] = args["definition"]
    data = await fabric.post(f"/workspaces/{wid}/items", json=body)
    return {"success": True, "data": data}


async def _delete_spark_job(args: dict) -> dict:
    wid, jid = args["workspace_id"], args["job_id"]
    await fabric.delete(f"/workspaces/{wid}/sparkJobDefinitions/{jid}")
    return {"success": True, "message": f"Spark Job {jid} deletado."}


async def _run_spark_job(args: dict) -> dict:
    wid, jid = args["workspace_id"], args["job_id"]
    resp = await fabric.post(f"/workspaces/{wid}/items/{jid}/jobs/instances?jobType=SparkJobDefinitionV1", json={})
    job_id = (resp or {}).get("id") if resp else None
    return {
        "success": True,
        "job_instance_id": job_id,
        "message": "Spark Job em execução. Use get_job_status para acompanhar.",
    }


HANDLERS = {
    "list_spark_jobs": _list_spark_jobs,
    "get_spark_job": _get_spark_job,
    "create_spark_job": _create_spark_job,
    "delete_spark_job": _delete_spark_job,
    "run_spark_job": _run_spark_job,
}
