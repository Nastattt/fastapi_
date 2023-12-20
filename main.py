from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core.models import Base
from session import engine
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix="/settings.api_v1_prefix")
app.include_router(users_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}


from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.shemas import UserCreate, UserRead

app = FastAPI(
    title="Trading App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
