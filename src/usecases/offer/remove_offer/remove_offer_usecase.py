from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from usecases.offer.remove_offer.remove_offer_dto import RemoveOfferInputDto


class RemoveOfferUseCase(UseCaseInterface):

    def __init__(self, offer_repository: OfferRepositoryInterface):
        self.offer_repository = offer_repository

    def execute(self, input: RemoveOfferInputDto) -> None:

        offer = self.offer_repository.find_offer(input.id)
        if offer is None:
            raise ValueError(f"Offer with id {input.id} not found")

        self.offer_repository.remove_offer(offer.id)

        return None