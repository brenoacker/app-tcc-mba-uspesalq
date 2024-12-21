from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.offer.offer_entity import Offer


class OfferRepositoryInterface(ABC):

    @abstractmethod
    def add_offer(self, offer: Offer) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_offer(self, offer_id: int) -> Offer:
        raise NotImplementedError

    @abstractmethod
    def list_offers(self) -> List[Offer]:
        raise NotImplementedError

    @abstractmethod
    def remove_offer(self, offer_id: int) -> None:
        raise NotImplementedError