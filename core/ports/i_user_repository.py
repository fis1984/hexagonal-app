from abc import ABC, abstractmethod
from typing import List, Optional
from core.entities.user import User
from sqlalchemy.orm import Session

class IUserRepository(ABC):
    
    @abstractmethod
    def set_session(self, session: Session) -> None:
        pass
    @abstractmethod
    def create(self, user: User) -> None:
        pass    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[User]:
        pass
    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass
    @abstractmethod
    def find_all(self) -> List[User]:
        pass
    
    @abstractmethod
    def find_by_filters(self, name: str = None, email: str = None) -> list[User]:
        pass
