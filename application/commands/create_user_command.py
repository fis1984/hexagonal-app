from pydantic import BaseModel

class CreateUserCommand(BaseModel):
    name: str
    email: str