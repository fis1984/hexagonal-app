# src/infrastructure/web/controllers/user_controller.py
from fastapi import APIRouter, Depends
from application.commands.create_user_command import CreateUserCommand
from application.queries.get_user_by_id_query import GetUserByIdQuery
from application.queries.list_users_query import ListUsersQuery
from application.mediator.mediator import Mediator
from infrastructure.container import Container

def get_mediator():
    return Container.mediator()

router = APIRouter()

@router.post("/")
async def create_user(command: CreateUserCommand, mediator: Mediator = Depends(get_mediator)):
    return await mediator.send(command)

@router.get("/{user_id}")
async def get_user_by_id(query: GetUserByIdQuery, mediator: Mediator = Depends(get_mediator)):
    return await mediator.query(query)

@router.get("/")
async def list_users(query: ListUsersQuery, mediator: Mediator = Depends(get_mediator)):
    return await mediator.query(query)