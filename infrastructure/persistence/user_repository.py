# src/infrastructure/persistence/user_repository.py
from sqlalchemy.orm import Session
from core.entities.user import User
from core.ports.i_user_repository import IUserRepository
from infrastructure.persistence.mappers.user_mapper import UserMapper
from infrastructure.persistence.models import UserModel

class UserRepository(IUserRepository):
    def __init__(self):        
        self.db_session = None
        
    def set_session(self, session: Session):
        self.db_session = session

    def create(self, user: User) -> None:
        if self.db_session is None:
            raise ValueError("La sesión no ha sido asignada al repositorio.")
        
        db_user = UserMapper.entity_to_model(user)
        self.db_session.add(db_user)
        self.db_session.flush()  # Asigna un ID temporal (opcional) 

    def find_by_id(self, id: int) -> User | None:
        if self.db_session is None:
            raise ValueError("La sesión no ha sido asignada al repositorio.")
        
        db_user = self.db_session.query(UserModel).filter(UserModel.id == id).first()
        if db_user:
            return UserMapper.entity_to_model(db_user)
        return None
    
    def find_by_email(self, email: str) -> User | None:
        if self.db_session is None:
            raise ValueError("La sesión no ha sido asignada al repositorio.")
        
        db_user = self.db_session.query(UserModel).filter(UserModel.email == email).first()
        if db_user:
            return UserMapper.model_to_entity(db_user)
        return None

    def find_all(self) -> list[User]:
        if self.db_session is None:
            raise ValueError("La sesión no ha sido asignada al repositorio.")
        
        db_users = self.db_session.query(UserModel).all()
        return [UserMapper.model_to_entity(user) for user in db_users]
    
    def find_by_filters(self, name: str = None, email: str = None) -> list[User]:
        if self.db_session is None:
            raise ValueError("La sesión no ha sido asignada al repositorio.")
        
        query = self.db_session.query(UserModel)
        if name:
            query = query.filter(UserModel.name == name)
        if email:
            query = query.filter(UserModel.email == email)
        db_users = query.all()
        return [UserMapper.model_to_entity(user) for user in db_users]