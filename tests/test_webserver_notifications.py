import importlib
import json
from dataclasses import dataclass
from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest


def reload_webserver(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("INTERNAL_API_TOKEN", "test-token")
    import config
    import webserver

    importlib.reload(config)
    importlib.reload(webserver)
    return webserver


@dataclass
class StubRequest:
    app: Dict[str, Any]
    headers: Dict[str, str]
    payload: Dict[str, Any]

    async def json(self) -> Dict[str, Any]:
        return self.payload


@pytest.mark.asyncio
async def test_notify_proxy_expiring(monkeypatch):
    webserver = reload_webserver(monkeypatch)
    bot = AsyncMock()
    app = {"bot": bot}

    request = StubRequest(
        app=app,
        headers={"X-API-Key": "test-token"},
        payload={
            "telegram_id": 101,
            "data": {
                "language": "ru",
                "type": "proxy_expiring",
                "host": "1.2.3.4:5678",
            },
        },
    )

    response = await webserver.handle_notify(request)
    assert response.status == 200
    body = json.loads(response.text)
    assert body["success"] is True

    bot.send_message.assert_awaited_once()
    await_event = bot.send_message.await_args
    assert await_event.kwargs["chat_id"] == 101
    assert "1.2.3.4:5678" in await_event.kwargs["text"]


@pytest.mark.asyncio
async def test_notify_requires_authorization(monkeypatch):
    webserver = reload_webserver(monkeypatch)
    bot = AsyncMock()
    app = {"bot": bot}

    request = StubRequest(
        app=app,
        headers={},
        payload={
            "telegram_id": 101,
            "data": {
                "language": "ru",
                "type": "balance_low",
                "message": "Top up",
            },
        },
    )

    response = await webserver.handle_notify(request)
    assert response.status == 401
    bot.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_notify_balance_low_uses_locale(monkeypatch):
    webserver = reload_webserver(monkeypatch)
    bot = AsyncMock()
    app = {"bot": bot}

    request = StubRequest(
        app=app,
        headers={"X-API-Key": "test-token"},
        payload={
            "telegram_id": 202,
            "data": {
                "language": "en",
                "type": "balance_low",
            },
        },
    )

    response = await webserver.handle_notify(request)
    assert response.status == 200

    bot.send_message.assert_awaited_once()
    await_event = bot.send_message.await_args
    assert await_event.kwargs["chat_id"] == 202
    assert await_event.kwargs["text"].startswith("Your balance is running low")
