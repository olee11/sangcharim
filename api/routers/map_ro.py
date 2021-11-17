from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.map_sc import MapCloseSchema, MapFarSchema

from api import database

router = APIRouter(
    prefix="/map",
    tags=["Map"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("/far", response_model=MapFarSchema)
def getFarMap(db: Session=Depends(get_db)):
    return "Map!"

@router.get("/close", response_model=MapCloseSchema)
def getCloseMap(db: Session=Depends(get_db)):
    return "Close"