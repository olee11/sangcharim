from sqlalchemy.sql.schema import ForeignKey
from src.database import Base
from sqlalchemy import Column, Integer, String, Float

class Area(Base):
    __tablename__ = "area"
    
    area_code = Column(Integer, primary_key=True)
    area_name = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    r_value = Column(Integer)
    
class Businesss(Base):
    __tablename__ = "business"
    
    business_code = Column(Integer, primary_key=True)
    business_name = Column(String(20))
    
class Store(Base):
    __tablename__ = "store"
    
    id = Column(Integer, primary_key=True, index=True)
    sotre_name = Column(String(20))
    area_code = Column(Integer, ForeignKey('area.area_code'))
    business_code = Column(Integer, ForeignKey('business.business_code'))
    latitude = Column(Float)
    longitude = Column(Float)
    
class Change(Base):
    __tablename__ = "change"
    
    id = Column(Integer, primary_key=True, index=True)
    area_code = Column(Integer, ForeignKey('area.area_code'))
    business_code = Column(Integer, ForeignKey('business.business_code'))
    status = Column(String(10))
    closure = Column(Float)
    
class Sales(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    area_code = Column(Integer, ForeignKey('area.area_code'))
    business_code = Column(Integer, ForeignKey('business.business_code'))
    amount = Column(Integer)
    
class DaySales(Base):
    __tablename__ = "daySales"
    
    id = Column(Integer, primary_key=True, index=True)
    sales_id = Column(Integer, ForeignKey('sales.id'))
    monday_ratio = Column(Integer)
    tuesday_ratio = Column(Integer)
    wednesday_ratio = Column(Integer)
    thursday_ratio = Column(Integer)
    friday_ratio = Column(Integer)
    saturday_ratio = Column(Integer)
    sunday_ratio = Column(Integer)
    
class TimeSales(Base):
    __tablename__ = "timeSales"
    
    id = Column(Integer, primary_key=True, index=True)
    sales_id = Column(Integer, ForeignKey('sales.id'))
    time_0006 = Column(Integer)
    time_0611 = Column(Integer)
    time_1114 = Column(Integer)
    time_1417 = Column(Integer)
    time_1721 = Column(Integer)
    time_2124 = Column(Integer)
    
class CustomerSales(Base):
    __tablename__ = "custommerSales"
    
    id = Column(Integer, primary_key=True, index=True)
    sales_id = Column(Integer, ForeignKey('sales.id'))
    man = Column(Integer)
    woman = Column(Integer)
    age_10 = Column(Integer)
    age_20 = Column(Integer)
    age_30 = Column(Integer)
    age_40 = Column(Integer)
    age_50 = Column(Integer)
    age_60 = Column(Integer)
