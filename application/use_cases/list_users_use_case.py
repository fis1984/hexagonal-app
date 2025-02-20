from typing import List
from core.entities.user import User
from core.ports.i_unit_of_work import IUnitOfWork
from core.ports.i_user_repository import IUserRepository

class ListUsersUseCase:
    def __init__(self, user_repository: IUserRepository, unit_of_work: IUnitOfWork):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    def execute(self, query) -> List[User]:
        """
        Maneja la consulta para buscar usuarios.
        """
        with self.unit_of_work as uow:
            session = uow.get_session()
            self.user_repository.set_session(session)
        
            # Ejecutar la lógica de búsqueda dentro del contexto del UnitOfWork
            if hasattr(query, "name") or hasattr(query, "email"):
                return self.user_repository.find_by_filters(name=query.name, email=query.email)
            return self.user_repository.find_all()