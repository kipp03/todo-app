from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    # email: str
    userName: str
    password: str


class User(BaseModel):
    id: int
    is_active: bool
    email: str
    userName: str

    class Config:
        orm_mode = True


class LoginRequestDetails(BaseModel):
    userName: str
    password: str
