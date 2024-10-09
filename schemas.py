from pydantic import BaseModel
from typing import Union


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    content: str

    category_id: Union[int, None] = None
    author_name: Union[str, None] = None
    category_name: Union[str, None] = None


class BookCreate(BookBase):
    pass


class BookResponse(BaseModel):
    id: int
    title: str
    content: str
    author: AuthorResponse
    category: CategoryResponse

    class Config:
        from_attributes = True


class PurchaseRequestResponse(BaseModel):
    id: int
    book_id: int
    reader_name: str
    payment_details: str
    status: str

    class Config:
        from_attributes = True


class PurchaseRequestCreate(BaseModel):
    book_id: int
    reader_name: str
    payment_details: str
    # status: str


# Model for the request, with the password
class UserCreate(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    password: str
    role: str  # Add role here


# Model for the response, without the password
class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool
    role: str


class UserInDB(UserResponse):
    hashed_password: str
