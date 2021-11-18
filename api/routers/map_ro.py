from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas import map_sc
from api import models

from api import database

router = APIRouter(
    prefix="/map",
    tags=["Map"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("/far", response_model=map_sc.MapFarSchema)
def getFarMap(areaCode: Optional[int]=None, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    """
    `완료`\n
    `focusLat`      : 중심좌표 위도\n
    `focusLong`     : 중심좌표 경도\n
    `areaList`      : 상권별 정보 리스트\n
    `areaCode`      : 상권 코드\n
    `lat`           : 상권 위도\n
    `long`          : 상권 경도\n
    `businessCount` : 상권내 가게 수\n
    -> businessCode1~3가 None이면 : 상권내의 모든 가게 수\n
    -> businessCode1~3에 값이 있으면 : 상권내의 선택한 업종의 가게 수
    """
    # areaCode가 없으면 좌표 = 태릉입구
    # areaCode가 있으면 좌표 = area 좌표
    focusLat: float = 37.617636
    focusLong: float = 127.075621
    if areaCode:
        area = db.query(models.Area).filter(models.Area.areaCode == areaCode).first()
        if area:
            focusLat = area.latitude
            focusLong = area.longitude
    
    # businessCode 1,2,3이 없으면 모든 점포 수
    # businessCode 1,2,3이 있으면 있는 점포 수
    areaList = db.query(models.Area).all()
    result: list[map_sc.AreaList] = []
    
    for area in areaList:
        businessInArea = db.query(models.Store).filter(models.Store.areaCode == area.areaCode)
        count = 0
        
        if not (businessCode1 or businessCode2 or businessCode3):
            count = businessInArea.count()
        else:
            count += 0 if not businessCode1 else businessInArea.filter(models.Store.businessCode == businessCode1).count()
            count += 0 if not businessCode2 else businessInArea.filter(models.Store.businessCode == businessCode2).count()
            count += 0 if not businessCode3 else businessInArea.filter(models.Store.businessCode == businessCode2).count()
        
        result.append(
            map_sc.AreaList(
                areaCode=area.areaCode,
                lat=area.latitude,
                long=area.longitude,
                businessCount=count,
            )
        )
            
    return map_sc.MapFarSchema(
        focusLat = focusLat,
        focusLong = focusLong,
        areaList = result,
    )

@router.get("/close", response_model=List[map_sc.MapCloseSchema])
def getCloseMap(areaCode: Optional[int]=None, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    """
    `완료`\n
    **areaCode**가 있으면 그 상권의 가게만 나옴\n
    **businessCode1~3**이 있으면 해당 업종의 가게만 나옴\n
    `name`          : 가게 이름\n
    `lat`           : 가게 위도\n
    `long`          : 가게 경도\n
    `areaCode`      : 가게의 상권 코드\n
    `areaName`      : 가게의 상권명\n
    `businessCode`  : 가게의 업종 코드\n
    `busniessName`  : 가게의 업종명\n
    """
    storeList = db.query(models.Store)
    
    if areaCode:
        storeList = storeList.filter(models.Store.areaCode == areaCode)
    
    resultStoreList: list[models.Store] = []
    
    if (businessCode1 or businessCode2 or businessCode3):
        for businessCode in (businessCode1, businessCode2, businessCode3):
            if businessCode:
                resultStoreList += storeList.filter(models.Store.businessCode == businessCode).all()
    else:
        resultStoreList = storeList.all()
    
    return [
        map_sc.MapCloseSchema(
            name = store.storeName,
            lat = store.latitude,
            long = store.longitude,
            areaCode = store.areaCode,
            areaName = db.query(models.Area).filter(models.Area.areaCode == store.areaCode).first().areaName,
            businessCode = store.businessCode,
            businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == store.businessCode).first().businessName,
        ) for store in resultStoreList
    ]
