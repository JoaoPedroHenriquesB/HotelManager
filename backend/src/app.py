from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.auth_router import auth_router
from src.routers.guest_router import guest_router
from src.routers.room_router import room_router
from src.routers.stay_router import stay_router
from src.routers.users_router import user_router
from src.handlers.global_handler import setup_exceptions

app = FastAPI(title="Hotel Manager")
setup_exceptions(app)

origins = [
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(stay_router)
app.include_router(guest_router)
app.include_router(room_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def health() -> dict:
    return {"message": "healthy"}
