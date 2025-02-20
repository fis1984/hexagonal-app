# src/application/use_cases/find_all_users_use_case.py
from typing import Optional, List
from core.entities.user import User
from core.ports.i_user_repository import IUserRepository

class FindAllUsersUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def handle(self, query) -> List[User]:
        """
        Maneja la consulta para buscar usuarios.
        """
        if hasattr(query, "name") or hasattr(query, "email"):
            return self.user_repository.find_by_filters(name=query.name, email=query.email)
        return self.user_repository.find_all()