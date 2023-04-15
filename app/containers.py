from dependency_injector import containers, providers
from app.db import Database
from app.services.book import BookService
from app.services.author import AuthorService
from app.services.library import LibraryService
from app.repositories.book import BookRepository
from app.repositories.author import AuthorRepository
from app.repositories.library import LibraryRepository
from dotenv import load_dotenv

load_dotenv()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.routes"])
    config = providers.Configuration()
    config.db.url.from_env("DATABASE_URL")
    db = providers.Singleton(Database, db_url=config.db.url)

    book_repository = providers.Factory(
        BookRepository, session_factory=db.provided.session
    )

    book_service = providers.Factory(
        BookService,
        book_repository=book_repository,
    )

    author_repository = providers.Factory(
        AuthorRepository, session_factory=db.provided.session
    )

    author_service = providers.Factory(
        AuthorService,
        author_repository=author_repository,
    )

    library_repository = providers.Factory(
        LibraryRepository, session_factory=db.provided.session
    )

    library_service = providers.Factory(
        LibraryService,
        library_repository=library_repository,
    )
