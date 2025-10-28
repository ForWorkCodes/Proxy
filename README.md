# Telegram Proxy Bot
Бот для покупки и управления прокси. Поддерживает многоязычное меню, PostgreSQL и пул соединений.

## 📦 Возможности

- Команда `/start` с автоопределением языка
- Inline-меню и Reply-клавиатура

## 🚀 Установка

1. Клонируй репозиторий.
2. Установи зависимости:
pip install -r requirements.txt
3. Создай .env файл:
BOT_TOKEN=your_bot_token_here
4. Запусти бота:
python main.py

## 🔔 Server notifications

The bot starts a lightweight HTTP server (port `8081` by default) that allows
your backend to push messages to users. See
[`docs/server_notifications.md`](docs/server_notifications.md) for the payload
schema and integration details.

## ⚙️ Требования

- Python 3.12+
- PostgreSQL 17+

## 🛠 Настройка базы данных PostgreSQL

CREATE TABLE users_telegram (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language VARCHAR(5),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT now() NOT NULL,
    updated_at TIMESTAMP DEFAULT now() NOT NULL
);

Для дебага на сервере  docker compose logs -f bot
