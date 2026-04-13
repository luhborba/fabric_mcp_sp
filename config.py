import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória não definida: {key}")
    return value


class Settings:
    tenant_id: str = _require("FABRIC_TENANT_ID")
    client_id: str = _require("FABRIC_CLIENT_ID")
    client_secret: str = _require("FABRIC_CLIENT_SECRET")

    api_base_url: str = os.getenv("FABRIC_API_BASE_URL", "https://api.fabric.microsoft.com/v1")
    default_workspace_id: str | None = os.getenv("FABRIC_DEFAULT_WORKSPACE_ID")
    request_timeout: int = int(os.getenv("FABRIC_REQUEST_TIMEOUT", "60"))
    operation_timeout: int = int(os.getenv("FABRIC_OPERATION_TIMEOUT", "300"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    fabric_scope: str = "https://api.fabric.microsoft.com/.default"
    storage_scope: str = "https://storage.azure.com/.default"


settings = Settings()
