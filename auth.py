import asyncio
import logging
import time
from msal import ConfidentialClientApplication
from config import settings
from exceptions import AuthError

logger = logging.getLogger(__name__)


class TokenManager:
    """Gerencia tokens OAuth2 via Service Principal com cache e auto-refresh."""

    def __init__(self):
        self._app = ConfidentialClientApplication(
            client_id=settings.client_id,
            client_credential=settings.client_secret,
            authority=f"https://login.microsoftonline.com/{settings.tenant_id}",
        )
        self._cache: dict[str, dict] = {}
        self._lock = asyncio.Lock()

    async def get_token(self, scope: str = None) -> str:
        scope = scope or settings.fabric_scope
        async with self._lock:
            cached = self._cache.get(scope)
            # Renova 5 minutos antes de expirar
            if cached and cached["expires_at"] > time.time() + 300:
                return cached["token"]
            return await self._acquire(scope)

    async def _acquire(self, scope: str) -> str:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self._app.acquire_token_for_client(scopes=[scope]),
        )
        if "access_token" not in result:
            error = result.get("error_description", result.get("error", "unknown"))
            raise AuthError(
                message="Falha ao obter token do Azure AD.",
                details=error,
                suggestion="Verifique FABRIC_TENANT_ID, FABRIC_CLIENT_ID e FABRIC_CLIENT_SECRET no .env",
            )
        expires_in = result.get("expires_in", 3600)
        self._cache[scope] = {
            "token": result["access_token"],
            "expires_at": time.time() + expires_in,
        }
        logger.debug("Token obtido para scope %s (expira em %ds)", scope, expires_in)
        return result["access_token"]


token_manager = TokenManager()
