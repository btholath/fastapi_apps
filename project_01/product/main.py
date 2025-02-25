from fastapi import FastAPI
import models
from database import engine
from routers import product, seller

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

# include all the routers
app.include_router(product.router)
app.include_router(seller.router)


# Create the tables in the database
models.Base.metadata.create_all(bind=engine)






