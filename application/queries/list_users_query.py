from pydantic import BaseModel

class ListUsersQuery(BaseModel):
    name: str | None = None
    email: str | None = None