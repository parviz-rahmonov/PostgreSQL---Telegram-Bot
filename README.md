# Telegram User Bot

Минималистичный Telegram-бот на **aiogram 3** с асинхронным хранением пользователей в **PostgreSQL**. Реализован в одном файле без излишней архитектуры — удобен как учебный пример или стартовая точка для собственного проекта.

## Стек технологий

| Компонент | Версия / Библиотека |
|---|---|
| Язык | Python 3.10+ |
| Telegram Framework | [aiogram 3](https://docs.aiogram.dev/) |
| База данных | PostgreSQL |
| Драйвер БД | [asyncpg](https://github.com/MagicStack/asyncpg) |

## Функциональность

| Команда | Описание |
|---|---|
| `/start` | Регистрирует пользователя в базе данных (если он ещё не зарегистрирован) и отправляет приветствие |
| `/users` | Выводит список всех зарегистрированных пользователей |
| `/count` | Показывает общее количество пользователей в базе |

## Требования

- Python 3.10 или новее
- Доступный сервер PostgreSQL
- Токен Telegram-бота ([@BotFather](https://t.me/BotFather))

## Установка

```bash
git clone <repository-url>
cd <project-folder>
pip install -r requirements.txt
```

или напрямую:

```bash
pip install aiogram asyncpg
```

## Конфигурация

Все настройки задаются в начале файла `main.py`:

```python
TOKEN = "your-telegram-bot-token"

DB_NAME = "your-database-name"
DB_USER = "your-database-user"
DB_PASSWORD = "your-database-password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

Таблица `users` создаётся автоматически при первом запуске — дополнительная миграция не требуется.

## Запуск

```bash
python3 main.py
```

## Схема базы данных

Таблица `users`:

| Поле | Тип | Описание |
|---|---|---|
| `id` | `SERIAL PRIMARY KEY` | Уникальный идентификатор записи |
| `telegram_id` | `BIGINT UNIQUE NOT NULL` | Идентификатор пользователя в Telegram |
| `full_name` | `TEXT NOT NULL` | Отображаемое имя пользователя |

## Особенности реализации

- Весь код находится в одном файле `main.py`
- Все операции с базой данных выполняются асинхронно через `asyncpg`
- Без использования FSM, middleware, роутеров и клавиатур — только базовые обработчики команд
- Подробные комментарии в коде для лёгкого понимания

## Лицензия

MIT
