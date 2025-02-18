from core.entities.user import User
from core.ports.i_user_repository import IUserRepository
from errors.custom_errors import UserNotFoundError

class GetUserByIdUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user