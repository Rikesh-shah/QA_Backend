from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from userdir.routes import UserRoutes
from db import ping_server


app = FastAPI()


@app.on_event("startup")
async def on_start():
    await ping_server()


allowed_origins = [
    "http://31.44.2.38",
    "https://31.44.2.38",
    "http://31.44.2.38:8002",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = allowed_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
usr_router = UserRoutes()
usr_router.setup_routes()

app.include_router(usr_router.router)