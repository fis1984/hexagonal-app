# src/infrastructure/container.py
from dependency_injector import containers, providers
from application.commands.create_user_command import CreateUserCommand
from application.handlers.create_user_handler import CreateUserHandler
from application.handlers.get_user_by_id_handler import GetUserByIdHandler
from application.handlers.list_users_handler import ListUsersHandler
from application.mediator.mediator import Mediator, configure_mediator
from application.queries.get_user_by_id_query import GetUserByIdQuery
from application.queries.list_users_query import ListUsersQuery
from application.use_cases.create_user_use_case import CreateUserUseCase
from application.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from application.use_cases.list_users_use_case import ListUsersUseCase
from infrastructure.persistence.user_repository import UserRepository
from infrastructure.persistence.unit_of_work import UnitOfWork

from infrastructure.persistence.database import get_db_session, SessionLocal

class Container(containers.DeclarativeContainer):
    # Configuración
    config = providers.Configuration()
    
    # Proveedor para la sesión de base de datos
    db_session = providers.Resource(get_db_session)  
  
    # Define a provider for the session factory
    session_provider = providers.Singleton(lambda: SessionLocal) 

    # Repositorios
    user_repository = providers.Factory(
        UserRepository
    ) 

    # Unidad de trabajo
    unit_of_work = providers.Factory(
        UnitOfWork,
        session_factory=session_provider
    )

    # Casos de uso
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        unit_of_work=unit_of_work
    )
    get_user_by_id_use_case = providers.Factory(
        GetUserByIdUseCase,
        user_repository=user_repository,
        unit_of_work=unit_of_work
    )
    list_users_use_case = providers.Factory(
        ListUsersUseCase,
        user_repository=user_repository,
        unit_of_work=unit_of_work
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
    
     # Configuración del mediador
     # Configuración del mediador
    configured_mediator = providers.Singleton(
        configure_mediator,
        mediator=mediator,
        user_repository=user_repository
    )
    

# Función wrapper para obtener el mediador configurado
""" def get_configured_mediator():
    return Container().configured_mediator() """
    
container_instance = Container()
    