# src/application/handlers/get_user_by_id_handler.py
from application.queries.get_user_by_id_query import GetUserByIdQuery
from core.use_cases.get_user_by_id_use_case import GetUserByIdUseCase

class GetUserByIdHandler:
    def __init__(self, get_user_by_id_use_case: GetUserByIdUseCase):
        self.get_user_by_id_use_case = get_user_by_id_use_case

    async def handle(self, query: GetUserByIdQuery):
        return self.get_user_by_id_use_case.execute(user_id=query.id)