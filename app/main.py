from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import init_models
from app.routes.posts import router as PostsRouter
from app.routes.users import router as UserRouter
from app.routes.auth import router as AuthRouter

load_dotenv()


async def lifespan(app: FastAPI):
    init_models()
    print("Models created sucessfully!")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(PostsRouter)
app.include_router(UserRouter)
app.include_router(AuthRouter)


@app.get("/")
async def root():
    return {"message": "Hello World"}
