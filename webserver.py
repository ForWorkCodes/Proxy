import logging
from aiohttp import web
from config import INTERNAL_API_TOKEN

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def handle_notify(request: web.Request) -> web.Response:
    bot = request.app['bot']

    # Проверка API-ключа
    api_key = request.headers.get("X-API-Key")
    if api_key != INTERNAL_API_TOKEN:
        logger.warning("Unauthorized request received")
        return web.json_response({'success': False, 'error': 'Unauthorized'}, status=401)

    # Парсинг JSON
    try:
        data = await request.json()
    except Exception:
        logger.exception("Invalid JSON")
        return web.json_response({'success': False, 'error': 'Invalid JSON'}, status=400)

    telegram_id = data.get('telegram_id') or data.get('user_id')
    text = data.get('text') or data.get('message')

    # Валидация данных
    if not telegram_id or not text or not isinstance(text, str):
        logger.warning("Missing or invalid fields")
        return web.json_response({'success': False, 'error': 'telegram_id and text are required'}, status=400)

    try:
        await bot.send_message(chat_id=int(telegram_id), text=text.strip())
        logger.info(f"Sent message to {telegram_id}")
        return web.json_response({'success': True})
    except Exception as e:
        logger.exception(f"Failed to send message to {telegram_id}")
        return web.json_response({'success': False, 'error': str(e)}, status=500)


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
