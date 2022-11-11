
import json
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware

from loguru import logger

from routers.statistic import router as statistic_router

app = FastAPI(
    title="Eventers XIVIVIDE",
    version="1",
    description="Zefir CRM API3",
    # openapi_url="/api/v1/openapi.json",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.add(
        "./assets/logs/latest.log", rotation="200 KB", enqueue=True, level="INFO"
    )
    logger.info("App started")


app.include_router(statistic_router)


# app = VersionedFastAPI(
#     app,
#     version="1",
#     openapi_version="3.0.2",
#     description="Test API",
#     version_format="{major}",
#     prefix_format="/v{major}",
#     tags_metadata=tags_metadata,
#     allow_middlewares=True,
#     middleware=middle,
# )