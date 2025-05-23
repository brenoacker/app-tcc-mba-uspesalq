from abc import ABC, abstractmethod
from typing import List

from domain.offer.offer_entity import Offer


class OfferRepositoryInterface(ABC):

    @abstractmethod
    async def add_offer(self, offer: Offer) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_offer(self, offer_id: int) -> Offer:
        raise NotImplementedError

    @abstractmethod
    async def list_offers(self) -> List[Offer]:
        raise NotImplementedError

    @abstractmethod
    async def remove_offer(self, offer_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_all_offers(self) -> None:
        raise NotImplementedError