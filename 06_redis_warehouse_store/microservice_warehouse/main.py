from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel, BaseConfig

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)

redis = get_redis_connection(
  host='localhost',
  port=6380,
  decode_responses=True
)

class Product(HashModel):
  name: str
  price: float
  quantity: int

  class Meta:
    database = redis

  class Config:
    arbitrary_types_allowed = True



class ProductInput(BaseModel):
  name: str
  price: float
  quantity: int

  # Define a test endpoint to check Redis connectivity
@app.get("/test-redis")
async def test_redis_connection():
    try:
        if redis.ping():
            return {"message": "Successfully connected to Redis"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis connection failed: {str(e)}")

@app.post('/product', tags=['warehouse'])
def create(product: ProductInput):
  product_obj = Product(
    name=product.name,
    price=product.price,
    quantity=product.quantity
  )
  return product_obj.save()

@app.get('/product/{pk}', tags=['warehouse'])
def get(pk: str):
  return Product.get(pk)

@app.get('/products', tags=['warehouse'])
def all():
  # return Product.all_pks()
  return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
  product = Product.get(pk)
  return {
    'id': product.pk,
    'name': product.name,
    'price': product.price,
    'quantity': product.quantity
  }

@app.delete('/product/{pk}', tags=['warehouse'])
def delete(pk: str):
  return Product.delete(pk)