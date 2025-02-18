from typing import List, Optional
from core.entities.user import User

class IUserRepository:
    def create(self, user: User) -> None:
        raise NotImplementedError
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError
    
    def find_all(self) -> List[User]:
        raise NotImplementedError