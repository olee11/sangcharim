from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import models, database
from api.routers import area_ro, business_ro, map_ro, detail_ro

app = FastAPI(
    title="SW SangChaRim API",
    description="FastAPI로 작성된 SangChaRim API입니다.",
    version="1.0.0",
    contact={
        "name": "SangChaRim",
        "email": "dev.ksanbal@gmail.com"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get('/')
def Index():
    return "Hello!"

# Router init
app.include_router(area_ro.router)
app.include_router(business_ro.router)
app.include_router(map_ro.router)
app.include_router(detail_ro.router)

# DB init
models.Base.metadata.create_all(database.engine)
