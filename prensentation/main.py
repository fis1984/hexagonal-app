# src/presentation/main.py
import sys
from pathlib import Path

from sqlalchemy import inspect



# Añadir la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))
# print("PYTHONPATH:", sys.path)

from fastapi import FastAPI
from infrastructure.container import Container
from middleware.error_handler_middleware import error_handler_middleware
from infrastructure.web.controllers.user_controller import router as user_router
from infrastructure.persistence.database import (Base, engine)


app = FastAPI() 

# Middleware
@app.middleware("http")
async def middleware(request, call_next):
    return await error_handler_middleware(request, call_next)

# Contenedor de inyección de dependencias
container = Container()
container.wire(modules=["infrastructure.web.controllers.user_controller"])

# Rutas
app.include_router(user_router, prefix="/users", tags=["users"])

# Crear todas las tablas
# Función para crear tablas solo si no existen
def create_tables_if_not_exist():
    inspector = inspect(engine)  # Inspector para verificar las tablas
    existing_tables = inspector.get_table_names()  # Lista de tablas existentes

    # Obtener los nombres de las tablas definidas en los modelos
    metadata = Base.metadata
    table_names = list(metadata.tables.keys())

    # Verificar si todas las tablas ya existen
    if not all(table in existing_tables for table in table_names):
        print("Creando tablas...")
        metadata.create_all(bind=engine)
    else:
        print("Las tablas ya existen. No se realizaron cambios.")

if __name__ == "__main__":
    create_tables_if_not_exist()
    
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
    