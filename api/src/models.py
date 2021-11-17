from sqlalchemy.sql.schema import ForeignKey
from src.database import Base
from sqlalchemy import Column, Integer, String, Float


class Area(Base):
    __tablename__ = "AREA_TB"
    
    areaCode = Column("area_code", Integer, primary_key=True)
    areaName = Column("area_name", String(20))
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)
    areaCategory = Column("area_category", String(10))
    status = Column('status', Integer)

    
class Businesss(Base):
    __tablename__ = "BUSINESS_TB"
    
    businessCode = Column("business_code", Integer, primary_key=True)
    businessName = Column("business_name", String(20))
    businesssCategory = Column("business_category", String(10))
    
    
class Store(Base):
    __tablename__ = "STORE_TB"
    
    id = Column("id", Integer, primary_key=True, index=True)
    sotreName = Column("sotre_name", String(20))
    areaCode = Column("area_code_fk", Integer, ForeignKey('AREA_TB.area_code'))
    businessCode = Column("business_code_fk", Integer, ForeignKey('BUSINESS_TB.business_code'))
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)
    
    
class Change(Base):
    __tablename__ = "CHANGE_TB"
    
    id = Column("id", Integer, primary_key=True, index=True)
    areaCode = Column("area_code_fk", Integer, ForeignKey('AREA_TB.area_code'))
    businessCode = Column("business_code_fk", Integer, ForeignKey('BUSINESS_TB.business_code'))
    closure = Column("closure", Float)
    
    
class Sales(Base):
    __tablename__ = "SALES_TB"
    
    id = Column("id", Integer, primary_key=True, index=True)
    areaCode = Column("area_code_fk", Integer, ForeignKey('AREA_TB.area_code'))
    businessCode = Column("business_code_fk", Integer, ForeignKey('BUSINESS_TB.business_code'))
    amount = Column("amount", Integer)
    
    
class DaySales(Base):
    __tablename__ = "DAYSALES_TB"
    
    id = Column("id", Integer, primary_key=True, index=True)
    salesId = Column("sales_id_fk", Integer, ForeignKey('SALES_TB.id'))
    mondayRatio = Column("monday_ratio", Integer)
    tuesdayRatio = Column("tuesday_ratio", Integer)
    wednesdayRatio = Column("wednesday_ratio", Integer)
    thursdayRatio = Column("thursday_ratio", Integer)
    fridayRatio = Column("friday_ratio", Integer)
    saturdayRatio = Column("saturday_ratio", Integer)
    sundayRatio = Column("sunday_ratio", Integer)
    
    
class TimeSales(Base):
    __tablename__ = "TIMESALES_TB"
    
    id = Column("id", Integer, primary_key=True, index=True)
    salesId = Column("sales_id_fk", Integer, ForeignKey('SALES_TB.id'))
    time0006 = Column("time_0006", Integer)
    time0611 = Column("time_0611", Integer)
    time1114 = Column("time_1114", Integer)
    time1417 = Column("time_1417", Integer)
    time1721 = Column("time_1721", Integer)
    time2124 = Column("time_2124", Integer)
    

class CustomerSales(Base):
    __tablename__ = "CUSTOMMERSALES_TB"
    
    id = Column("id", Integer, primary_key=True, index=True)
    salesId = Column("sales_id_fk", Integer, ForeignKey('SALES_TB.id'))
    man = Column("man", Integer)
    woman = Column("woman", Integer)
    age10 = Column("age_10", Integer)
    age20 = Column("age_20", Integer)
    age30 = Column("age_30", Integer)
    age40 = Column("age_40", Integer)
    age50 = Column("age_50", Integer)
    age60 = Column("age_60", Integer)
