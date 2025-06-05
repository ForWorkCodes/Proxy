from aiohttp import web

async def handle_notify(request: web.Request) -> web.Response:
    """Handle incoming notifications from external server."""
    bot = request.app['bot']
    try:
        data = await request.json()
    except Exception:
        return web.json_response({'success': False, 'error': 'Invalid JSON'}, status=400)

    telegram_id = data.get('telegram_id') or data.get('user_id')
    text = data.get('text') or data.get('message')
    if not telegram_id or not text:
        return web.json_response({'success': False, 'error': 'telegram_id and text are required'}, status=400)

    await bot.send_message(chat_id=int(telegram_id), text=text)
    return web.json_response({'success': True})

async def start_webserver(bot, host: str = '0.0.0.0', port: int = 8080):
    """Start aiohttp web server for external callbacks."""
    app = web.Application()
    app['bot'] = bot
    app.router.add_post('/notify', handle_notify)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=host, port=port)
    await site.start()
    return runner
