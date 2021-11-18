from typing import List
from pydantic import BaseModel

# 상권
class Area(BaseModel):
    areaCode: int
    areaName: str


class AreaSchema(BaseModel):
    areaCategory: str
    areaList: List[Area]
