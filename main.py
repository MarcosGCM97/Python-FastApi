from typing import Union
from fastapi import FastAPI
from routers import products, user, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router)
app.include_router(user.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get("/")
async def root():
    return "Hola mundo"


@app.get("/url")
async def root():
    return "https://marcos-congregado-front-end.netlify.app/"

