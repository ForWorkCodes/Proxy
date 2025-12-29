from __future__ import annotations

import json
import logging
from typing import Dict

from aiohttp import web

from config import INTERNAL_API_TOKEN
from data.locales import get_text_by_land
from dtos.notification_dto import IncomingNotification, NotificationData
from enums.notification_type import NotificationType

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _build_notification_text(payload: NotificationData, locale_texts: Dict[str, str]) -> str:
    template_key = f"notification_{payload.type.value}"
    template = locale_texts.get(template_key)

    if payload.type == NotificationType.admin_alert:
        base_line = template
        extras = payload.extras["data"]
        if extras["reason"] == "notification_delivery_failed":
            base_line += " Ошибка доставки сообщения " + extras["notification_type"] + ". Пользователю " + str(extras["user_id"])
        if extras["reason"] == "proxy_purchase_insufficient_funds":
            base_line += " Ошибка покупки прокси: " + extras["details"] + ". Пользователю " + str(extras["requested_by"])

        return base_line

    if payload.type == NotificationType.balance_low:
        base_line = template
        return base_line

    if payload.type == NotificationType.proxy_expiring or payload.type == NotificationType.proxy_expired:
        base_line = payload.message or template
        if not base_line:
            raise ValueError("Missing message template for proxy_expiring notification")

        parts = [base_line.strip()]
        if payload.host:
            proxy_label = locale_texts.get("proxy:", "Proxy:")
            parts.append(f"{proxy_label} {payload.host}")
        return "\n".join(part for part in parts if part).strip()

    if payload.message:
        return payload.message

    if template:
        return template.strip()

    raise ValueError("Notification message is empty")


async def handle_notify(request: web.Request) -> web.Response:
    bot = request.app['bot']

    api_key = request.headers.get("X-API-Key")
    if api_key != INTERNAL_API_TOKEN:
        logger.warning("Unauthorized request received")
        return web.json_response({'success': False, 'error': 'Unauthorized'}, status=401)

    try:
        raw_payload = await request.json()
    except json.JSONDecodeError:
        logger.warning("Invalid JSON payload received")
        return web.json_response({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception:
        logger.exception("Unexpected error while parsing JSON payload")
        return web.json_response({'success': False, 'error': 'Invalid JSON'}, status=400)

    try:
        notification = IncomingNotification.from_mapping(raw_payload)
    except ValueError as error:
        logger.warning("Invalid notification payload: %s", error)
        return web.json_response({'success': False, 'error': str(error)}, status=400)

    locale_texts = get_text_by_land(notification.payload.language)
    try:
        text = _build_notification_text(notification.payload, locale_texts)
    except ValueError as error:
        logger.warning("Failed to compose notification text: %s", error)
        return web.json_response({'success': False, 'error': str(error)}, status=400)

    try:
        await bot.send_message(chat_id=notification.telegram_id, text=text)
    except Exception as error:
        logger.exception("Failed to send message to %s", notification.telegram_id)
        return web.json_response({'success': False, 'error': str(error)}, status=500)

    logger.info("Sent message to %s", notification.telegram_id)
    return web.json_response({'success': True})


async def start_webserver(bot, host: str = '0.0.0.0', port: int = 8081):
    app = web.Application()
    app['bot'] = bot
    app.router.add_post('/notify', handle_notify)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    logger.info(f"Notify server started on http://{host}:{port}")
    return runner
