from fastapi import FastAPI

# import routers
from routers.area import router as router
from routers.home import homerouter
from routers.User_router import userrouter

app = FastAPI(title="Padpick Backend 🚀")

@app.get("/")
def root():
    return {"message": "Padpick Backend is running 🚀"}

# 🔥 REGISTER ROUTERS HERE
app.include_router(router)
app.include_router(homerouter)
app.include_router(userrouter)
