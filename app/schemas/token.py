from pydantic import BaseModel
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class Tokendata(BaseModel):
    email: str | None = None
    id: UUID | None = None