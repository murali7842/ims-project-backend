from src.app.config.db_config import AsyncSessionLocal


async def get_db() -> AsyncSessionLocal:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()