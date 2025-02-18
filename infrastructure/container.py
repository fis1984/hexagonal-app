# src/infrastructure/container.py
from dependency_injector import containers, providers
from application.commands.create_user_command import CreateUserCommand
from application.handlers.create_user_handler import CreateUserHandler
from application.handlers.get_user_by_id_handler import GetUserByIdHandler
from application.handlers.list_users_handler import ListUsersHandler
from application.mediator.mediator import Mediator
from application.queries.get_user_by_id_query import GetUserByIdQuery
from application.queries.list_users_query import ListUsersQuery
from infrastructure.persistence.user_repository import UserRepository
from infrastructure.persistence.unit_of_work import UnitOfWork
from core.use_cases.create_user_use_case import CreateUserUseCase
from core.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from core.use_cases.list_users_use_case import ListUsersUseCase
from infrastructure.persistence.database import SessionLocal

class Container(containers.DeclarativeContainer):
    # Configuración
    config = providers.Configuration()

    # Repositorios
    user_repository = providers.Factory(
        UserRepository,
        db_session=providers.Resource(SessionLocal)
    )

    # Unidad de trabajo
    unit_of_work = providers.Factory(
        UnitOfWork,
        session_factory=providers.Singleton(SessionLocal)
    )

    # Casos de uso
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        unit_of_work=unit_of_work
    )
    get_user_by_id_use_case = providers.Factory(
        GetUserByIdUseCase,
        user_repository=user_repository
    )
    list_users_use_case = providers.Factory(
        ListUsersUseCase,
        user_repository=user_repository
    )
    
    # Handlers
    create_user_handler = providers.Factory(
        CreateUserHandler,
        create_user_use_case=create_user_use_case
    )
    get_user_by_id_handler = providers.Factory(
        GetUserByIdHandler,
        get_user_by_id_use_case=get_user_by_id_use_case
    )
    list_users_handler = providers.Factory(
        ListUsersHandler,
        list_users_use_case=list_users_use_case
    )
    
    # Mediador
    mediator = providers.Singleton(Mediator)
    mediator.add_kwargs(
        command_handlers={
            CreateUserCommand: create_user_handler,
        },
        query_handlers={
            GetUserByIdQuery: get_user_by_id_handler,
            ListUsersQuery: list_users_handler,
        }
    )
    
   