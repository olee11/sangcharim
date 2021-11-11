from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.area_sc import AreaSchema

from src import database

router = APIRouter(
    prefix="/area",
    tags=["Area"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("", response_model=AreaSchema)
def getArea(db: Session=Depends(get_db)):
    return "Area!"
