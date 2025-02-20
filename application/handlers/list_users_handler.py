# src/application/handlers/list_users_handler.py
from dataclasses import dataclass
from application.queries.list_users_query import ListUsersQuery
from application.use_cases.list_users_use_case import ListUsersUseCase


@dataclass
class ListUsersHandler:
    def __init__(self, list_users_use_case: ListUsersUseCase):
        self.list_users_use_case = list_users_use_case

    async def handle(self, query):
        return self.list_users_use_case.execute(query)