from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.api.rooms import router as rooms_router
from app.websocket import router as websocket_router
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (nothing needed here)


app = FastAPI(
    title="Yapper API",
    lifespan=lifespan
)

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ROUTERS --------------------

app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(websocket_router)


@app.get("/")
def root():
    return {"message": "Yapper backend running"}
