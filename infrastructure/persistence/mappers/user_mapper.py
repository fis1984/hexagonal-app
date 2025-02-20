from core.entities.user import User
from infrastructure.persistence.models import UserModel

class UserMapper:
    @staticmethod
    def entity_to_model(entity: User) -> UserModel:
        return UserModel(name=entity.name, email=entity.email)
    
    @staticmethod
    def model_to_entity(model: UserModel) -> User:
        return User(name=model.name, email=model.email, id=model.id)