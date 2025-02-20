# src/infrastructure/web/controllers/user_controller.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query
from application.commands.create_user_command import CreateUserCommand
from application.queries.get_user_by_id_query import GetUserByIdQuery
from application.queries.list_users_query import ListUsersQuery
from application.mediator.mediator import Mediator
from core.entities.user import User
from infrastructure.container import container_instance

def get_mediator():
    return container_instance.mediator()

router = APIRouter()

@router.post("/")
async def create_user(command: CreateUserCommand, mediator: Mediator = Depends(get_mediator)):
    return await mediator.send(command)

@router.get("/{user_id}")
async def get_user_by_id(user_id: int = Path(..., description="ID del usuario")):
    query = GetUserByIdQuery(id=user_id)
    mediator = container_instance.mediator()   
    
    return await mediator.query(query)

@router.get("/")
async def list_users(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    email: Optional[str] = Query(None, description="Filtrar por correo electrónico")    
):
    """
    Endpoint para listar usuarios.
    Opcionalmente, puedes filtrar por nombre o correo electrónico.
    """    
    # Crear una instancia de ListUsersQuery con los parámetros de consulta
    query = ListUsersQuery(name=name, email=email)    
    
    mediator = container_instance.mediator()
    
    # Pasar la consulta al mediator
    return await mediator.query(query)