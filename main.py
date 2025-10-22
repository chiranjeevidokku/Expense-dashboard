from fastapi import FastAPI
from user_api.resources import user_router
from budget_api.resources import financial_router
from transactions_api.resources import transaction_api

app = FastAPI()

app.include_router(user_router)
app.include_router(financial_router)
app.include_router(transaction_api)