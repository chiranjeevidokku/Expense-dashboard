from fastapi import FastAPI
from user_api.resources import user_router
from savings_api.resources import savings_router

app = FastAPI()

app.include_router(user_router)
app.include_router(savings_router)