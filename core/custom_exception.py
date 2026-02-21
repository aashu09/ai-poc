from fastapi import  Request
from fastapi.responses import JSONResponse

class SystemException(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


def system_exception_handler(request: Request, exc: SystemException):
    return JSONResponse(
        status_code=400,
        content={"status": exc.status, "message":exc.message},
    )


class ApplicationException(Exception):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message


def application_exception_handler(request: Request, exc: ApplicationException):
    return JSONResponse(
        status_code=400,
        content={"status": exc.status, "message":exc.message},
    )