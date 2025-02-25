
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt
import schemas
import models
import database
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from schemas import TokenData

# JWT variables
SECRET_KEY = "ed383250ab5e129d78b449d4856cbb096e96dd3f4eb775ec760b25f5a9fffe33"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found/invalid username")

    print(f"request.password: {request.password}")
    print(f"user.password: {user.password}")

    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    # Generate JWT token
    access_token = generate_token(data={"sub": user.username})
    print(f"access_token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}



def get_current_user(token:str=Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload_jwt.get('sub')
        if username is None:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    return token_data
