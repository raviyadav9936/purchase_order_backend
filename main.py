from fastapi import FastAPI
from database.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
from database.models import Product
import modules.product.route as assignment
import modules.purchase.route as purchase

Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(assignment.router,tags=['Product'])
app.include_router(purchase.router,tags=['Purchase'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)