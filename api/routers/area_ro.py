from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import models
from api.schemas import area_sc

from api import database

router = APIRouter(
    prefix="/area",
    tags=["Area"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("", response_model=List[area_sc.AreaSchema])
def getArea(db: Session=Depends(get_db)):
    """
    `완료`\n
    `areaCategory`  : 상권 대분류\n
    `areaList`      : 대분류내의 상권 리스트\n
    `areaCode`      : 세부 상권 코드\n
    `areaName`      : 세부 상권 이름\n
    """
    areaList = db.query(models.Area).all()
    
    areaCategoryList: list[str] = list(set([area.areaCategory for area in areaList]))
    result: list[area_sc.AreaSchema] = [area_sc.AreaSchema(areaCategory=areaCategory, areaList=[]) for areaCategory in areaCategoryList]
    
    for area in areaList:
        index = areaCategoryList.index(area.areaCategory)
        result[index].areaList.append(area_sc.Area(
            areaCode=area.areaCode,
            areaName=area.areaName,
        ))
    
    return result
