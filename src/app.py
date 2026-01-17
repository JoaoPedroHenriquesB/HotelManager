from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.handlers.global_handler import setup_exceptions
from src.routers.auth_router import auth_router
from src.routers.guest_router import guest_router
from src.routers.room_router import room_router
from src.routers.stay_router import stay_router
from src.routers.users_router import user_router

app = FastAPI(title="Hotel Manager")
setup_exceptions(app)

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stay_router, prefix="/bookings", tags=["bookings"])
app.include_router(guest_router, prefix="/guests", tags=["guests"])
app.include_router(room_router, prefix="/rooms", tags=["rooms"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
def health() -> dict:
    return {"message": "healthy"}
