from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from usecases.offer.list_offers.list_offers_dto import (ListOffersOutputDto,
                                                        OfferDto)


class ListOffersUseCase(UseCaseInterface):
    def __init__(self, offer_repository: OfferRepositoryInterface):
        self.offer_repository = offer_repository

    async def execute(self) -> ListOffersOutputDto:
        
        offers = await self.offer_repository.list_offers()

        if not offers:
            return ListOffersOutputDto(offers=[])
        
        return ListOffersOutputDto(offers=[OfferDto(id=offer.id, start_date=offer.start_date, end_date=offer.end_date, discount_type=offer.discount_type, discount_value=offer.discount_value) for offer in offers])