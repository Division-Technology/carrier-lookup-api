from fastapi import FastAPI
from .routers import phone_router

app = FastAPI()

app.include_router(phone_router)
