"""
Простой учебный Telegram-бот на aiogram 3 + PostgreSQL (asyncpg).

Что умеет бот:
/start  - сохраняет пользователя в базу данных (если его там ещё нет)
/users  - показывает список всех пользователей
/count  - показывает количество пользователей в базе

Никаких классов, FSM, middleware и клавиатур - только самое простое и понятное.
"""

import asyncio          # нужен, чтобы запускать асинхронный код
import asyncpg          # библиотека для работы с PostgreSQL асинхронно
from aiogram import Bot, Dispatcher       # основные объекты aiogram
from aiogram.filters import Command       # фильтр для обработки команд типа /start
from aiogram.types import Message         # тип "сообщение", которое присылает пользователь


# =========================================================
# НАСТРОЙКИ. Впишите сюда свои данные перед запуском бота.
# =========================================================

TOKEN = "ВАШ_ТОКЕН_БОТА"        # токен бота, который выдаёт @BotFather

DB_NAME = "ВАШ_НАЗВАНИЕ_БАЗЫ"       # название базы данных PostgreSQL
DB_USER = "ВАШ_ПОЛЬЗОВАТЕЛЬ_БД"     # имя пользователя PostgreSQL
DB_PASSWORD = "ВАШ_ПАРОЛЬ_БД"       # пароль от базы данных
DB_HOST = "localhost"               # адрес сервера базы данных (обычно localhost)
DB_PORT = "5432"                    # порт PostgreSQL (по умолчанию 5432)


# =========================================================
# СОЗДАЁМ ОБЪЕКТЫ БОТА И ДИСПЕТЧЕРА
# =========================================================

# Bot - это объект, который умеет отправлять сообщения в Telegram
bot = Bot(token=TOKEN)

# Dispatcher - это объект, который получает обновления (сообщения) от Telegram
# и передаёт их нужным функциям-обработчикам
dp = Dispatcher()


# =========================================================
# ФУНКЦИЯ ДЛЯ СОЗДАНИЯ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
# =========================================================

async def get_db_connection():
    """
    Создаёт и возвращает новое подключение к PostgreSQL.
    Мы будем вызывать эту функцию каждый раз, когда нужно
    выполнить запрос к базе данных.
    """
    connection = await asyncpg.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    return connection


# =========================================================
# ФУНКЦИЯ СОЗДАНИЯ ТАБЛИЦЫ users, ЕСЛИ ЕЁ ЕЩЁ НЕТ
# =========================================================

async def create_table():
    """
    Подключается к базе данных и создаёт таблицу users,
    если такой таблицы ещё не существует.

    Столбцы таблицы:
    id          - уникальный номер записи (создаётся автоматически)
    telegram_id - уникальный id пользователя в Telegram
    full_name   - имя пользователя (то, что он указал в Telegram)
    """
    conn = await get_db_connection()

    # SQL-запрос CREATE TABLE. IF NOT EXISTS означает:
    # "создать таблицу, только если её ещё нет"
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            full_name TEXT NOT NULL
        )
        """
    )

    # закрываем подключение, чтобы не тратить ресурсы впустую
    await conn.close()


# =========================================================
# ОБРАБОТЧИК КОМАНДЫ /start
# =========================================================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Срабатывает, когда пользователь отправляет команду /start.
    1. Проверяет, есть ли пользователь уже в базе данных.
    2. Если нет - добавляет его.
    3. Отправляет приветственное сообщение.
    """
    # message.from_user может быть None (например, для сообщений от анонимных
    # администраторов канала). Если отправителя нет - ничего не делаем.
    if message.from_user is None:
        return

    conn = await get_db_connection()

    # telegram_id - уникальный идентификатор пользователя в Telegram
    telegram_id = message.from_user.id
    # full_name - имя и фамилия пользователя (как указано в его профиле)
    full_name = message.from_user.full_name

    # Проверяем через SELECT, есть ли уже такой пользователь в таблице
    existing_user = await conn.fetchrow(
        "SELECT id FROM users WHERE telegram_id = $1",
        telegram_id,
    )

    # Если пользователя нет (existing_user is None) - добавляем его
    if existing_user is None:
        await conn.execute(
            "INSERT INTO users (telegram_id, full_name) VALUES ($1, $2)",
            telegram_id,
            full_name,
        )

    await conn.close()

    # Отправляем пользователю приветственное сообщение
    await message.answer(
        f"Привет, {full_name}! 👋\n"
        f"Ты успешно зарегистрирован в базе данных.\n\n"
        f"Доступные команды:\n"
        f"/start - регистрация\n"
        f"/users - список всех пользователей\n"
        f"/count - количество пользователей"
    )


# =========================================================
# ОБРАБОТЧИК КОМАНДЫ /users
# =========================================================

@dp.message(Command("users"))
async def cmd_users(message: Message):
    """
    Срабатывает, когда пользователь отправляет команду /users.
    Выводит список всех пользователей, которые есть в базе данных.
    """
    conn = await get_db_connection()

    # SELECT * означает "выбрать все столбцы из таблицы"
    rows = await conn.fetch("SELECT telegram_id, full_name FROM users")

    await conn.close()

    # Если пользователей в базе нет
    if len(rows) == 0:
        await message.answer("Пока в базе данных нет ни одного пользователя.")
        return

    # Собираем текст со списком пользователей
    text = "Список пользователей:\n\n"
    for row in rows:
        # row["full_name"] и row["telegram_id"] - доступ к столбцам результата
        text += f"👤 {row['full_name']} (id: {row['telegram_id']})\n"

    await message.answer(text)


# =========================================================
# ОБРАБОТЧИК КОМАНДЫ /count
# =========================================================

@dp.message(Command("count"))
async def cmd_count(message: Message):
    """
    Срабатывает, когда пользователь отправляет команду /count.
    Показывает, сколько всего пользователей сохранено в базе данных.
    """
    conn = await get_db_connection()

    # COUNT(*) - специальная SQL-функция, которая считает количество строк
    # fetchval() возвращает только одно значение (не строку и не список)
    total_users = await conn.fetchval("SELECT COUNT(*) FROM users")

    await conn.close()

    await message.answer(f"Всего пользователей в базе: {total_users}")


# =========================================================
# ГЛАВНАЯ ФУНКЦИЯ ЗАПУСКА БОТА
# =========================================================

async def main():
    """
    Главная асинхронная функция:
    1. Создаёт таблицу users (если её ещё нет).
    2. Запускает бота в режиме постоянного опроса Telegram (polling).
    """
    # Сначала убеждаемся, что таблица в базе данных существует
    await create_table()

    # Запускаем бота. Он будет работать, пока мы его не остановим (Ctrl+C)
    await dp.start_polling(bot)


# Точка входа в программу.
# Если файл запущен напрямую (а не импортирован), запускаем main()
if __name__ == "__main__":
    asyncio.run(main())