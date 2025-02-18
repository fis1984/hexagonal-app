# src/presentation/main.py
from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide
from infrastructure.container import Container
from middleware.error_handler_middleware import error_handler_middleware
from infrastructure.web.controllers.user_controller import router as user_router

app = FastAPI()

# Middleware
@app.middleware("http")
async def middleware(request, call_next):
    return await error_handler_middleware(request, call_next)

# Contenedor de inyección de dependencias
container = Container()
container.wire(modules=["infrastructure.web.controllers.user_controller"])

# Rutas
app.include_router(user_router, prefix="/users")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)