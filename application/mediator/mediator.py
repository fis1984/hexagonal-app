from typing import Generic, Type, TypeVar

from application.queries.list_users_query import ListUsersQuery

TQuery = TypeVar("TQuery")
TResult = TypeVar("TResult")

class Mediator(Generic[TQuery, TResult]):
    def __init__(self, command_handlers=None, query_handlers=None):
        self.command_handlers = command_handlers or {}
        self.query_handlers = query_handlers or {}
    
    """ def register_command_handler(self, command_type: Type, handler):
        self.command_handlers[command_type] = handler
        
    def register_query_handler(self, query_type: Type, handler):
        self.query_handlers[query_type] = handler """
    def register_query_handler(self, query_type: Type[TQuery], handler):
        """
        Registra un handler para una consulta específica.
        """
        self.query_handlers[query_type] = handler
        
    async def send(self, command):
        handler_factory = self.command_handlers.get(type(command))
        if not handler_factory:
            raise ValueError(f"No handler registered for command: {type(command)}")
        
        # Obtener una instancia del handler
        handler = handler_factory()
        return await handler.handle(command)

    async def query(self, query: TQuery) -> TResult:
        # print ("Query is: %s" % type(query))
        handler_factory = self.query_handlers.get(type(query))
        if not handler_factory:
            raise ValueError(f"No handler registered for query: {type(query)}")
      
        # Obtener una instancia del handler
        handler = handler_factory()        
        return await handler.handle(query)
    
def configure_mediator(mediator: Mediator, user_repository):
    from core.use_cases.find_all_users_use_case import FindAllUsersUseCase

    find_all_users_use_case = FindAllUsersUseCase(user_repository)
    mediator.register_query_handler(ListUsersQuery, find_all_users_use_case)