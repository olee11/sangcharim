from typing import List, Optional
from pydantic import BaseModel
from api.models import Businesss

from api.schemas import area_sc, map_sc

# 상대업종률
class DetailBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessRel: float

class DetailSchema(BaseModel):
    area: area_sc.AreaSchema
    bestBusinesss: List[map_sc.BusinessCount]
    Businesss: List[DetailBusiness]

# 매출
class Sales(BaseModel):
    min: int
    max: int
    avg: int

class Day(BaseModel):
    mon: int
    tue: int
    wed: int
    thu: int
    fri: int
    sat: int
    sun: int
    
class Time(BaseModel):
    time0006: int
    time0611: int
    time1114: int
    time1417: int
    time1721: int
    time2124: int

class SalesBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessSales: Sales
    businessDay: Day
    businessTime: Time

class SalesSchema(BaseModel):
    area: area_sc.AreaSchema
    sales: Sales
    day: Day
    time: Time
    business: List[SalesBusiness]
    
# 주 고객층
class CustomerGenderRatio(BaseModel):
    male: float
    female: float
    
class CustomerAgeRatio(BaseModel):
    age10: float
    age20: float
    age30: float
    age40: float
    age50: float
    age60: float

class CustomerBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessGender: CustomerGenderRatio
    businessAge: CustomerAgeRatio

class CustomerSchema(BaseModel):
    area: area_sc.AreaSchema
    genderRatio: CustomerGenderRatio
    ageRatio: CustomerAgeRatio
    business: List[CustomerBusiness]

# 미래
class FutureBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessClosure: float

class FutureSchema(BaseModel):
    area: area_sc.AreaSchema
    areaSituation: str
    areaClosure: float
    business: List[FutureBusiness]