from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from infrastructure.logging_config import logger
from usecases.offer.find_offer.find_offer_dto import (FindOfferInputDto,
                                                      FindOfferOutputDto)


class FindOfferUseCase(UseCaseInterface):
    def __init__(self, offer_repository: OfferRepositoryInterface):	
        self.offer_repository = offer_repository

    def execute(self, input: FindOfferInputDto) -> FindOfferOutputDto:
        offer = self.offer_repository.find_offer(offer_id=input.id)

        if offer is None:
            return ValueError(f"Offer with id '{input.id}' not found")
        
        return offer