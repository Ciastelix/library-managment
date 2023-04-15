from fastapi import APIRouter, status, HTTPException, Depends
from app.services.author import AuthorService
from app.containers import Container
from dependency_injector.wiring import inject, Provide
from app.schemas import (
    AuthorSchemaIn,
    BookSchema,
    LibrarySchema,
    AuthorSchema,
    BookSchemaIn,
    LibrarySchemaIn,
)


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, tags=["root"])
async def root():
    return


@router.get("/book", status_code=status.HTTP_200_OK, tags=["book"])
@inject
async def get_book(
    id: int = None,
    name: str = None,
    book_service: AuthorService = Depends(Provide[Container.book_service]),
) -> BookSchema | list[BookSchema]:
    books = book_service.get_book(id, name)
    if books:
        return books
    raise HTTPException(status_code=404, detail="Book not found.")


@router.post("/book", status_code=status.HTTP_201_CREATED, tags=["book"])
@inject
async def create_book(
    book: BookSchemaIn,
    book_service: AuthorService = Depends(Provide[Container.book_service]),
):
    try:
        return book_service.create_book(book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/book", status_code=status.HTTP_200_OK, tags=["book"])
@inject
async def delete_book(
    id: int,
    book_service: AuthorService = Depends(Provide[Container.book_service]),
):
    try:
        return book_service.delete_book(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/book", status_code=status.HTTP_200_OK, tags=["book"])
@inject
async def update_book(
    id: int,
    book: BookSchemaIn,
    book_service: AuthorService = Depends(Provide[Container.book_service]),
):
    try:
        return book_service.update_book(id, book)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/author", status_code=status.HTTP_200_OK, tags=["author"])
@inject
async def get_author(
    id: int = None,
    name: str = None,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
) -> list[AuthorSchema] | AuthorSchema:
    authors = author_service.get_author(id, name)
    if authors:
        return authors
    raise HTTPException(status_code=404, detail="Author not found.")


@router.post("/author", status_code=status.HTTP_201_CREATED, tags=["author"])
@inject
async def create_author(
    author: AuthorSchemaIn,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    try:
        return author_service.create_author(author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/author", status_code=status.HTTP_200_OK, tags=["author"])
@inject
async def delete_author(
    id: int,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    try:
        return author_service.delete_author(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/author", status_code=status.HTTP_200_OK, tags=["author"])
async def update_author(
    id: int,
    author: AuthorSchemaIn,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
):
    try:
        return author_service.update_author(id, author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/libary", status_code=status.HTTP_200_OK, tags=["library"])
@inject
async def get_libary(
    id: int = None,
    city: str = None,
    library_service: AuthorService = Depends(Provide[Container.library_service]),
) -> LibrarySchema | list[LibrarySchema]:
    library = library_service.get_library(id, city)
    if library:
        return library
    raise HTTPException(status_code=404, detail="Library not found.")


@router.post("/library", status_code=status.HTTP_201_CREATED, tags=["library"])
@inject
async def create_library(
    library: LibrarySchemaIn,
    library_service: AuthorService = Depends(Provide[Container.library_service]),
):
    try:
        return library_service.create_library(library)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/library", status_code=status.HTTP_200_OK, tags=["library"])
@inject
async def delete_library(
    id: int,
    library_service: AuthorService = Depends(Provide[Container.library_service]),
):
    try:
        return library_service.delete_library(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/library", status_code=status.HTTP_200_OK, tags=["library"])
@inject
async def update_library(
    id: int,
    library: LibrarySchemaIn,
    library_service: AuthorService = Depends(Provide[Container.library_service]),
):
    try:
        return library_service.update_library(id, library)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
