from typing import List
from pydantic import BaseModel

# 먼 지도
class AreaList(BaseModel):
    areaCode: int
    lat: float
    long: float
    businessCount: int

class MapFarSchema(BaseModel):
    focusLat: float
    focusLong: float
    areaList: List[AreaList]
    
# 가까운 지도
class MapCloseSchema(BaseModel):
    name: str
    lat: float
    long: float
    areaCode: int
    areaName: str
    businessCode: int
    businessName: str
