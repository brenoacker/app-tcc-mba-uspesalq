import traceback

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.api.database import get_session
from infrastructure.offer.sqlalchemy.offer_repository import OfferRepository
from usecases.offer.add_offer.add_offer_dto import AddOfferInputDto
from usecases.offer.add_offer.add_offer_usecase import AddOfferUseCase
from usecases.offer.find_offer.find_offer_dto import FindOfferInputDto
from usecases.offer.find_offer.find_offer_usecase import FindOfferUseCase
from usecases.offer.list_offers.list_offers_usecase import ListOffersUseCase
from usecases.offer.remove_all_offers.remove_all_offers_usecase import \
    RemoveAllOffersUsecase
from usecases.offer.remove_offer.remove_offer_dto import RemoveOfferInputDto
from usecases.offer.remove_offer.remove_offer_usecase import RemoveOfferUseCase

router = APIRouter(prefix="/offer", tags=["Offer"])

@router.post("/", status_code=201)
async def add_offer(request: AddOfferInputDto, session: AsyncSession = Depends(get_session)):
    try:
        offer_repository = OfferRepository(session=session)
        usecase = AddOfferUseCase(offer_repository=offer_repository)
        output = await usecase.execute(input=AddOfferInputDto(id=request.id, expiration_days=request.expiration_days ,discount_type=request.discount_type, discount_value=request.discount_value))
        return output
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e  
    
@router.get("/", status_code=200)
async def list_offers(session: AsyncSession = Depends(get_session)):
    try:
        offer_repository = OfferRepository(session=session)
        usecase = ListOffersUseCase(offer_repository=offer_repository)
        output = await usecase.execute()
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/{offer_id}", status_code=200)
async def find_offer(offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        offer_repository = OfferRepository(session=session)
        usecase = FindOfferUseCase(offer_repository=offer_repository)
        output = await usecase.execute(input=FindOfferInputDto(id=offer_id))
        return output
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.delete("/{offer_id}", status_code=204)
async def remove_offer(offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        offer_repository = OfferRepository(session=session)
        usecase = RemoveOfferUseCase(offer_repository=offer_repository)
        await usecase.execute(input=RemoveOfferInputDto(id=offer_id))
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.delete("/", status_code=204)
def remove_all_offers(session: AsyncSession = Depends(get_session)):
    try:
        offer_repository = OfferRepository(session=session)
        usecase = RemoveAllOffersUsecase(offer_repository=offer_repository)
        usecase.execute()
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e