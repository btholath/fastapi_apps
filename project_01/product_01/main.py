from urllib import request

from fastapi import FastAPI, HTTPException, Response
from sqlalchemy.sql.functions import mode
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi import status
import schemas
import models
from database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext


app = FastAPI(
    title="Products API",
    description="API for product management",
    version="1.0",
    contact={
        "developer":"818-235-6639",
        "email":"biju.tholath@gmail.com"
    },
    terms_of_service="https://www.bijutholath.com",
    docs_url="/documentation",
)

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    # Create a session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["product"])
async def add(request: schemas.Product, db: Session = Depends(get_db)):
    # Add a sample product
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

# Query the database
@app.get("/product", response_model=List[schemas.DisplayProduct], tags=["product"])
def read_product(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}")

    return products

#@app.get("/product/{id}")
#def read_product(id: int, db: Session = Depends(get_db)):
#    product = db.query(models.Product).filter(models.Product.id == id).first()
#    return product

@app.get("/product/{id}", response_model=schemas.DisplayProduct, tags=["product"])
def read_product(id: int, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Product with ID: {id} not found")
    return product


@app.delete("/product/{id}", tags=["product"])
def delete_product(id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted!'}


@app.put("/product/{id}", tags=["product"])
def update_product(id: int, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(status_code=404, detail="Product not found")
    product.update(request.dict())
    db.commit()
    return {"Product updated!"}



@app.post('/seller', response_model=schemas.DisplaySeller, tags=["seller"])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    # Add a sample product
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return request

