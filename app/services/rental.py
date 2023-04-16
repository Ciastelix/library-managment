from app.models import Rental
from app.repositories.rental import RentalRepository
from app.schemas import RentalSchemaIn


class RentalService:
    def __init__(self, rental_repository: RentalRepository) -> None:
        self._repository: RentalRepository = rental_repository

    def get_rental(self, id: int = None, user_id: str = None) -> list[Rental]:
        if id:
            return self._repository.get_by_id(id)
        elif user_id:
            return self._repository.get_by_user(user_id)
        else:
            return self._repository.get_all()

    def create_rental(self, rental: RentalSchemaIn) -> Rental:
        return self._repository.add(rental)

    def delete_rental(self, id: int) -> Rental:
        return self._repository.delete(id)

    def update_rental(self, id: int, rental: RentalSchemaIn) -> Rental:
        return self._repository.update(id, rental)
