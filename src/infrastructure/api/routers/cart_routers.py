import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from infrastructure.api.database import get_session
from infrastructure.cart.sqlalchemy.cart_repository import CartRepository
from infrastructure.cart_item.sqlalchemy.cart_item_repository import \
    CartItemRepository
from infrastructure.product.sqlalchemy.product_repository import \
    ProductRepository
from infrastructure.user.sqlalchemy.user_repository import UserRepository
from usecases.cart.add_cart.add_cart_dto import (AddCartInputDto)
from usecases.cart.add_cart.add_cart_usecase import AddCartUseCase
from usecases.cart.find_cart.find_cart_dto import FindCartInputDto
from usecases.cart.find_cart.find_cart_usecase import FindCartUseCase
from usecases.cart.find_cart_items.find_cart_items_dto import \
    FindCartItemsInputDto
from usecases.cart.find_cart_items.find_cart_items_usecase import \
    FindCartItemsUseCase
from usecases.cart.list_carts.list_carts_dto import ListCartsInputDto
from usecases.cart.list_carts.list_carts_usecase import ListCartsUseCase
from usecases.cart.remove_cart.remove_cart_dto import RemoveCartInputDto
from usecases.cart.remove_cart.remove_cart_usecase import RemoveCartUseCase
from usecases.cart.update_cart.update_cart_dto import UpdateCartInputDto
from usecases.cart.update_cart.update_cart_usecase import UpdateCartUseCase

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", status_code=201, responses={
        201: {
            "description": "Cart added",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "123e4567-e89b-12d3-a456-426614174001",
                        "total_price": 150.50,
                    }
                }
            },
        },
    }
)
def create_cart(request: AddCartInputDto, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        cart_item_repository = CartItemRepository(session=session)
        cart_repository = CartRepository(session=session)
        product_repository = ProductRepository(session=session)
        usecase = AddCartUseCase(cart_repository=cart_repository, cart_item_repository=cart_item_repository, user_repository=user_repository, product_repository=product_repository)
        output = usecase.execute(user_id=user_id, input=AddCartInputDto(items=request.items))
        return output
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.get("/{cart_id}", status_code=200)
def find_cart(cart_id: UUID, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        cart_repository = CartRepository(session=session)
        usecase = FindCartUseCase(cart_repository=cart_repository)
        output = usecase.execute(input=FindCartInputDto(id=cart_id, user_id=user_id))
        return output

    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.get("/{cart_id}/items", status_code=200)
def list_items(cart_id: UUID, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        cart_repository = CartRepository(session=session)
        cart_item_repository = CartItemRepository(session=session)
        usecase = FindCartItemsUseCase(cart_repository=cart_repository, cart_item_repository=cart_item_repository)
        output = usecase.execute(input=FindCartItemsInputDto(cart_id=cart_id, user_id=user_id))
        return output
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/", status_code=200)
def list_carts(user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        cart_repository = CartRepository(session=session)
        usecase = ListCartsUseCase(cart_repository=cart_repository)
        output = usecase.execute(input=ListCartsInputDto(user_id=user_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.delete("/{cart_id}", status_code=204)
def remove_cart(cart_id: UUID, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        cart_repository = CartRepository(session=session)
        usecase = RemoveCartUseCase(cart_repository=cart_repository)
        usecase.execute(input=RemoveCartInputDto(id=cart_id, user_id=user_id))
    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.patch("/{cart_id}", status_code=200)
def update_cart(cart_id: UUID, request: UpdateCartInputDto, user_id: UUID = Header(...), session: Session = Depends(get_session)):
    try:
        cart_repository = CartRepository(session=session)
        cart_item_repository = CartItemRepository(session=session)
        product_repository = ProductRepository(session=session)
        usecase = UpdateCartUseCase(cart_repository=cart_repository, cart_item_repository=cart_item_repository, product_repository=product_repository)
        output = usecase.execute(user_id=user_id, cart_id=cart_id, input=UpdateCartInputDto(items=request.items))
        return output

    except ValueError as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e
    
# @router.delete("/", status_code=204)
# def delete_all_carts(session: Session = Depends(get_session)):
#     try:
#         cart_repository = CartRepository(session=session)
#         usecase = DeleteAllCartsUseCase(cart_repository=cart_repository)
#         usecase.execute()
#         return {"message": "All carts deleted"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) from e