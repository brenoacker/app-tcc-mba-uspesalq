from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.offer.offer_entity import Offer
from domain.offer.offer_repository_interface import OfferRepositoryInterface
from infrastructure.api.cache import async_cached
from infrastructure.offer.sqlalchemy.offer_model import OfferModel


class OfferRepository(OfferRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_offer(self, offer: Offer) -> Offer:

        offer_model = OfferModel(
            id=offer.id,
            start_date=offer.start_date,
            end_date=offer.end_date,
            discount_type=offer.discount_type,
            discount_value=offer.discount_value
        )

        self.session.add(offer_model)
        await self.session.commit()
        await self.session.refresh(offer_model)

        added_offer = Offer(
            id=offer_model.id,
            start_date=offer_model.start_date,
            end_date=offer_model.end_date,
            discount_type=offer_model.discount_type,
            discount_value=offer_model.discount_value
        )

        return added_offer

    @async_cached(ttl=600, prefix='offer')
    async def find_offer(self, offer_id: int) -> Offer:
        result = await self.session.execute(
            select(OfferModel).filter(OfferModel.id == offer_id)
        )
        offer_in_db = result.scalars().first()
        
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

    @async_cached(ttl=600, prefix='offer')
    async def list_offers(self) -> List[Offer]:
        result = await self.session.execute(select(OfferModel))
        offers_in_db = result.scalars().all()

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

    async def remove_offer(self, offer_id: int) -> None:
        stmt = select(OfferModel).filter(OfferModel.id == offer_id)
        result = await self.session.execute(stmt)
        offer = result.scalars().first()
        
        if offer:
            await self.session.delete(offer)
            await self.session.commit()

        return None
        
    async def remove_all_offers(self) -> None:
        await self.session.execute("DELETE FROM tb_offers")
        await self.session.commit()
        return None