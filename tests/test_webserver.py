import pytest
from unittest.mock import AsyncMock
from aiohttp.test_utils import TestClient, TestServer
from aiohttp import web

from webserver import start_webserver, handle_notify

@pytest.mark.asyncio
async def test_handle_notify_success():
    bot = AsyncMock()
    app = web.Application()
    app['bot'] = bot
    app.router.add_post('/notify', handle_notify)
    server = TestServer(app)
    client = TestClient(server)
    await client.start_server()
    resp = await client.post('/notify', json={'telegram_id': 1, 'text': 'hi'})
    assert resp.status == 200
    data = await resp.json()
    assert data['success'] is True
    bot.send_message.assert_awaited_once_with(chat_id=1, text='hi')
    await client.close()
