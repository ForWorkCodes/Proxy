from webserver import handle_notify
import pytest
from unittest.mock import AsyncMock
from aiohttp.test_utils import TestClient, TestServer
from aiohttp import web
import os
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "test-key")


@pytest.mark.asyncio
async def test_handle_notify_success():
    bot = AsyncMock()
    app = web.Application()
    app['bot'] = bot
    app.router.add_post('/notify', handle_notify)
    server = TestServer(app)
    client = TestClient(server)
    await client.start_server()

    headers = {'X-API-Key': INTERNAL_API_TOKEN}
    payload = {'telegram_id': 1, 'text': 'hi'}

    resp = await client.post('/notify', json=payload, headers=headers)

    assert resp.status == 200
    data = await resp.json()
    assert data['success'] is True
    bot.send_message.assert_awaited_once_with(chat_id=1, text='hi')

    await client.close()
