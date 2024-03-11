from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"]
)

redis = get_redis_connection(
    host="redis-19196.c10.us-east-1-4.ec2.cloud.redislabs.com",
    port=19196,
    password="qa7cEQ7enuXT1LTk2wOpWfHpCYbLAtJE",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/products")
async def all():
    return  [format(pk)for pk in Product.all_pks()]
    
def format(pk : str):
    productt = Product.get(pk)

    return {
        'id' : productt.pk ,
        'name' : productt.name,
        'price' : productt.price,
        'quantity' : productt.quantity  
    }


@app.post("/products")
async def create(product: Product):
    return product.save()

@app.get("/products/{pk}")
async def get(pk : str):
    return Product.get(pk)

@app.get("products/{pk}")
async def delete(pk : str):
    return Product.delete(pk)
