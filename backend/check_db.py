# check_db.py
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://axiom_user:axiom_pass@localhost:5432/axiom_db"

async def check_tables():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT tablename FROM pg_tables WHERE schemaname = 'public';
        """))
        tables = result.fetchall()
        print("Таблицы в БД:")
        for row in tables:
            print(f"  - {row[0]}")

        # Проверим alembic_version
        try:
            version = await conn.execute(text("SELECT * FROM alembic_version;"))
            print("\nВерсия миграции:")
            for row in version.fetchall():
                print(f"  - {row[0]}")
        except Exception as e:
            print(f"\n❌ alembic_version не найдена: {e}")

    await engine.dispose()

asyncio.run(check_tables())