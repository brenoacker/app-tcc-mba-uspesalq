from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from infrastructure.api.cache import async_cached, invalidate_cache
from infrastructure.product.sqlalchemy.product_model import ProductModel
from usecases.product.list_products.list_products_dto import ListProductsDto


class ProductRepository(ProductRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    @invalidate_cache(key_prefix='product')
    async def add_product(self, product: Product) -> ProductModel:
        
        product_model = ProductModel(id=product.id, name=product.name, price=product.price, category=product.category)
        
        self.session.add(product_model)
        await self.session.commit()
        await self.session.refresh(product_model)
        
        return product_model
    
    @async_cached(ttl=600, prefix='product')  # Cache por 10 minutos
    async def find_product(self, product_id: int) -> Optional[Product]:
        
        result = await self.session.execute(select(ProductModel).filter(ProductModel.id == product_id))
        product_in_db = result.scalars().first()
        
        if not product_in_db:
            return None
        
        product = Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=product_in_db.category)
        
        return product
    
    @async_cached(ttl=600, prefix='product')  # Cache por 10 minutos
    async def find_product_by_name(self, name: str) -> Optional[Product]:
        
        result = await self.session.execute(select(ProductModel).filter(ProductModel.name == name))
        product_in_db = result.scalars().first()
        
        if not product_in_db:
            return None
        
        product = Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=product_in_db.category)
        
        return product
    
    @async_cached(ttl=600, prefix='product')  # Cache por 10 minutos
    async def find_product_by_code(self, product_code: int) -> Optional[Product]:
        '''Find a product by its code'''
        
        result = await self.session.execute(select(ProductModel).filter(ProductModel.product_code == product_code))
        product_in_db = result.scalars().first()
        
        if not product_in_db:
            return None
        
    #     product = Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=product_in_db.category)
        
    #     return product
    
    @invalidate_cache(key_prefix='product')
    async def update_product(self, product: Product) -> None:
        
        stmt = select(ProductModel).filter(ProductModel.id == product.id)
        result = await self.session.execute(stmt)
        product_model = result.scalars().first()
        
        if product_model:
            product_model.name = product.name
            product_model.price = product.price
            product_model.category = product.category
            await self.session.commit()
        
        return None
    
    @async_cached(ttl=300, prefix='product')  # Cache por 5 minutos
    async def list_products(self) -> List[Product]:

        result = await self.session.execute(select(ProductModel))
        products_in_db = result.scalars().all()

        products = []

        for product_in_db in products_in_db:
            category = ProductCategory(product_in_db.category)
            products.append(Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=category))

        products_dicts = [product.__dict__ for product in products]
        products_dto = [ListProductsDto(**product_dict) for product_dict in products_dicts]

        return products_dto
    
    @invalidate_cache(key_prefix='product')
    async def delete_product(self, product_id: UUID) -> None:
        
        stmt = select(ProductModel).filter(ProductModel.id == product_id)
        result = await self.session.execute(stmt)
        product_model = result.scalars().first()
        
        if product_model:
            await self.session.delete(product_model)
            await self.session.commit()
        
        return None
    
    @invalidate_cache(key_prefix='product')
    async def delete_all_products(self) -> int:
        
        result = await self.session.execute(select(ProductModel))
        products = result.scalars().all()
        
        count = 0
        for product in products:
            await self.session.delete(product)
            count += 1
        
        await self.session.commit()
        
        return count