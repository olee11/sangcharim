from src.database import SessionLocal
from src import models
import requests, xmltodict, json, math
from config import key
from src.models import *
from sqlalchemy import select

db = SessionLocal()

# 노원구 상권영역 db저장
# rValue값 구하기?
def create_area():
    area_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/TbgisTrdarRelm/1/5/"

    content = requests.get(area_url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['TbgisTrdarRelm'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    # 상권영역 데이터 총 개수
    total_cnt = int(jsonObj['list_total_count'])

    for i in range(1, math.ceil(total_cnt/1000)+1):
        end = i * 1000
        start = end - 1000 + 1
        if end > total_cnt:
            end = total_cnt

        # openapi
        area_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/TbgisTrdarRelm/{start}/{end}/"

        content = requests.get(area_url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['TbgisTrdarRelm'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for u in jsonObj['row']:
            # 노원구 시군구 코드: 11350
            if u['SIGNGU_CD'] == '11350':
                print(u)
                db_area = models.Area(areaCode=u['TRDAR_CD'], # 상권_코드
                                        areaName=u['TRDAR_CD_NM'], # 상권_코드_명
                                        latitude=u['XCNTS_VALUE'], # 엑스좌표_값
                                        longitude=u['YDNTS_VALUE']) # 와이좌표_값
                db.add(db_area)

        db.commit()

# 노원구 업종 db 저장
def create_business():
    business_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarStorQq/1/5/2020"

    content = requests.get(business_url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['VwsmTrdarStorQq'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    # 업종 데이터 총 개수
    total_cnt = int(jsonObj['list_total_count'])

    # 노원구 상권코드 리스트
    area_code_db = db.query(Area.areaCode)
    area_codes = []
    for area_code in area_code_db:
        area_codes.append(area_code[0])

    business = {}  # 업종 저장 딕셔너리
    for i in range(1, math.ceil(total_cnt/1000)+1):
        end = i * 1000
        start = end - 1000 + 1
        if end > total_cnt:
            end = total_cnt

        # openapi
        business_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarStorQq/{start}/{end}/2020"

        content = requests.get(business_url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['VwsmTrdarStorQq'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)
        

        for u in jsonObj['row']:
            if int(u['TRDAR_CD']) in area_codes:  # 노원구에 존재하는 업종만 저장
                if u['SVC_INDUTY_CD_NM'] not in business: # 딕셔너리에 업종명이 존재하지 않다면 저장
                    business[u['SVC_INDUTY_CD_NM']] = u['SVC_INDUTY_CD'][2:]
    
    for name, code in business.items():
        db_business = models.Businesss(businessCode=int(code), # 서비스_업종_코드
                                        businessName=name) # 서비스_업종_코드_명
        db.add(db_business)

    db.commit()


if __name__ == '__main__':
    # create_area()
    create_business()