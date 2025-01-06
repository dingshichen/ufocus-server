from fastapi.responses import JSONResponse
from fastapi import Request

from app import create_app
from .api.param.base import ResultStatus, Result
from .exception import EntityNotFound

app = create_app()

@app.exception_handler(EntityNotFound)
async def value_error_exception_handler(request: Request, exc: EntityNotFound):
    return JSONResponse(
        status_code=200,
        content=Result.fail(ResultStatus.ENTITY_NOT_FOUND, str(exc))
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content=Result.fail(ResultStatus.SYSTEM_ERROR, str(exc))
    )