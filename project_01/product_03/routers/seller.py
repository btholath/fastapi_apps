from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from fastapi import status
import schemas
import models
from typing import List
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from passlib.context import CryptContext


router = APIRouter(
    tags=["seller"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/seller', response_model=schemas.DisplaySeller )
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    # Add a sample product
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return request

