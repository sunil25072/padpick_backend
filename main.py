from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.area import router as area_router
from routers.home import homerouter
from routers.User_router import userrouter

app = FastAPI()

# ✅ CORS MUST BE HERE (BEFORE include_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Padpick Backend is running 🚀"}

# routers AFTER CORS
app.include_router(area_router)
app.include_router(homerouter)
app.include_router(userrouter)
