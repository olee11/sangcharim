from typing import List
from pydantic import BaseModel

# 업종
class Business(BaseModel):
    businessCode: int
    businessName: str
    
class BusinessSchema(BaseModel):
    businessCategory: str
    businessList: List[Business]