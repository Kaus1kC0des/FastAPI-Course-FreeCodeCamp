from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DATABASE_USER", "")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")

SYNC_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"
)

ASYNC_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE_NAME}"
)

# Engines
sync_engine = create_engine(SYNC_URL, pool_pre_ping=True)

async_engine = create_async_engine(ASYNC_URL, pool_pre_ping=True)

# Session Makers
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# Base
Base = declarative_base()


# Init Models
def init_models():
    print("Starting init_models")  # Debug: start
    print(f"Database URL: {SYNC_URL}")  # Debug: print the URL
    try:
        Base.metadata.create_all(bind=sync_engine, checkfirst=True)
    except Exception as e:
        print(f"Error: {e}")  # Debug: print any errors
