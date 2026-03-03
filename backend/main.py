from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.market import router as market_router
from routes.stocks import router as stocks_router

app = FastAPI()

app.include_router(health_router)
app.include_router(market_router)
app.include_router(stocks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois vamos restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)