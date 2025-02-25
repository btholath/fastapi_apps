from pydantic import BaseModel



class Seller(BaseModel):
    username: str
    email: str
    password: str



class DisplaySeller(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True

class Product(BaseModel):
    name: str
    description: str
    price: float


# The response body will now show only name and description and not price
class DisplayProduct(BaseModel):
    name: str
    description: str
    seller: DisplaySeller
    class Config:
        orm_mode = True
