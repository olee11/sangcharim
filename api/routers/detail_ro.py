from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from api.schemas.detail_sc import DetailSchema, CustomerSchema, SalesSchema, FutureSchema
from api.schemas import detail_sc, area_sc
from api import models
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

@router.get("/future", response_model=List[detail_sc.FutureSchema])
def getFuture(db: Session=Depends(get_db)):
    # areaList = db.query(models.Area).filter(models.Area.areaCode == areaCode)
    areaList = db.query(models.Area).all()
    changeList = db.query(models.Change).all()

    change_sum = 0
    change_cnt = 0
    for change in changeList:
        change_sum += change.closure
        change_cnt += 1
    area_closure = change_sum / change_cnt
    # print(area_closure)
    
    a = []
    for area in areaList:
        area_sc.Area = {
            "areaName": area.areaName,
            "areaCode": area.areaCode
        }
        a.append(detail_sc.FutureSchema(
                area = area_sc.Area,
                areaSituation = area.status,
                areaClosure = round(area_closure, 1),
                business = []
        ))
    return a 