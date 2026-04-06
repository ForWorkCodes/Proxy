import importlib
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import web
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User


@asynccontextmanager
async def proxy_api_server(payload: dict, *, status: int = 200):
    captured = {}

    async def get_proxy_telegram_id(request: web.Request) -> web.StreamResponse:
        captured["method"] = request.method
        captured["path"] = request.path
        captured["headers"] = {
            "X-Internal-Token": request.headers.get("X-Internal-Token"),
        }
        captured["payload"] = await request.json()

        if status == 200:
            return web.json_response(payload)

        return web.Response(status=status, text="server error")

    app = web.Application()
    app.router.add_post("/get-proxy-telegram-id", get_proxy_telegram_id)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()

    port = site._server.sockets[0].getsockname()[1]
    try:
        yield {
            "base_url": f"http://127.0.0.1:{port}",
            "captured": captured,
        }
    finally:
        await runner.cleanup()


def reload_my_proxy_modules(monkeypatch: pytest.MonkeyPatch, *, api_base_url: str):
    monkeypatch.setenv("API_BASE_URL", api_base_url)
    monkeypatch.setenv("SERVER_BASE_URL", api_base_url)
    monkeypatch.setenv("INTERNAL_API_TOKEN", "test-token")

    import config
    import services.proxy_api_client as proxy_api_client_module
    import handlers.my_proxy as my_proxy_module

    importlib.reload(config)
    importlib.reload(proxy_api_client_module)
    importlib.reload(my_proxy_module)
    return my_proxy_module


def build_callback_and_state(language: str = "ru"):
    callback = AsyncMock(spec=CallbackQuery)
    callback.from_user = User(id=123, is_bot=False, first_name="Test")
    callback.message = AsyncMock(spec=Message)
    callback.message.answer = AsyncMock()
    callback.message.answer_document = AsyncMock()
    callback.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)
    state.get_data = AsyncMock(return_value={"user": {"language": language}})
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    return callback, state


def flatten_inline_callback_data(markup):
    return [
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if button.callback_data is not None
    ]


@pytest.mark.asyncio
async def test_my_proxy_happy_path_integration(monkeypatch):
    payload = {
        "success": True,
        "proxies": [
            {
                "ip": "1.2.3.4",
                "host": "1.2.3.4",
                "port": 8080,
                "type": "http",
                "version": "ipv4",
                "country": "us",
                "date": "2026-04-01T10:00:00",
                "date_end": "2026-05-01T10:00:00",
                "unixtime": 1711965600,
                "unixtime_end": 1714557600,
                "descr": None,
                "active": True,
                "auto_prolong": True,
                "login_proxy": "login1",
                "pass_proxy": "pass1",
            }
        ],
    }

    async with proxy_api_server(payload) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    captured = server["captured"]
    assert captured["method"] == "POST"
    assert captured["path"] == "/get-proxy-telegram-id"
    assert captured["headers"]["X-Internal-Token"] == "test-token"
    assert captured["payload"] == {"telegram_id": "123"}

    assert callback.message.answer.await_count == 3

    count_call = callback.message.answer.await_args_list[0]
    assert count_call.args[0] == "У тебя есть прокси в количестве: 1"

    proxy_call = callback.message.answer.await_args_list[1]
    proxy_text = proxy_call.args[0]
    assert "<b>IP: </b>1.2.3.4:8080" in proxy_text
    assert "<b>Тип: </b>HTTP" in proxy_text
    assert "<b>Версия: </b>ipv4" in proxy_text
    assert "<b>Страна: </b>США" in proxy_text
    assert "<b>Логин: </b>login1" in proxy_text
    assert "<b>Пароль: </b>pass1" in proxy_text
    assert "<b>Срок до: </b>01.05.2026 10:00" in proxy_text
    assert "<b>Автопродление: </b>Да" in proxy_text
    assert proxy_call.kwargs["parse_mode"] == "HTML"

    menu_call = callback.message.answer.await_args_list[2]
    assert menu_call.kwargs["text"] == "Мои прокси"

    markup = menu_call.kwargs["reply_markup"]
    callback_data = flatten_inline_callback_data(markup)
    button_texts = [button.text for row in markup.inline_keyboard for button in row]

    assert "download_proxies_csv" in callback_data
    assert "download_proxies_xls" in callback_data
    assert "cancel_proxy" in callback_data
    assert "enable_auto_prolong" not in callback_data
    assert "Купить прокси?" in button_texts
    assert "🔙 Назад" in button_texts
    assert "main_menu_btn" in callback_data


@pytest.mark.asyncio
async def test_my_proxy_empty_response_2001_returns_empty_menu(monkeypatch):
    payload = {
        "success": False,
        "status_code": 2001,
        "error": "No proxies",
        "proxies": [],
    }

    async with proxy_api_server(payload) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    assert callback.message.answer.await_count == 2
    assert callback.message.answer.await_args_list[0].args[0] == "У тебя есть прокси в количестве: 0"
    final_call = callback.message.answer.await_args_list[1]
    assert final_call.kwargs["text"] == "У вас нет прокси"

    markup = final_call.kwargs["reply_markup"]
    callback_data = flatten_inline_callback_data(markup)
    assert callback_data == ["buy_proxy", "main_menu_btn"]


@pytest.mark.asyncio
async def test_my_proxy_server_error_falls_back_to_api_error(monkeypatch):
    payload = {"success": False, "status_code": 500, "error": "boom", "proxies": []}

    async with proxy_api_server(payload, status=500) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    assert callback.message.answer.await_count == 2
    assert callback.message.answer.await_args_list[0].args[0] == "У тебя есть прокси в количестве: 0"
    assert callback.message.answer.await_args_list[1].kwargs["text"] == "❗ Ошибка при подключении к серверу. Попробуйте позже"


