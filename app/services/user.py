from app.models import User
from app.repositories.user import UserRepository
from app.schemas import UserSchemaIn


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_user(
        self, id: int = None, name: str = None, email: str = None
    ) -> list[User]:
        if id:
            return self._repository.get_by_id(id)
        elif name:
            return self._repository.get_by_name(name)
        elif email:
            return self._repository.get_by_email(email)
        else:
            return self._repository.get_all()

    def create_user(self, user: UserSchemaIn) -> User:
        return self._repository.add(user)

    def delete_user(self, id: int) -> User:
        return self._repository.delete(id)

    def update_user(self, id: int, user: UserSchemaIn) -> User:
        return self._repository.update(id, user)
