# src/infrastructure/persistence/user_repository.py
from sqlalchemy.orm import Session
from core.entities.user import User
from core.ports.i_user_repository import IUserRepository
from infrastructure.persistence.models import UserModel

class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> None:
        db_user = UserModel(name=user.name, email=user.email)
        self.db_session.add(db_user)

    def find_by_id(self, user_id: int) -> User | None:
        db_user = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            return User(id=db_user.id, name=db_user.name, email=db_user.email)
        return None

    def find_all(self) -> list[User]:
        db_users = self.db_session.query(UserModel).all()
        return [User(id=user.id, name=user.name, email=user.email) for user in db_users]