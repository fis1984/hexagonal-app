from typing import List
from core.entities.user import User
from core.ports.i_user_repository import IUserRepository

class ListUsersUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        return self.user_repository.find_all()