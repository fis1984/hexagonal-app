from pydantic import BaseModel

class GetUserByIdQuery(BaseModel):
    id: int
