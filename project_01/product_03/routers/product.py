from routers.login import get_current_user
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from fastapi import status
import schemas
import models
from typing import List
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED
router = APIRouter(
    tags=["product"],
    prefix="/product",
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add(request: schemas.Product, db: Session = Depends(get_db)):
    # Add a sample product
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

# Query the database
@router.get("/", response_model=List[schemas.DisplayProduct])
def read_product(db: Session = Depends(get_db), current_user:schemas.User = Depends(get_current_user)):
    products = db.query(models.Product).all()
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}")

    return products


@router.get("/{id}", response_model=schemas.DisplayProduct)
def read_product(id: int, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Product with ID: {id} not found")
    return product


@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted!'}


@router.put("/{id}")
def update_product(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=404, detail="Product not found")
    product.update(request.dict())
    db.commit()
    return {"Product updated!"}
