import asyncio
from pathlib import Path
from mcp.types import Tool
from azure.storage.filedatalake.aio import DataLakeServiceClient
from auth import token_manager
from config import settings

TOOLS = [
    Tool(name="list_onelake_files", description="Lista arquivos e pastas no OneLake (pasta Files/ do lakehouse).", inputSchema={"type": "object", "required": ["workspace_name", "lakehouse_name"], "properties": {"workspace_name": {"type": "string"}, "lakehouse_name": {"type": "string"}, "path": {"type": "string", "default": ""}}}),
    Tool(name="upload_file", description="Faz upload de um arquivo local para o OneLake.", inputSchema={"type": "object", "required": ["workspace_name", "lakehouse_name", "destination_path", "local_path"], "properties": {"workspace_name": {"type": "string"}, "lakehouse_name": {"type": "string"}, "destination_path": {"type": "string"}, "local_path": {"type": "string"}}}),
    Tool(name="download_file", description="Baixa um arquivo do OneLake para o sistema local.", inputSchema={"type": "object", "required": ["workspace_name", "lakehouse_name", "source_path", "local_path"], "properties": {"workspace_name": {"type": "string"}, "lakehouse_name": {"type": "string"}, "source_path": {"type": "string"}, "local_path": {"type": "string"}}}),
    Tool(name="delete_onelake_file", description="Deleta um arquivo ou pasta no OneLake.", inputSchema={"type": "object", "required": ["workspace_name", "lakehouse_name", "path"], "properties": {"workspace_name": {"type": "string"}, "lakehouse_name": {"type": "string"}, "path": {"type": "string"}}}),
    Tool(name="create_folder", description="Cria uma pasta no OneLake.", inputSchema={"type": "object", "required": ["workspace_name", "lakehouse_name", "folder_path"], "properties": {"workspace_name": {"type": "string"}, "lakehouse_name": {"type": "string"}, "folder_path": {"type": "string"}}}),
    Tool(name="get_file_properties", description="Retorna metadados de um arquivo no OneLake (tamanho, data).", inputSchema={"type": "object", "required": ["workspace_name", "lakehouse_name", "path"], "properties": {"workspace_name": {"type": "string"}, "lakehouse_name": {"type": "string"}, "path": {"type": "string"}}}),
]

# OneLake endpoint: {workspace_name}.dfs.fabric.microsoft.com
# Filesystem = lakehouse_name.Lakehouse


def _adls_url(workspace_name: str) -> str:
    safe = workspace_name.replace(" ", "%20")
    return f"https://{safe}.dfs.fabric.microsoft.com"


def _filesystem(lakehouse_name: str) -> str:
    return f"{lakehouse_name}.Lakehouse"


async def _get_client(workspace_name: str) -> DataLakeServiceClient:
    token = await token_manager.get_token(settings.storage_scope)
    from azure.core.credentials import AccessToken
    import time

    class _StaticCred:
        def get_token(self, *scopes, **kw):
            return AccessToken(token, int(time.time()) + 3000)

    return DataLakeServiceClient(account_url=_adls_url(workspace_name), credential=_StaticCred())


async def _list_onelake_files(args: dict) -> dict:
    ws, lh = args["workspace_name"], args["lakehouse_name"]
    path = args.get("path", "")
    async with await _get_client(ws) as client:
        fs = client.get_file_system_client(_filesystem(lh))
        items = []
        async for item in fs.get_paths(path=path or None, recursive=False):
            items.append({
                "name": item.name,
                "is_directory": item.is_directory,
                "size": item.content_length,
                "last_modified": str(item.last_modified),
            })
    return {"success": True, "data": items}


async def _upload_file(args: dict) -> dict:
    ws, lh = args["workspace_name"], args["lakehouse_name"]
    dest = args["destination_path"]
    local = args["local_path"]
    async with await _get_client(ws) as client:
        fs = client.get_file_system_client(_filesystem(lh))
        file_client = fs.get_file_client(dest)
        with open(local, "rb") as f:
            data = f.read()
        await file_client.upload_data(data, overwrite=True)
    return {"success": True, "message": f"Arquivo '{local}' enviado para '{dest}'."}


async def _download_file(args: dict) -> dict:
    ws, lh = args["workspace_name"], args["lakehouse_name"]
    src = args["source_path"]
    local = args["local_path"]
    async with await _get_client(ws) as client:
        fs = client.get_file_system_client(_filesystem(lh))
        file_client = fs.get_file_client(src)
        download = await file_client.download_file()
        data = await download.readall()
    Path(local).parent.mkdir(parents=True, exist_ok=True)
    with open(local, "wb") as f:
        f.write(data)
    return {"success": True, "message": f"Arquivo salvo em '{local}' ({len(data)} bytes)."}


async def _delete_onelake_file(args: dict) -> dict:
    ws, lh = args["workspace_name"], args["lakehouse_name"]
    path = args["path"]
    async with await _get_client(ws) as client:
        fs = client.get_file_system_client(_filesystem(lh))
        await fs.delete_file(path)
    return {"success": True, "message": f"'{path}' deletado."}


async def _create_folder(args: dict) -> dict:
    ws, lh = args["workspace_name"], args["lakehouse_name"]
    folder = args["folder_path"]
    async with await _get_client(ws) as client:
        fs = client.get_file_system_client(_filesystem(lh))
        await fs.create_directory(folder)
    return {"success": True, "message": f"Pasta '{folder}' criada."}


async def _get_file_properties(args: dict) -> dict:
    ws, lh = args["workspace_name"], args["lakehouse_name"]
    path = args["path"]
    async with await _get_client(ws) as client:
        fs = client.get_file_system_client(_filesystem(lh))
        file_client = fs.get_file_client(path)
        props = await file_client.get_file_properties()
    return {
        "success": True,
        "data": {
            "name": props.name,
            "size": props.size,
            "last_modified": str(props.last_modified),
            "content_type": props.content_settings.content_type,
        },
    }


HANDLERS = {
    "list_onelake_files": _list_onelake_files,
    "upload_file": _upload_file,
    "download_file": _download_file,
    "delete_onelake_file": _delete_onelake_file,
    "create_folder": _create_folder,
    "get_file_properties": _get_file_properties,
}
