from core.entities.user import User
from core.ports.i_unit_of_work import IUnitOfWork
from core.ports.i_user_repository import IUserRepository
from errors.custom_errors import UserNotFoundError

class GetUserByIdUseCase:
    def __init__(self, user_repository: IUserRepository, unit_of_work: IUnitOfWork):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work
        
    def execute(self, query) -> User:
        with self.unit_of_work as uow:
            session = uow.get_session()
            self.user_repository.set_session(session)
            user = self.user_repository.find_by_id(query.id)
            
            if not user:
                raise UserNotFoundError(query.id)
            return user