from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.api.database import get_session
from infrastructure.cart_item.sqlalchemy.cart_item_repository import \
    CartItemRepository
from infrastructure.user.sqlalchemy.user_repository import UserRepository
from usecases.cart_item.add_item.add_item_dto import AddItemInputDto
from usecases.cart_item.add_item.add_item_usecase import AddItemUseCase
from usecases.cart_item.find_item.find_item_dto import FindItemInputDto
from usecases.cart_item.find_item.find_item_usecase import FindItemUseCase
from usecases.cart_item.list_items.list_items_usecase import ListItemsUseCase
from usecases.cart_item.remove_item.remove_item_dto import RemoveItemInputDto
from usecases.cart_item.remove_item.remove_item_usecase import \
    RemoveItemUseCase
from usecases.cart_item.update_item.update_item_dto import UpdateItemInputDto
from usecases.cart_item.update_item.update_item_usecase import \
    UpdateItemUseCase
from usecases.user.find_user.find_user_dto import FindUserInputDto
from usecases.user.find_user.find_user_usecase import FindUserUseCase

router = APIRouter(prefix="/cart_items", tags=["CartItems"])

@router.post("/", status_code=201)
def add_cart_item(request: AddItemInputDto, session: Session = Depends(get_session)):
    try:
        user_repository = UserRepository(session=session)
        usecase = FindUserUseCase(user_repository=user_repository)
        user_found = usecase.execute(input=FindUserInputDto(id=request.user_id))
        if not user_found:
            raise HTTPException(status_code=404, detail=f"User with id '{request.user_id}' not found")
        cart_item_repository = CartItemRepository(session=session)
        find_item = cart_item_repository.find_item(cart_item_id=request.id)
        if find_item:
            usecase = UpdateItemUseCase(cart_item_repository=cart_item_repository)
            find_item.quantity += request.quantity
            output = usecase.execute(input=UpdateItemInputDto(id=find_item.id, quantity=find_item.quantity))
            return output
        usecase = AddItemUseCase(cart_item_repository=cart_item_repository)
        output = usecase.execute(input=AddItemInputDto(id=request.id, user_id=request.user_id, product_id=request.product_id, quantity=request.quantity))
        return output
    except Exception as e:
        raise e
    
@router.get("/{cart_item_id}", status_code=200)
def find_cart_item(cart_item_id: UUID, session: Session = Depends(get_session)):
    try:
        cart_item_repository = CartItemRepository(session=session)
        usecase = FindItemUseCase(cart_item_repository=cart_item_repository)
        output = usecase.execute(input=FindItemInputDto(id=cart_item_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"CartItem with id '{cart_item_id}' not found") from e
    
@router.patch("/{cart_item_id}", status_code=200)
def update_cart_item(cart_item_id: UUID, request: UpdateItemInputDto, session: Session = Depends(get_session)):
    try:
        cart_item_repository = CartItemRepository(session=session)
        usecase = UpdateItemUseCase(cart_item_repository=cart_item_repository)
        output = usecase.execute(input=UpdateItemInputDto(id=cart_item_id, quantity=request.quantity))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"CartItem with id '{cart_item_id}' not found") from e
    
@router.delete("/{cart_item_id}", status_code=204)
def remove_cart_item(cart_item_id: UUID, session: Session = Depends(get_session)):
    try:
        cart_item_repository = CartItemRepository(session=session)
        cart_item_found = cart_item_repository.find_item(cart_item_id=cart_item_id)
        if not cart_item_found:
            raise HTTPException(status_code=404, detail=f"CartItem with id '{cart_item_id}' not found")
        usecase = RemoveItemUseCase(cart_item_repository=cart_item_repository)
        output = usecase.execute(input=RemoveItemInputDto(id=cart_item_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"CartItem with id '{cart_item_id}' not found") from e
    
@router.get("/", status_code=200)
def list_cart_items(session: Session = Depends(get_session)):
    try:
        cart_item_repository = CartItemRepository(session=session)
        usecase = ListItemsUseCase(cart_item_repository=cart_item_repository)
        output = usecase.execute()

        return output
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e