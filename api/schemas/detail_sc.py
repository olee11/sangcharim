from typing import List, Optional
from pydantic import BaseModel
from api.models import Businesss

from api.schemas import area_sc, map_sc

# 상대업종률
class DetailBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessCount: int

class DetailSchema(BaseModel):
    area: area_sc.Area
    businessList: List[DetailBusiness]

# 매출
class Sales(BaseModel):
    min: int
    max: int
    avg: float

class Day(BaseModel):
    mon: Optional[int]=0
    tue: Optional[int]=0
    wed: Optional[int]=0
    thu: Optional[int]=0
    fri: Optional[int]=0
    sat: Optional[int]=0
    sun: Optional[int]=0
    
class Time(BaseModel):
    time0006: Optional[int]=0
    time0611: Optional[int]=0
    time1114: Optional[int]=0
    time1417: Optional[int]=0
    time1721: Optional[int]=0
    time2124: Optional[int]=0

class SalesBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessSale: int
    businessDay: Day
    businessTime: Time

class SalesSchema(BaseModel):
    area: area_sc.Area
    sales: Sales
    day: Day
    time: Time
    businessList: List[SalesBusiness]
    
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
    area: area_sc.Area
    genderRatio: CustomerGenderRatio
    ageRatio: CustomerAgeRatio
    # business: List[CustomerBusiness]

# 미래
class FutureBusiness(BaseModel):
    businessCode: int
    businessName: str
    businessClosure: float

class FutureSchema(BaseModel):
    area: area_sc.Area
    areaSituation: str
    areaClosure: float
    business: List[FutureBusiness]