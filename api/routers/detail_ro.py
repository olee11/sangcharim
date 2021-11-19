from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api import models
from api.schemas import detail_sc, area_sc

from api import database

router = APIRouter(
    prefix="/detail",
    tags=["Detail"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("/", response_model=detail_sc.DetailSchema)
def getDetail(areaCode: int, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    """
    `완료`\n
    `area`          : 선택한 상권 정보\n
    `areaCode`      : 상권 코드\n
    `areaName`      : 상권 이름\n
    `businessList`  : 가게 정보\n
    `businessCode`  : 업종 코드\n
    `businessName`  : 업종 이름\n
    `businessCount` : 상권내 해당 업종의 수\n
    -> businessCode1~3가 None이면 : 상권내의 가장 많은 업종 best3\n
    -> businessCode1~3에 값이 있으면 : 상권내의 선택한 업종 수
    """
    area = db.query(models.Area).filter(models.Area.areaCode == areaCode).first()
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 상권을 찾을 수 없습니다."
        )
    
    result = []
    storeList = db.query(models.Store).filter(models.Store.areaCode == areaCode)
    if not (businessCode1 or businessCode2 or businessCode3):
        # best3 뽑기
        storeDict: dict = {}
        for store in storeList.all():
            if store.businessCode in storeDict.keys():
                storeDict[store.businessCode] += 1
            else:
                storeDict[store.businessCode] = 1
        for bestKey in sorted(storeDict, key=storeDict.get, reverse=True)[:3]:
            result.append(
                detail_sc.DetailBusiness(
                    businessCode = bestKey,
                    businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == bestKey).first().businessName,
                    businessCount = storeDict[bestKey]
                )
            )
    else:
        # 선택한 애들의 수 뽑기
        for businessCode in (businessCode1, businessCode2, businessCode3):
            if businessCode:
                result.append(
                    detail_sc.DetailBusiness(
                        businessCode = businessCode,
                        businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == businessCode).first().businessName,
                        businessCount = storeList.filter(models.Store.businessCode == businessCode).count()
                    )
                )
    return detail_sc.DetailSchema(
        area = area_sc.Area(
            areaCode = area.areaCode,
            areaName = area.areaName,
        ),
        businessList = result
    )

@router.get("/sales", response_model=detail_sc.SalesSchema)
def getSales(db: Session=Depends(get_db)):
    return "Detail!"

@router.get("/customer", response_model=detail_sc.CustomerSchema)
def getCustomer(db: Session=Depends(get_db)):
    return "Detail!"

@router.get("/future", response_model=detail_sc.FutureSchema)
def getFuture(db: Session=Depends(get_db)):
    return "Detail!"