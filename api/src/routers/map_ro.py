from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src import database

router = APIRouter(
    prefix="/map",
    tags=["Map"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("/")
def temp(db: Session=Depends(get_db)):
    return "Map!"