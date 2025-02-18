from typing import Type

class Mediator:
    def __init__(self):
        self.command_handlers = {}
        self.query_handlers = {}
    
    def register_command_handler(self, command_type: Type, handler):
        self.command_handlers[command_type] = handler
        
    def register_query_handler(self, query_type: Type, handler):
        self.query_handlers[query_type] = handler
        
    async def send(self, command):
        handler = self.command_handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler registered for command: {type(command)}")
        return await handler.handle(command)

    async def query(self, query):
        handler = self.query_handlers.get(type(query))
        if not handler:
            raise ValueError(f"No handler registered for query: {type(query)}")
        return await handler.handle(query)