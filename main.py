import logging
import os
import sys
import time

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from apis.base import api_router
from core.config import settings
from core.constants import OperatingSystem

import platform

operating_system = platform.system()

timestr = time.strftime("%Y%m%d-%H%M%S")

config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}

logger = logging.getLogger("gunicorn.error")


def include_router(app):
    app.include_router(api_router, prefix=settings.API_V1_STR)


def __setup_logging(log_level: str):
    log_level = getattr(logging, log_level.upper())
    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    root_logger = logging.getLogger("gunicorn.error")
    root_logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)
    logger.info("Set up logging with log level %s", log_level)


def init_logging():
    logging.basicConfig(format='%(levelname)s (%(asctime)s: %(message)s (Line %(lineno)d [%(filename)s]))',
                        datefmt='%d%m%Y %I:%M:%S %p',
                        level=logging.DEBUG)


def get_logger():
    return logging


def start_application():
    try:
        if settings.PRODUCTION_ENV == "True":
            app = FastAPI(docs_url=None)
        else:
            app = FastAPI()
    except:
        app = FastAPI()
    include_router(app)
    add_pagination(app)

    __setup_logging(settings.LOG_LEVEL)
    return app


app = start_application()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="HIG Docs",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# app.openapi = custom_swagger_ui_html
app.openapi = custom_openapi


class CustomHTTPException(Exception):
    def __init__(self, detail: str, status_code: str):
        self.detail = detail
        self.status_code = status_code


@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    code = "000"
    code = f"{exc.status_code}"
    status_code = int(code)
    return JSONResponse(
        status_code=status_code,
        content={"status_code":status_code,"detail": f"{exc.detail}"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace ["*"] with your list of allowed origins (e.g., ["http://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Replace ["*"] with the HTTP methods you want to allow (e.g., ["GET", "POST"])
    allow_headers=["*"],  # Replace ["*"] with the headers you want to allow
)


if __name__ == '__main__' and operating_system.lower() == OperatingSystem.LINUX.lower():
    from core.gunicorn_start import start_gunicorn
    start_gunicorn(app)
