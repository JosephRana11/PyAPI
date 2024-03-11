from fastapi import FastAPI , BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel , get_redis_connection
from starlette.requests import Request  
import requests
import time

app = FastAPI()


app.add_middleware(
    CORSMiddleware ,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

#Should be different database in Real world Application
redis = get_redis_connection(
    host="redis-19196.c10.us-east-1-4.ec2.cloud.redislabs.com",
    port=19196,
    password="qa7cEQ7enuXT1LTk2wOpWfHpCYbLAtJE",
    decode_responses=True
)

class Order(HashModel):
    product_id : str
    price : float
    fee : float
    total : float
    quantity : int 
    status : str

    class Meta:
        database = redis        

@app.get('/order/{pk}')
async def get_order(pk : str):
     return Order.get(pk)



@app.post('/orders')
async def create(request : Request , background_tasks : BackgroundTasks):
    body = await request.json()
    req = requests.get(f'http://localhost:8000/products/{body["id"]}')

    product = req.json()
    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity = body['quantity'],
        status = 'pending'  
    )
    order.save()
    
    background_tasks.add_task(order_completed , order)

    return order

def order_completed(order : Order):
        time.sleep(5)
        order.status = 'completed'
        order.save()