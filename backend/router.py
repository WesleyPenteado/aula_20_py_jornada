from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product,
    get_products,
    get_product,
    delete_product,
    update_product,
)

router = APIRouter()

@router.post("/products/", response_model=ProductResponse) # sempre teremos 2 atributos PATH e 
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Rota de criar um produto no banco
    """
    return create_product(db=db, product=product)

@router.get("/products/", response_model=List[ProductResponse])
def read_all_products_route(db: Session = Depends(get_db)):
    """
    Rota de ler todos os produtos
    """
    products = get_products(db)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    """
    Rota de ler um produto específico por ID
    """
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/products/{product_id}", response_model=ProductResponse)
def detele_product_route(product_id: int, db: Session = Depends(get_db)):
    """
    Rota de deletar um produto específico por ID
    """
    db_product = delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    """
    Rota de atualizar um produto específico por ID
    """
    db_product = update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product