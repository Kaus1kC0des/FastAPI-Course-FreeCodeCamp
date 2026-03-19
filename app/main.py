from app.logging_config import setup_logging

setup_logging("DEBUG")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import init_models
from app.routes.posts import router as PostsRouter
from app.routes.users import router as UserRouter
from app.middleware.logging_middleware import logging_middleware
import sentry_sdk
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    send_default_pii=True,
)


async def lifespan(app: FastAPI):
    init_models()
    logger.debug("Models created sucessfully!")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(PostsRouter)
app.include_router(UserRouter)
app.middleware("http")(logging_middleware)


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}
