from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.business_sc import BusinessSchema

from src import database

router = APIRouter(
    prefix="/business",
    tags=["Business"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("", response_model=BusinessSchema)
def getBusiness(db: Session=Depends(get_db)):
    return "Business"