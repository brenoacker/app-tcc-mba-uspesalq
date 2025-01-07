from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm.session import Session

from domain.product.product_category_enum import ProductCategory
from domain.product.product_entity import Product
from domain.product.product_repository_interface import \
    ProductRepositoryInterface
from infrastructure.product.sqlalchemy.product_model import ProductModel
from usecases.product.list_products.list_products_dto import ListProductsDto


class ProductRepository(ProductRepositoryInterface):

    def __init__(self, session: Session):
        self.session: Session = session

    def add_product(self, product: Product) -> ProductModel:
        
        product_model = ProductModel(id=product.id, name=product.name, price=product.price, category=product.category)
        
        self.session.add(product_model)
        self.session.commit()
        self.session.refresh(product_model)
        
        return product_model
    
    def find_product(self, product_id: int) -> Optional[Product]:
        
        product_in_db: ProductModel = self.session.query(ProductModel).get(product_id)
        if not product_in_db:
            return None
        
        product = Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=product_in_db.category)
        
        return product
    
    def find_product_by_name(self, name: str) -> Optional[Product]:
        
        product_in_db: ProductModel = self.session.query(ProductModel).filter(ProductModel.name == name).first()
        if not product_in_db:
            return None
        
        product = Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=product_in_db.category)
        
        return product
    
    # def find_product_by_code(self, product_code: int) -> Optional[Product]:
    #     '''Find a product by its code'''
    #     # Create code that filters the product by product_code without the id

    #     product_in_db: ProductModel = self.session.query(ProductModel).filter(ProductModel.product_code == product_code).first()
        
        
    #     # product_in_db: ProductModel = self.session.query(ProductModel).filter(ProductModel.product_code == product_code).first()
    #     if not product_in_db:
    #         return None
        
    #     product = Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=product_in_db.category)
        
    #     return product
    
    def update_product(self, product: Product) -> None:
        
        self.session.query(ProductModel).filter(ProductModel.id == product.id).update(
            {
                "name": product.name,
                "price": product.price,
                "category": product.category
            }
        )
        self.session.commit()
        
        return None
    
    def list_products(self) -> List[Product]:

        products_in_db = self.session.query(ProductModel).all()

        products = []

        for product_in_db in products_in_db:
            category = ProductCategory(product_in_db.category)
            products.append(Product(id=product_in_db.id, name=product_in_db.name, price=product_in_db.price, category=category))

        products_dicts = [product.__dict__ for product in products]
        products_dto = [ListProductsDto(**product_dict) for product_dict in products_dicts]

        return products_dto
    
    def delete_product(self, product_id: UUID) -> None:
        
        self.session.query(ProductModel).filter(ProductModel.id == product_id).delete()
        self.session.commit()
        
        return None
    
    def delete_all_products(self) -> None:
        
        self.session.query(ProductModel).delete()
        self.session.commit()
        
        return None