import uvloop
import asyncio
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import routes

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI()

cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:4200,http://localhost").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
