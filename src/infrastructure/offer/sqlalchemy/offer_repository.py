from typing import List

from sqlalchemy.orm.session import Session

from domain.offer.offer_entity import Offer
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from infrastructure.offer.sqlalchemy.offer_model import OfferModel


class OfferRepository(OfferRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def add_offer(self, offer: Offer) -> Offer:

        offer_model = OfferModel(
            id=offer.id,
            start_date=offer.start_date,
            end_date=offer.end_date,
            discount_type=offer.discount_type,
            discount_value=offer.discount_value
        )

        self.session.add(offer_model)
        self.session.commit()

        added_offer = Offer(
            id=offer_model.id,
            start_date=offer_model.start_date,
            end_date=offer_model.end_date,
            discount_type=offer_model.discount_type,
            discount_value=offer_model.discount_value
        )

        return added_offer

    def find_offer(self, offer_id: int) -> Offer:
        offer_in_db = self.session.query(OfferModel).filter(OfferModel.id == offer_id).first()
        
        if not offer_in_db:
            return None

        offer = Offer(
            id=offer_in_db.id,
            start_date=offer_in_db.start_date,
            end_date=offer_in_db.end_date,
            discount_type=offer_in_db.discount_type,
            discount_value=offer_in_db.discount_value
        )

        return offer

    def list_offers(self) -> List[Offer]:
        offers_in_db = self.session.query(OfferModel).all()

        if not offers_in_db:
            return None
        
        offers = [
            Offer(
                id=offer.id,
                start_date=offer.start_date,
                end_date=offer.end_date,
                discount_type=offer.discount_type,
                discount_value=offer.discount_value
            )
            for offer in offers_in_db
        ]

        return offers

    def remove_offer(self, offer_id: int) -> None:

        self.session.query(OfferModel).filter(OfferModel.id == offer_id).delete()
        self.session.commit()

        return None
    
    def remove_all_offers(self) -> None:
        
        self.session.query(OfferModel).delete()
        self.session.commit()

        return None