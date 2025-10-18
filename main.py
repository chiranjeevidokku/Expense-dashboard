from fastapi import FastAPI
from user_api.resources import user_router
from savings_api.resources import savings_router
from income_api.resources import income_router
from expense_api.resources import expense_router

app = FastAPI()

app.include_router(user_router)
app.include_router(savings_router)
app.include_router(income_router)
app.include_router(expense_router)