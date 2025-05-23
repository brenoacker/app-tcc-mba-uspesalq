import logging
import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.api.database import get_session
from infrastructure.product.sqlalchemy.product_repository import \
    ProductRepository
from usecases.product.add_product.add_product_dto import AddProductInputDto
from usecases.product.add_product.add_product_usecase import AddProductUseCase
from usecases.product.delete_all_products.delete_all_products_usecase import \
    DeleteAllProductsUseCase
from usecases.product.delete_product.delete_product_dto import \
    DeleteProductInputDto
from usecases.product.delete_product.delete_product_usecase import \
    DeleteProductUseCase
from usecases.product.find_product.find_product_dto import FindProductInputDto
from usecases.product.find_product.find_product_usecase import \
    FindProductUsecase
from usecases.product.list_products.list_products_usecase import \
    ListProductsUseCase
from usecases.product.update_product.update_product_dto import \
    UpdateProductInputDto
from usecases.product.update_product.update_product_usecase import \
    UpdateProductUseCase

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", status_code=201)
async def add_product(request: AddProductInputDto, session: AsyncSession = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        usecase = AddProductUseCase(product_repository=product_repository)
        output = await usecase.execute(input=AddProductInputDto(id=request.id, name=request.name, price=request.price, category=request.category))
        return output
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"{str(e)}\n{error_trace}") from e  
    
@router.get("/", status_code=200)
async def list_products(session: AsyncSession = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        usecase = ListProductsUseCase(product_repository=product_repository)
        output = await usecase.execute()
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e    

@router.get("/{product_id}", status_code=200)
async def find_product(product_id: int, session: AsyncSession = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        usecase = FindProductUsecase(product_repository=product_repository)
        output = await usecase.execute(input=FindProductInputDto(id=product_id))
        return output

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.patch("/{product_id}", status_code=200)
async def update_product(product_id: int, request: UpdateProductInputDto, session: AsyncSession = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        product_found = await product_repository.find_product(product_id=product_id)
        if not product_found:
            raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")
        
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product_found, key, value)

        usecase = UpdateProductUseCase(product_repository=product_repository)
        output = await usecase.execute(
            input=UpdateProductInputDto(
                id=product_found.id,
                name=product_found.name,
                price=product_found.price,
                category=product_found.category
            )
        )
        return output
    except Exception as e:
        error_trace = traceback.format_exc()
        raise HTTPException(status_code=404, detail=f"{str(e)}\n{error_trace}") from e   
    
@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        product_found = await product_repository.find_product(product_id=product_id)
        if not product_found:
            raise HTTPException(status_code=404, detail=f"Product with id '{product_id}' not found")
        
        usecase = DeleteProductUseCase(product_repository=product_repository)
        output = await usecase.execute(input=DeleteProductInputDto(id=product_id))
        
        return output
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    
@router.delete("/", status_code=204)
async def delete_all_products(session: AsyncSession = Depends(get_session)):
    try:
        product_repository = ProductRepository(session=session)
        usecase = DeleteAllProductsUseCase(product_repository=product_repository)
        output = await usecase.execute()
        return output
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e