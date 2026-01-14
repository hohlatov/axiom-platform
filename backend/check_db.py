import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://axiom_user:axiom_pass@localhost:5432/axiom_db"

async def check():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT tablename FROM pg_tables WHERE schemaname = 'public';
        """))
        tables = result.fetchall()
        print("📋 Таблицы в БД:")
        for row in tables:
            print(f"  - {row[0]}")
    await engine.dispose()

asyncio.run(check())