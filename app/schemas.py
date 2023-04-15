from __future__ import annotations
from pydantic import BaseModel, BaseConfig
from datetime import date
from typing import List, ForwardRef
from uuid import UUID


class BookSchema(BaseModel):
    id: UUID
    name: str
    written_at: date
    author: AuthorSchemaRef
    library: LibrarySchemaRef

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

BookSchema.update_forward_refs()
