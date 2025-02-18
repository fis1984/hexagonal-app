# src/application/handlers/list_users_handler.py
from application.queries.list_users_query import ListUsersQuery
from core.use_cases.list_users_use_case import ListUsersUseCase

class ListUsersHandler:
    def __init__(self, list_users_use_case: ListUsersUseCase):
        self.list_users_use_case = list_users_use_case

    async def handle(self):
        return self.list_users_use_case.execute()