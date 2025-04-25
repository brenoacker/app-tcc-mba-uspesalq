from datetime import datetime, timedelta

import requests

from domain.__seedwork.use_case_interface import UseCaseInterface
from domain.offer.offer_entity import Offer
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from usecases.offer.add_offer.add_offer_dto import (AddOfferInputDto,
                                                    AddOfferOutputDto)


class AddOfferUseCase(UseCaseInterface):

    def __init__(self, offer_repository: OfferRepositoryInterface):
        self.offer_repository = offer_repository

    async def execute(self, input: AddOfferInputDto) -> AddOfferOutputDto:
        
        found_offer = await self.offer_repository.find_offer(offer_id=input.id)

        # # Call the API to find the offer
        # response = requests.get(f"http://localhost:8000/offer/{input.id}")
        
        # if response.status_code == 200:
        #     found_offer = response.json()
        # elif response.status_code == 404:
        #     found_offer = None
        # else:
        #     response.raise_for_status()

        if found_offer is not None:
            raise ValueError(f"Offer with id {input.id} already exists")
    
        if input.expiration_days <= 0:
            raise ValueError("Expiration days must be greater than 0")
        
        start_date = datetime.now()
        end_date = datetime.now() + timedelta(days=input.expiration_days)

        added_offer = await self.offer_repository.add_offer(offer=Offer(id=input.id, start_date=start_date, end_date=end_date, discount_type=input.discount_type, discount_value=input.discount_value))
        
        return AddOfferOutputDto(id=added_offer.id, discount_type=added_offer.discount_type, discount_value=added_offer.discount_value, start_date=added_offer.start_date, end_date=added_offer.end_date)