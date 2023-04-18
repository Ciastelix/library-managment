from fastapi import APIRouter, status, HTTPException, Depends
from app.services.author import AuthorService
from app.services.book import BookService
from app.services.library import LibraryService
from app.services.user import UserService
from app.services.rental import RentalService
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


def create_jwt_token(data: dict) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    data.update({"exp": expiration})
    token = jwt.encode(
        data,
        str(environ.get("SECRET_KEY")),
        algorithm=str(environ.get("ALGORITHM")),
    )
    return token


def decode_jwt_token(token: str) -> dict[str, str]:
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
    user_service: UserService = Depends(Provide[Container.user_service]),
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
    id: str = None,
    name: str = None,
    book_service: BookService = Depends(Provide[Container.book_service]),
) -> BookSchema | list[BookSchema]:
    books = book_service.get_book(id, name)
    if books:
        return books
    raise HTTPException(status_code=404, detail="Book not found.")


@router.post("/book", status_code=status.HTTP_201_CREATED, tags=["book"])
@inject
async def create_book(
    book: BookSchemaIn,
    book_service: BookService = Depends(Provide[Container.book_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return book_service.create_book(book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/book", status_code=status.HTTP_200_OK, tags=["book"])
@inject
async def delete_book(
    id: str,
    book_service: BookService = Depends(Provide[Container.book_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return book_service.delete_book(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.put("/book", status_code=status.HTTP_200_OK, tags=["book"])
@inject
async def update_book(
    id: str,
    book: BookSchemaIn,
    book_service: BookService = Depends(Provide[Container.book_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return book_service.update_book(id, book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/author", status_code=status.HTTP_200_OK, tags=["author"])
@inject
async def get_author(
    id: str = None,
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
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return author_service.create_author(author)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.delete("/author", status_code=status.HTTP_200_OK, tags=["author"])
@inject
async def delete_author(
    id: str,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return author_service.delete_author(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.put("/author", status_code=status.HTTP_200_OK, tags=["author"])
async def update_author(
    id: str,
    author: AuthorSchemaIn,
    author_service: AuthorService = Depends(Provide[Container.author_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return author_service.update_author(id, author)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/library", status_code=status.HTTP_200_OK, tags=["library"])
@inject
async def get_library(
    id: str = None,
    city: str = None,
    library_service: LibraryService = Depends(Provide[Container.library_service]),
) -> LibrarySchema | list[LibrarySchema]:
    library = library_service.get_library(id, city)
    if library:
        return library
    raise HTTPException(status_code=404, detail="Library not found.")


@router.post("/library", status_code=status.HTTP_201_CREATED, tags=["library"])
@inject
async def create_library(
    library: LibrarySchemaIn,
    library_service: LibraryService = Depends(Provide[Container.library_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return library_service.create_library(library)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=403, detail="Forbidden")


@router.delete("/library", status_code=status.HTTP_200_OK, tags=["library"])
@inject
async def delete_library(
    id: str,
    library_service: LibraryService = Depends(Provide[Container.library_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return library_service.delete_library(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=403, detail="Forbidden")


@router.put("/library", status_code=status.HTTP_200_OK, tags=["library"])
@inject
async def update_library(
    id: str,
    library: LibrarySchemaIn,
    library_service: LibraryService = Depends(Provide[Container.library_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"]:
        try:
            return library_service.update_library(id, library)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/user", status_code=status.HTTP_200_OK, tags=["user"])
@inject
async def get_user(
    id: str = None,
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
    id: str,
    userUpdate: UserSchemaIn,
    user_service: AuthorService = Depends(Provide[Container.user_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"] or id == user["id"]:
        try:
            return user_service.update_user(id, userUpdate)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=403, detail="You can't update this user.")


@router.delete("/user", status_code=status.HTTP_200_OK, tags=["user"])
@inject
async def delete_user(
    id: str,
    user_service: RentalService = Depends(Provide[Container.user_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["is_superuser"] or id == user["id"]:
        try:
            return user_service.delete_user(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=403, detail="You can't delete this user.")


@router.get("/rental", status_code=status.HTTP_200_OK, tags=["rental"])
@inject
async def get_rental(
    id: str = None,
    rental_service: RentalService = Depends(Provide[Container.rental_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    rentals = rental_service.get_rental(id, user["id"])
    if rentals:
        if user["is_superuser"] or rentals[0].user_id == user["id"]:
            return rentals
        raise HTTPException(
            status_code=403, detail="You are not allowed to see this rental."
        )
    raise HTTPException(status_code=404, detail="Rental not found.")


@router.post("/rental", status_code=status.HTTP_201_CREATED, tags=["rental"])
@inject
async def create_rental(
    rental: RentalSchemaIn,
    rental_service: RentalService = Depends(Provide[Container.rental_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    try:
        rental = rental.copy(update={"user_id": user["id"]})
        return rental_service.create_rental(rental)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/rental", status_code=status.HTTP_200_OK, tags=["rental"])
@inject
async def update_rental(
    id: str,
    rental: RentalSchemaIn,
    rental_service: RentalService = Depends(Provide[Container.rental_service]),
    token: str = Depends(oauth2_scheme),
):
    user = await get_current_user(token)
    if user["id"] == rental_service.get_rental(id)[0].user_id or user["is_superuser"]:
        try:
            return rental_service.update_rental(id, rental)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=400, detail="You can't update other user's rental.")


@router.delete("/rental", status_code=status.HTTP_200_OK, tags=["rental"])
@inject
async def delete_rental(
    id: str,
    rental_service: AuthorService = Depends(Provide[Container.rental_service]),
    user: dict = Depends(get_current_user),
):
    if user["id"] == id:
        try:
            return rental_service.delete_rental(id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(status_code=400, detail="You can't delete other user's rental.")
