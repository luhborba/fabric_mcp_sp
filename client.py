import asyncio
import logging
from typing import Any
import httpx
from config import settings
from auth import token_manager
from exceptions import (
    AuthError,
    FabricAPIError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ValidationError,
    OperationTimeoutError,
)

logger = logging.getLogger(__name__)

RETRY_STATUSES = {429, 503}
MAX_RETRIES = 3


class FabricClient:
    """HTTP client para a Fabric REST API com retry e mapeamento de erros."""

    def __init__(self):
        self._client = httpx.AsyncClient(timeout=settings.request_timeout)

    async def _headers(self, scope: str = None) -> dict:
        token = await token_manager.get_token(scope)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def request(
        self,
        method: str,
        url: str,
        scope: str = None,
        **kwargs,
    ) -> dict | None:
        headers = await self._headers(scope)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await self._client.request(
                    method, url, headers=headers, **kwargs
                )
            except httpx.TimeoutException:
                raise FabricAPIError(
                    f"Timeout na requisição {method} {url}",
                    suggestion="Aumente FABRIC_REQUEST_TIMEOUT no .env",
                )

            if resp.status_code in RETRY_STATUSES and attempt < MAX_RETRIES:
                wait = 2 ** attempt
                logger.warning("HTTP %s — retry %d/%d em %ds", resp.status_code, attempt, MAX_RETRIES, wait)
                await asyncio.sleep(wait)
                headers = await self._headers(scope)  # renova token em retry
                continue

            self._raise_for_status(resp)

            if resp.status_code == 202:
                # LRO: retorna body + location para o caller fazer polling se necessário
                location = resp.headers.get("Location") or resp.headers.get("location")
                body = resp.json() if resp.content else {}
                if location:
                    body["_lro_location"] = location
                return body or None

            if resp.status_code == 204 or not resp.content:
                return None
            return resp.json()

    async def get(self, path: str, **kwargs) -> dict:
        return await self.request("GET", f"{settings.api_base_url}{path}", **kwargs)

    async def post(self, path: str, **kwargs) -> dict | None:
        return await self.request("POST", f"{settings.api_base_url}{path}", **kwargs)

    async def patch(self, path: str, **kwargs) -> dict | None:
        return await self.request("PATCH", f"{settings.api_base_url}{path}", **kwargs)

    async def delete(self, path: str, **kwargs) -> None:
        await self.request("DELETE", f"{settings.api_base_url}{path}", **kwargs)

    async def poll_lro(self, location: str, operation_id: str = "") -> dict:
        """Faz polling de Long-Running Operations até status terminal."""
        deadline = asyncio.get_event_loop().time() + settings.operation_timeout
        poll_interval = 5

        while asyncio.get_event_loop().time() < deadline:
            await asyncio.sleep(poll_interval)
            headers = await self._headers()
            resp = await self._client.get(location, headers=headers)
            self._raise_for_status(resp)

            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status", "").lower()
                if status in ("succeeded", "completed"):
                    return data
                if status in ("failed", "cancelled"):
                    error_msg = data.get("error", {}).get("message", "Operação falhou")
                    raise FabricAPIError(
                        f"Operação falhou: {error_msg}",
                        details=str(data.get("error", "")),
                    )
            poll_interval = min(poll_interval * 1.5, 30)

        raise OperationTimeoutError(
            f"Operação excedeu timeout de {settings.operation_timeout}s.",
            suggestion="Aumente FABRIC_OPERATION_TIMEOUT no .env ou verifique a operação manualmente.",
        )

    def _raise_for_status(self, resp: httpx.Response) -> None:
        if resp.status_code < 400:
            return
        try:
            body = resp.json()
            msg = body.get("message") or body.get("error", {}).get("message", resp.text)
        except Exception:
            msg = resp.text

        if resp.status_code == 400:
            raise ValidationError(msg, details=f"HTTP 400 — {resp.url}")
        if resp.status_code == 401:
            raise AuthError(msg, suggestion="Verifique as credenciais do Service Principal.")
        if resp.status_code == 403:
            raise PermissionError(
                msg,
                details=f"HTTP 403 — {resp.url}",
                suggestion="Verifique o role do Service Principal no workspace.",
            )
        if resp.status_code == 404:
            raise NotFoundError(
                msg,
                details=f"HTTP 404 — {resp.url}",
                suggestion="Use list_* para obter IDs válidos.",
            )
        if resp.status_code == 429:
            raise RateLimitError(msg, suggestion="Aguarde e tente novamente.")
        raise FabricAPIError(msg, details=f"HTTP {resp.status_code} — {resp.url}")


fabric = FabricClient()
