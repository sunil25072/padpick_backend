from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine, Base
from routers.User_router import userrouter
from routers.Product_router import productrouter
from routers.home import homerouter
from routers.area import router

import models.home  # for SQLAlchemy models

app = FastAPI()

# ✅ CORS Middleware (frontend connect panna MUST)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Root API (testing purpose)
@app.get("/")
def greet():
    return {"message": "hello world"}

# ✅ Routers
app.include_router(userrouter)
app.include_router(productrouter)
app.include_router(homerouter)
app.include_router(router)


# from fastapi import FastAPI, Depends
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from db.session import SessionLocal, engine,Base
# from schemas.User import UserCreate,UserProfileUpdate
# from models.User import User
# from routers.User_router import userrouter
# from routers.Product_router import productrouter
# from routers.area import router
# import models.home
# from routers.home import homerouter
# from fastapi.middleware.cors import CORSMiddleware


# app = FastAPI()
# Base.metadata.create_all(bind=engine)
# @app.get("/")


# @app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # dev time
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# def greet():
#     return {"message":"hello world"}
# app.include_router(userrouter)
# app.include_router(productrouter)
# app.include_router(homerouter)
# app.include_router(router)
