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
    UserSchemaIn,
    UserSchema,
    RentalSchema,
    RentalSchemaIn,
)
from app.repositories.password_managment import verify_password
from fastapi.security import OAuth2PasswordBearer
import datetime
from dotenv import load_dotenv
from os import environ
import jwt

router = APIRouter()

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    data.update({"exp": expiration})
    token = jwt.encode(
        data,
        str(environ.get("SECRET_KEY")),
        algorithm=str(environ.get("ALGORITHM")),
    )
    return token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token,
            str(environ.get("SECRET_KEY")),
            algorithms=[str(environ.get("ALGORITHM"))],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    return payload


@router.get("/", status_code=status.HTTP_200_OK, tags=["root"])
async def root():
    return


@router.post("/token")
@inject
async def generate_token(
    email: str,
    password: str,
    user_service: AuthorService = Depends(Provide[Container.user_service]),
):
    user = user_service.get_user(email=email)
    if user:
        user = user[0]
    else:
        raise HTTPException(404, detail="User not found")
    if verify_password(password, user.password):
        if user.is_active:
            user_data = {
                "id": user.id,
                "name": user.email,
                "is_superuser": user.is_superuser,
            }
            token = create_jwt_token(user_data)
            return {"access_token": token, "token_type": "bearer"}
        raise HTTPException(401, detail="User is not active")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


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


@router.get("/user", status_code=status.HTTP_200_OK, tags=["user"])
@inject
async def get_user(
    id: int = None,
    name: str = None,
    user_service: AuthorService = Depends(Provide[Container.user_service]),
):
    users = user_service.get_user(id, name)
    if users:
        return users
    raise HTTPException(status_code=404, detail="User not found.")


@router.post("/user", status_code=status.HTTP_201_CREATED, tags=["user"])
@inject
async def create_user(
    user: UserSchemaIn,
    user_service: AuthorService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/user", status_code=status.HTTP_200_OK, tags=["user"])
@inject
async def update_user(
    id: int,
    user: UserSchemaIn,
    user_service: AuthorService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.update_user(id, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/user", status_code=status.HTTP_200_OK, tags=["user"])
@inject
async def delete_user(
    id: int,
    user_service: AuthorService = Depends(Provide[Container.user_service]),
):
    try:
        return user_service.delete_user(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rental", status_code=status.HTTP_200_OK, tags=["rental"])
@inject
async def get_rental(
    id: int = None,
    user_id: int = None,
    rental_service: AuthorService = Depends(Provide[Container.rental_service]),
    token: str = Depends(oauth2_scheme),
):
    rentals = rental_service.get_rental(id, user_id)
    if rentals:
        return rentals
    raise HTTPException(status_code=404, detail="Rental not found.")


@router.post("/rental", status_code=status.HTTP_201_CREATED, tags=["rental"])
@inject
async def create_rental(
    rental: RentalSchemaIn,
    rental_service: AuthorService = Depends(Provide[Container.rental_service]),
    token: str = Depends(oauth2_scheme),
):
    try:
        data = await get_current_user(token)
        rental = rental.copy(update={"user_id": data["id"]})
        return rental_service.create_rental(rental)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/rental", status_code=status.HTTP_200_OK, tags=["rental"])
@inject
async def update_rental(
    id: int,
    rental: RentalSchemaIn,
    rental_service: AuthorService = Depends(Provide[Container.rental_service]),
):
    try:
        return rental_service.update_rental(id, rental)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/rental", status_code=status.HTTP_200_OK, tags=["rental"])
@inject
async def delete_rental(
    id: int,
    rental_service: AuthorService = Depends(Provide[Container.rental_service]),
):
    try:
        return rental_service.delete_rental(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
