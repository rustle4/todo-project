from fastapi import FastAPI

from app.users.router import router

app = FastAPI()

app.include_router(router)
