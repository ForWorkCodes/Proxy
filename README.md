# Telegram Proxy Bot
Бот для покупки и управления прокси. Поддерживает многоязычное меню, PostgreSQL и пул соединений.

## 📦 Возможности

- Команда `/start` с автоопределением языка
- Inline-меню и Reply-клавиатура
- Смена языка с сохранением в БД
- Хранение профиля пользователя: ID, имя, username, язык
- Асинхронная работа с PostgreSQL через `asyncpg` + пул

## 🚀 Установка

1. Клонируй репозиторий.
2. Установи зависимости:
pip install -r requirements.txt
3. Создай .env файл:
BOT_TOKEN=your_bot_token_here
POSTGRES_DSN=postgresql://user:pass@localhost:port/dbname
4. Запусти бота:
python main.py

## ⚙️ Требования

- Python 3.11+
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