@pytest.mark.asyncio
async def test_my_proxy_network_error_falls_back_to_api_error(monkeypatch, unused_tcp_port):
    unused_base_url = f"http://127.0.0.1:{unused_tcp_port}"
    my_proxy_module = reload_my_proxy_modules(
        monkeypatch,
        api_base_url=unused_base_url,
    )

    callback, state = build_callback_and_state()

    with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
        await my_proxy_module.my_proxy(callback, state)

    assert callback.message.answer.await_count == 2
    assert callback.message.answer.await_args_list[0].args[0] == "У тебя есть прокси в количестве: 0"
    assert callback.message.answer.await_args_list[1].kwargs["text"] == "❗ Ошибка при подключении к серверу. Попробуйте позже"


@pytest.mark.asyncio
async def test_my_proxy_mixed_auto_prolong_shows_both_action_buttons(monkeypatch):
    payload = {
        "success": True,
        "proxies": [
            {
                "ip": "1.2.3.4",
                "host": "1.2.3.4",
                "port": 8080,
                "type": "http",
                "version": "ipv4",
                "country": "us",
                "date": "2026-04-01T10:00:00",
                "date_end": "2026-05-01T10:00:00",
                "unixtime": 1711965600,
                "unixtime_end": 1714557600,
                "descr": None,
                "active": True,
                "auto_prolong": True,
                "login_proxy": "login1",
                "pass_proxy": "pass1",
            },
            {
                "ip": "5.6.7.8",
                "host": "5.6.7.8",
                "port": 9090,
                "type": "http",
                "version": "ipv4",
                "country": "de",
                "date": "2026-04-02T10:00:00",
                "date_end": "2026-05-02T10:00:00",
                "unixtime": 1712052000,
                "unixtime_end": 1714644000,
                "descr": None,
                "active": True,
                "auto_prolong": False,
                "login_proxy": "login2",
                "pass_proxy": "pass2",
            },
        ],
    }

    async with proxy_api_server(payload) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    menu_call = callback.message.answer.await_args_list[-1]
    callback_data = flatten_inline_callback_data(menu_call.kwargs["reply_markup"])
    assert "cancel_proxy" in callback_data
    assert "enable_auto_prolong" in callback_data


@pytest.mark.asyncio
async def test_my_proxy_all_true_hides_enable_button(monkeypatch):
    payload = {
        "success": True,
        "proxies": [
            {
                "ip": "1.2.3.4",
                "host": "1.2.3.4",
                "port": 8080,
                "type": "http",
                "version": "ipv4",
                "country": "us",
                "date": "2026-04-01T10:00:00",
                "date_end": "2026-05-01T10:00:00",
                "unixtime": 1711965600,
                "unixtime_end": 1714557600,
                "descr": None,
                "active": True,
                "auto_prolong": True,
                "login_proxy": "login1",
                "pass_proxy": "pass1",
            }
        ],
    }

    async with proxy_api_server(payload) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    menu_call = callback.message.answer.await_args_list[-1]
    callback_data = flatten_inline_callback_data(menu_call.kwargs["reply_markup"])
    assert "cancel_proxy" in callback_data
    assert "enable_auto_prolong" not in callback_data


@pytest.mark.asyncio
async def test_my_proxy_all_false_hides_cancel_button(monkeypatch):
    payload = {
        "success": True,
        "proxies": [
            {
                "ip": "5.6.7.8",
                "host": "5.6.7.8",
                "port": 9090,
                "type": "http",
                "version": "ipv4",
                "country": "de",
                "date": "2026-04-02T10:00:00",
                "date_end": "2026-05-02T10:00:00",
                "unixtime": 1712052000,
                "unixtime_end": 1714644000,
                "descr": None,
                "active": True,
                "auto_prolong": False,
                "login_proxy": "login2",
                "pass_proxy": "pass2",
            }
        ],
    }

    async with proxy_api_server(payload) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    menu_call = callback.message.answer.await_args_list[-1]
    callback_data = flatten_inline_callback_data(menu_call.kwargs["reply_markup"])
    assert "cancel_proxy" not in callback_data
    assert "enable_auto_prolong" in callback_data


@pytest.mark.asyncio
async def test_my_proxy_unknown_country_falls_back_to_country_code(monkeypatch):
    payload = {
        "success": True,
        "proxies": [
            {
                "ip": "9.9.9.9",
                "host": "9.9.9.9",
                "port": 9999,
                "type": "http",
                "version": "ipv4",
                "country": "xx",
                "date": "2026-04-03T10:00:00",
                "date_end": "2026-05-03T10:00:00",
                "unixtime": 1712138400,
                "unixtime_end": 1714730400,
                "descr": None,
                "active": True,
                "auto_prolong": True,
                "login_proxy": "login3",
                "pass_proxy": "pass3",
            }
        ],
    }

    async with proxy_api_server(payload) as server:
        my_proxy_module = reload_my_proxy_modules(
            monkeypatch,
            api_base_url=server["base_url"],
        )

        callback, state = build_callback_and_state()

        with patch.object(my_proxy_module, "safe_delete_message", new=AsyncMock()):
            await my_proxy_module.my_proxy(callback, state)

    proxy_text = callback.message.answer.await_args_list[1].args[0]
    assert "<b>Страна: </b>XX" in proxy_text
