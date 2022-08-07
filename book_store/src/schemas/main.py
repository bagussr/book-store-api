import uuid
from src import BaseModel, Optional, date


class UserSchemas(BaseModel):  # UserSchemas is defined in BaseModel
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
    is_admin: Optional[bool] = False
    is_staff: Optional[bool] = False


class CreateUser(UserSchemas):  # CreateUser is defined in UserSchemas
    pass

    class Config:
        orm_mode = True


class LoginUser(BaseModel):  # LoginUser is defined in BaseModel
    username: str
    password: str

    class Config:
        orm_mode = True


class BookSchemas(BaseModel):  # BookSchemas is defined in BaseModel
    name: str
    author: int
    year_release: Optional[date]
    year_create: Optional[date]
    genre: Optional[str]
    price: int


class CreateBook(BookSchemas):  # CreateBook is defined in BookSchemas
    pass

    class Config:
        orm_mode = True


class AuthorSchemas(BaseModel):  # AuthorSchemas is defined in BaseModel
    name: Optional[str]
    date_of_birth: Optional[date]


class CreateAuthor(AuthorSchemas):  # CreateAuthor is defined in AuthorSchemas
    pass

    class Config:
        orm_mode = True


class OrderSchemas(BaseModel):  # OrderSchemas is defined in BaseModel
    book_id: int
    transaction_id: int
    qty: int
    order_at: Optional[date]


class CreateOrder(OrderSchemas):  # CreateOrder is defined in OrderSchemas
    pass

    class Config:
        orm_mode = True


class TransactionSchemas(BaseModel):  # TransactionSchemas is defined in BaseModel
    member_id: Optional[uuid.UUID] = None


class CreateTransaction(TransactionSchemas):  # CreateTransaction is defined in TransactionSchemas
    pass

    class Config:
        orm_mode = True
