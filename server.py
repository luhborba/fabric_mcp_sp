"""
fabric-mcp — MCP Server para Microsoft Fabric via Service Principal
Transporte: stdio
"""
import asyncio
import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from config import settings
from exceptions import FabricMCPError

# Importa todos os módulos de tools
from tools import (
    workspaces,
    lakehouses,
    warehouses,
    notebooks,
    pipelines,
    spark_jobs,
    semantic_models,
    reports,
    onelake,
)

logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

app = Server("fabric-mcp")

# ─── Registro de todas as tools ────────────────────────────────────────────────

ALL_TOOLS: list[Tool] = (
    workspaces.TOOLS
    + lakehouses.TOOLS
    + warehouses.TOOLS
    + notebooks.TOOLS
    + pipelines.TOOLS
    + spark_jobs.TOOLS
    + semantic_models.TOOLS
    + reports.TOOLS
    + onelake.TOOLS
)

TOOL_HANDLERS = {
    **workspaces.HANDLERS,
    **lakehouses.HANDLERS,
    **warehouses.HANDLERS,
    **notebooks.HANDLERS,
    **pipelines.HANDLERS,
    **spark_jobs.HANDLERS,
    **semantic_models.HANDLERS,
    **reports.HANDLERS,
    **onelake.HANDLERS,
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    return ALL_TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": {"code": "UNKNOWN_TOOL", "message": f"Tool '{name}' não encontrada."},
        }))]
    try:
        result = await handler(arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, default=str))]
    except FabricMCPError as e:
        return [TextContent(type="text", text=json.dumps(e.to_dict(), ensure_ascii=False))]
    except Exception as e:
        logger.exception("Erro inesperado na tool %s", name)
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": {"code": "INTERNAL_ERROR", "message": str(e)},
        }))]


async def main():
    logger.info("fabric-mcp iniciando (tenant: %s)", settings.tenant_id)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
