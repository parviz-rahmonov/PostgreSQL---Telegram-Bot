# Simple Telegram Bot (aiogram 3 + PostgreSQL)

Учебный Telegram-бот на Python. Один файл, без классов, FSM и middleware — только основы.

## Возможности

- `/start` — сохраняет пользователя в PostgreSQL (если его ещё нет) и приветствует
- `/users` — список всех пользователей из базы
- `/count` — количество пользователей

## Стек

- Python 3.10+
- [aiogram 3](https://docs.aiogram.dev/)
- [asyncpg](https://github.com/MagicStack/asyncpg)
- PostgreSQL

## Установка

\`\`\`bash
git clone <ссылка на репозиторий>
cd <папка проекта>
pip install aiogram asyncpg
\`\`\`

## Настройка

Открой `main.py` и укажи в начале файла:

\`\`\`python
TOKEN = "..."         # токен бота от @BotFather
DB_NAME = "..."
DB_USER = "..."
DB_PASSWORD = "..."
DB_HOST = "localhost"
DB_PORT = "5432"
\`\`\`

Таблица `users` создастся автоматически при первом запуске.

## Запуск

\`\`\`bash
python3 main.py
\`\`\`

## Структура БД

| Поле        | Тип    | Описание                    |
|-------------|--------|------------------------------|
| id          | SERIAL | Первичный ключ               |
| telegram_id | BIGINT | ID пользователя в Telegram   |
| full_name   | TEXT   | Имя пользователя              |
