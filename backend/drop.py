# drop_alembic.py
import asyncio
import asyncpg

async def drop_alembic_version():
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="axiom_user",
        password="axiom_pass",
        database="axiom_db"
    )
    try:
        await conn.execute("DROP TABLE IF EXISTS alembic_version;")
        print("✅ Таблица alembic_version удалена")
    except Exception as e:
        print("Ошибка:", e)
    finally:
        await conn.close()

asyncio.run(drop_alembic_version())
