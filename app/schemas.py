from __future__ import annotations
from pydantic import BaseModel, BaseConfig, EmailStr, validator
from datetime import date
from typing import List, ForwardRef, Optional
from uuid import UUID


class UserSchema(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    password: str
    is_active: bool
    is_superuser: bool
    books: list["RentalSchemaUser"] = []

    @validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email is required")
        return value

    class Config(BaseConfig):
        orm_mode = True


class UserSchemaIn(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: str

    @validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email is required")
        return value

    class Config(BaseConfig):
        orm_mode = True


class UserSchemaBooks(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    password: str
    is_active: bool
    is_superuser: bool

    class Config(BaseConfig):
        orm_mode = True

    @validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email is required")
        return value


class RentalSchema(BaseModel):
    id: UUID
    user: UserSchemaRef
    book: BookSchemaRef
    rented_at: date
    returned_at: date

    class Config(BaseConfig):
        orm_mode = True


class RentalSchemaUser(BaseModel):
    id: UUID
    book: BookSchemaRef
    rented_at: date
    returned_at: date

    class Config(BaseConfig):
        orm_mode = True


class RentalSchemaIn(BaseModel):
    book_id: str
    rented_at: date
    returned_at: Optional[date]

    class Config(BaseConfig):
        orm_mode = True


class BookSchema(BaseModel):
    id: UUID
    name: str
    written_at: date
    author: AuthorSchemaRef
    library: LibrarySchemaRef
    rental: RentalSchema

    class Config(BaseConfig):
        orm_mode = True


class AuthorSchemaBooks(BaseModel):
    id: UUID
    name: str

    class Config(BaseConfig):
        orm_mode = True


class LibrarySchemaBooks(BaseModel):
    id: UUID
    name: str
    city: str

    class Config(BaseConfig):
        orm_mode = True


class AuthorSchema(BaseModel):
    id: UUID
    name: str
    books: List[BookSchema] = []

    class Config(BaseConfig):
        orm_mode = True


class LibrarySchema(BaseModel):
    id: UUID
    name: str
    city: str
    books: List[BookSchema] = []

    class Config(BaseConfig):
        orm_mode = True


class AuthorSchemaIn(BaseModel):
    name: str

    class Config(BaseConfig):
        orm_mode = True


class LibrarySchemaIn(BaseModel):
    name: str
    city: str

    class Config(BaseConfig):
        orm_mode = True


class BookSchemaIn(BaseModel):
    name: str
    library_id: str
    author_id: str
    written_at: date

    class Config(BaseConfig):
        orm_mode = True


AuthorSchemaRef = ForwardRef("AuthorSchemaBooks")
LibrarySchemaRef = ForwardRef("LibrarySchemaBooks")
UserSchemaRef = ForwardRef("UserSchemaBooks")
BookSchemaRef = ForwardRef("BookSchema")


BookSchema.update_forward_refs()
RentalSchema.update_forward_refs()
RentalSchemaUser.update_forward_refs()
