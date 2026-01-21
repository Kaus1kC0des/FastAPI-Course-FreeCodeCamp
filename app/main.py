import os
import time
import app.models as models

from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from app.database import init_models
from app.dependencies import get_db_sync, get_db_async
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.schemas import *
from app.routes.posts import router as PostsRouter
from app.logger import setup_logging

load_dotenv()

app = FastAPI()
app.include_router(PostsRouter)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
async def test_posts(db: AsyncSession = Depends(get_db_async)):
    query = select(models.Post).where(models.Post.id == 2)
    post = await db.scalar(query)
    print(post)
    return {"status": "Success", "post": post}
