from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.detail_sc import DetailSchema, CustomerSchema, SalesSchema, FutureSchema

from api import database

router = APIRouter(
    prefix="/detail",
    tags=["Detail"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("/", response_model=DetailSchema)
def getDetail(db: Session=Depends(get_db)):
    return "Detail!"

@router.get("/sales", response_model=SalesSchema)
def getSales(db: Session=Depends(get_db)):
    return "Detail!"

@router.get("/customer", response_model=CustomerSchema)
def getCustomer(db: Session=Depends(get_db)):
    return "Detail!"

@router.get("/future", response_model=FutureSchema)
def getFuture(db: Session=Depends(get_db)):
    return "Detail!"