from pydantic import BaseModel

# 업종
class BusinessSchema(BaseModel):
    businessCode: int
    businessName: str
    
    class Config():
        orm_mode = True