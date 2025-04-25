from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from infrastructure.offer.sqlalchemy.offer_repository import OfferRepository


class RemoveAllOffersUsecase(UseCaseInterface):
    def __init__(self, offer_repository: OfferRepositoryInterface):
        self.offer_repository = offer_repository

    async def execute(self) -> None:

        await self.offer_repository.remove_all_offers()

        return None