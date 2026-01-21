from app.database import AsyncSessionLocal, SyncSessionLocal


async def get_db_async():
    db = AsyncSessionLocal()
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        await db.close()


def get_db_sync():
    db = SyncSessionLocal()
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()
