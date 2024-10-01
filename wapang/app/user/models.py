from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    address: str | None = None
    phone_number: str | None = None
