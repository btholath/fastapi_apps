from fastapi import FastAPI, Body, Form
from pydantic import BaseModel, Field, model_validator, HttpUrl
from typing import Set, Optional, List
from uuid import UUID
from datetime import date, datetime, time, timedelta


class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta


# --- Profile model and endpoint ---
class Profile(BaseModel):
    name: str
    email: str
    age: int

class Image(BaseModel):
    url: HttpUrl
    name: str



# --- Product model with computed field ---
class Product(BaseModel):
    name: str
    price: int = Field(gt=0, title="Price of the item", description="Price must be greater than zero")
    discount: int = Field(ge=0, lt=100, description="Discount percentage from 0 to 100")
    discounted_price: Optional[int] = None
    tags: Set[str] = Field(example="[electronics, phones]")
    image: List[Image]

    @model_validator(mode="after")
    def compute_discounted_price(cls, m: "Product") -> "Product":
        if m.price is not None and m.discount is not None:
            m.discounted_price = int(m.price - (m.price * m.discount / 100))
        return m

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Phone",
                "price": 100,
                "discount": 100,
                "discounted_price": 0,
                "tags": ["electronics", "computers"],
                "image": [
                    {"url": "https://www.google.com", "name": "phone image"},
                    {"url": "https://www.google.com", "name": "phone image side view"}
                ]
            }
        }

class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product]

class User(BaseModel):
    name: str
    email: str

# --- Combined Purchase Model ---
class Purchase(BaseModel):
    user: User
    product: Product
app = FastAPI()

@app.get("/hello")
def index():
    return {"message": "Hello World"}

@app.get("/")
async def root():
    return {"message": "Hello Root"}

@app.get('/products/')
def products(id: int = 10, price: int = 100):
    # Example: http://localhost:8000/products/?id=10&price=200
    return {"message": f"Product with an id {id} and price: {price}"}

@app.get('/profile/{userid}/comments/')
def profile(userid: int, commentid: int):
    # Example: http://localhost:8000/profile/101/comments/?commentid=1
    return {"message": f"Profile page for user with userid {userid} and comment with id {commentid}"}

@app.post('/adduser')
def adduser():
    # POST http://localhost:8000/adduser
    return {"user": {"name": "johns", "email": "johns@example.com"}}


@app.post('/profile/')
def create_profile(profile: Profile):
    # POST http://localhost:8000/profile/
    # Body example: {"name": "Johns", "email": "johns@example.com", "age": 25}
    return profile





@app.post('/purchase/')
def purchase(purchase: Purchase):
    # The request body should have a nested structure:
    # {
    #   "user": {"name": "Alice", "email": "alice@example.com"},
    #   "product": {"name": "Laptop", "price": 1000, "discount": 10, "tags": ["electronics"]}
    # }
    return purchase

# --- Merged addproduct Endpoint ---
@app.post('/addproduct/{product_id}')
def addproduct(product_id: int, product: Product, category: Optional[str] = None):
    """
    Endpoint to add a product.
    - **product_id**: The ID of the product.
    - **product**: Product details.
    - **category**: Optional product category.
    """
    # The discounted_price is auto-computed by the model validator.
    response = {'product_id': product_id, 'product': product.dict()}
    if category:
        response['category'] = category
    return response


@app.post('/addevent')
def addevent(event: Event):
    return event

@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}
