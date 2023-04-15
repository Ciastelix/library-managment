from app.models import Library
from app.repositories.library import LibraryRepository
from app.schemas import LibrarySchemaIn


class LibraryService:
    def __init__(self, library_repository: LibraryRepository) -> None:
        self._repository: LibraryRepository = library_repository

    def get_library(self, id: int = None, name: str = None) -> list[Library]:
        if id:
            return self._repository.get_by_id(id)
        elif name:
            return self._repository.get_by_name(name)
        else:
            return self._repository.get_all()

    def create_library(self, library: LibrarySchemaIn) -> Library:
        return self._repository.add(library)

    def delete_library(self, id: int) -> Library:
        return self._repository.delete(id)

    def update_library(self, id: int, library: LibrarySchemaIn) -> Library:
        return self._repository.update(id, library)
