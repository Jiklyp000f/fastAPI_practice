from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.exc import DatabaseError, OperationalError
import aiosqlite
import os
from typing import Optional

# Создание движка для асинхронной работы с базой данных
DATABASE_URL = "sqlite+aiosqlite:///tasks.db"
engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Базовая модель для ORM
class Model(DeclarativeBase):
    pass

# Описание таблицы tasks
class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]

# Проверка целостности базы данных
async def check_db_integrity():
    try:
        async with aiosqlite.connect("tasks.db") as db:
            async with db.execute("PRAGMA integrity_check;") as cursor:
                result = await cursor.fetchone()
                if result[0] != "ok":
                    print("Database is corrupted. Consider rebuilding it.")
                    return False
        print("Database integrity check passed.")
        return True
    except Exception as e:
        print(f"Error while checking database integrity: {e}")
        return False

# Создание таблиц
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
        print("Tables created successfully.")
    except (DatabaseError, OperationalError) as e:
        print(f"Error while creating tables: {e}")

# Удаление таблиц
async def delete_table():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)
        print("Tables deleted successfully.")
    except (DatabaseError, OperationalError) as e:
        print(f"Error while deleting tables: {e}")

# Восстановление базы данных
async def recreate_db():
    if os.path.exists("tasks.db"):
        print("Deleting corrupted database...")
        os.remove("tasks.db")
    await create_tables()
    print("Database recreated successfully.")

# Инициализация базы данных
async def initialize():
    db_is_valid = await check_db_integrity()
    if not db_is_valid:
        await recreate_db()
    else:
        await create_tables()

# Сброс базы данных
async def reset_database():
    await check_db_integrity()
    await delete_table()
    await create_tables()

# Главная функция для запуска
import asyncio

if __name__ == "__main__":
    asyncio.run(initialize())
