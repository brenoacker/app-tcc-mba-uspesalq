
import traceback
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infrastructure.api.database import get_session
from infrastructure.product.sqlalchemy.product_repository import \
    ProductRepository
from usecases.product.add_product.add_product_dto import AddProductInputDto
from usecases.product.add_product.add_product_usecase import AddProductUseCase
from usecases.product.delete_product.delete_product_dto import \
    DeleteProductInputDto
from usecases.product.delete_product.delete_product_usecase import \
    DeleteProductUseCase
from usecases.product.find_product.find_product_dto import FindProductInputDto
from usecases.product.find_product.find_product_usecase import \
    FindProductUsecase
from usecases.product.list_products.list_products_dto import \
    ListProductsInputDto
from usecases.product.list_products.list_products_usecase import \
    ListProductsUseCase
from usecases.product.update_product.update_product_dto import \
    UpdateProductInputDto
from usecases.product.update_product.update_product_usecase import \
    UpdateProductUseCase

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", status_code=201)
def add_product(request: AddProductInputDto, session: Session = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        find_product_by_name = product_repository.find_product_by_name(name=request.name)
        if find_product_by_name:
            raise HTTPException(status_code=422, detail=f"Product '{request.name}' already registered")
        usecase = AddProductUseCase(product_repository=product_repository)
        output = usecase.execute(input=AddProductInputDto(name=request.name, price=request.price, category=request.category))
        return output
    except Exception as e:
        raise e
    
@router.get("/", status_code=200)
def list_products(session: Session = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        usecase = ListProductsUseCase(product_repository=product_repository)
        output = usecase.execute()
        return output

    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e
    
@router.get("/{product_id}", status_code=200)
def find_product(product_id: UUID, session: Session = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        usecase = FindProductUsecase(product_repository=product_repository)
        output = usecase.execute(input=FindProductInputDto(id=product_id))
        return output

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found") from e
    
@router.patch("/{product_id}", status_code=200)
def update_product(product_id: UUID, request: UpdateProductInputDto, session: Session = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        product_found = product_repository.find_product(product_id=product_id)
        if not product_found:
            raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product_found, key, value)

        usecase = UpdateProductUseCase(product_repository=product_repository)
        output = usecase.execute(
            product_id=product_id,
            input=UpdateProductInputDto(
            name=product_found.name,
            price=product_found.price,
            category=product_found.category
        ))
        return output
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    
@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: UUID, session: Session = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        product_found = product_repository.find_product(product_id=product_id)
        if not product_found:
            raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")
        
        usecase = DeleteProductUseCase(product_repository=product_repository)
        output = usecase.execute(input=DeleteProductInputDto(id=product_id))
        
        return output
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e