# src/middleware/error_handler_middleware.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse

async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})