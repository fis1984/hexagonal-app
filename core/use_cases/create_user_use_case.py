from core.entities.user import User
from core.ports.i_user_repository import IUserRepository
from core.ports.i_unit_of_work import IUnitOfWork

class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository, unit_of_work: IUnitOfWork):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    def execute(self, name: str, email: str) -> User:
        user = User(id=None, name=name, email=email)
        self.user_repository.create(user)
        self.unit_of_work.commit()
        return user