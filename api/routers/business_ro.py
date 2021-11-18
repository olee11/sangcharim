from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import models
from api.schemas import business_sc

from api import database

router = APIRouter(
    prefix="/business",
    tags=["Business"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("", response_model=List[business_sc.BusinessSchema])
def getBusiness(db: Session=Depends(get_db)):
    """
    `완료`\n
    `businessCategory`  : 업종 대분류\n
    `businessList`      : 소분류 업종 리스트\n
    `businessCode`      : 업종 코드\n
    `businessName`      : 업종 이름\n
    """
    businessList = db.query(models.Businesss).all()
    
    businessCategoryList: list[str] = list(set([business.businesssCategory for business in businessList]))
    result: list[business_sc.BusinessSchema] = [business_sc.BusinessSchema(businessCategory=businessCategory, businessList=[]) for businessCategory in businessCategoryList]
    
    for businesss in businessList:
        index = businessCategoryList.index(businesss.businesssCategory)
        result[index].businessList.append(business_sc.Business(
            businessCode=businesss.businessCode,
            businessName=businesss.businessName,
        ))
    
    return result