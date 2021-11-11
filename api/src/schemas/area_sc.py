from pydantic import BaseModel

# 상권
class AreaSchema(BaseModel):
    areaCode: int
    areaName: str
    
    class Config():
        orm_mode = True