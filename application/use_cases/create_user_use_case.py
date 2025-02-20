from application.exceptions.user_exists_error import UserAlreadyExistsError
from core.entities.user import User
from core.ports.i_user_repository import IUserRepository
from core.ports.i_unit_of_work import IUnitOfWork

class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository, unit_of_work: IUnitOfWork):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    def execute(self, name: str, email: str) -> User:
        # Usar el UnitOfWork como un context manager
        with self.unit_of_work as uow:
            # Obtener la sesión del UnitOfWork y asignarla al repositorio
            session = uow.get_session()
            self.user_repository.set_session(session)

            # Verificar si ya existe un usuario con el mismo correo electrónico
            existing_user = self.user_repository.find_by_email(email)
            if existing_user:
                raise UserAlreadyExistsError(f"Ya existe un usuario con el correo electrónico: {email}")

            # Crear el nuevo usuario
            user = User(name=name, email=email, id=None)
            self.user_repository.create(user)
            self.unit_of_work.commit()

        return user