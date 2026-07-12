from fastapi import  HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from app.core.logger import logger


# Handles all HTTPException raised by your code
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


# Handles FastAPI/Pydantic validation errors
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Invalid request.",
            "errors": exc.errors(),
        },
    )


# Handles unexpected server errors
async def general_exception_handler(
    request: Request,
    exc: Exception
):  
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error.",
        },
    )