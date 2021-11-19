from api.database import SessionLocal
from api import models
import requests, xmltodict, json, math
from api.models import *
from sqlalchemy import select
import os
import csv

db = SessionLocal()

# 환경변수 key값 가져오기
key = os.getenv('KEY')

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

    print("노원구 상권영역의 데이터를 찾고있습니다...")
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
    print("데이터 저장 완료!")

# area테이블 status 추가
def add_status():
    status_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarIxQq/1/5/2021"

    content = requests.get(status_url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['VwsmTrdarIxQq'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    # 상권변화지표 데이터 총 개수
    total_cnt = int(jsonObj['list_total_count'])

    # 노원구 상권코드 리스트
    area_code_db = db.query(Area.areaCode)
    area_codes = []
    for area_code in area_code_db:
        area_codes.append(area_code[0])

    print("노원구 상권변화지표의 데이터를 찾고있습니다...")
    area_status = {}
    for i in range(1, math.ceil(total_cnt/1000)+1):
        end = i * 1000
        start = end - 1000 + 1
        if end > total_cnt:
            end = total_cnt

        # openapi
        status_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarIxQq/{start}/{end}/2021"

        content = requests.get(status_url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['VwsmTrdarIxQq'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for u in jsonObj['row']:
            if int(u['TRDAR_CD']) in area_codes:
                if u['TRDAR_CHNGE_IX'] == 'HH':
                    status_code = 1  # 정체
                elif u['TRDAR_CHNGE_IX'] == 'HL':
                    status_code = 2  # 상권축소
                elif u['TRDAR_CHNGE_IX'] == 'LH':
                    status_code = 3  # 상권확장
                elif u['TRDAR_CHNGE_IX'] == 'LL':
                    status_code = 1  # 다이나믹                
                area = db.query(Area).filter(Area.areaCode == int(u['TRDAR_CD'])).first()
                area.status = status_code
                db.commit()
    print("데이터 저장 완료!")
        

# 노원구 업종 db 저장
def create_business():
    business_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarStorQq/1/5/2021"

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
    print("노원구 업종의 데이터를 찾고있습니다...")
    for i in range(1, math.ceil(total_cnt/1000)+1):
        end = i * 1000
        start = end - 1000 + 1
        if end > total_cnt:
            end = total_cnt

        # openapi
        business_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarStorQq/{start}/{end}/2021"

        content = requests.get(business_url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['VwsmTrdarStorQq'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)
        

        for u in jsonObj['row']:
            # 업종 저장
            if int(u['TRDAR_CD']) in area_codes:  # 노원구에 존재하는 업종만 저장
                if u['SVC_INDUTY_CD_NM'] not in business: # 딕셔너리에 업종명이 존재하지 않다면 저장
                    business[u['SVC_INDUTY_CD_NM']] = u['SVC_INDUTY_CD'][2:]
    
    for name, code in business.items():
        db_business = models.Businesss(businessCode=int(code), # 서비스_업종_코드
                                        businessName=name) # 서비스_업종_코드_명
        db.add(db_business)

    db.commit()
    print("데이터 저장 완료!")

# 노원구 상권변화 db 저장
def create_change():
    change_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarStorQq/1/5/2021"

    content = requests.get(change_url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['VwsmTrdarStorQq'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    # 상권변화 데이터 총 개수
    total_cnt = int(jsonObj['list_total_count'])

    # 노원구 상권코드 리스트
    area_code_db = db.query(Area.areaCode)
    area_codes = []
    for area_code in area_code_db:
        area_codes.append(area_code[0])

    print("노원구 상권변화 데이터를 찾고 있습니다...")
    for i in range(1, math.ceil(total_cnt/1000)+1):
        end = i * 1000
        start = end - 1000 + 1
        if end > total_cnt:
            end = total_cnt

        # openapi
        change_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarStorQq/{start}/{end}/2021"

        content = requests.get(change_url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['VwsmTrdarStorQq'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for u in jsonObj['row']:
            if int(u['TRDAR_CD']) in area_codes:
                db_change = models.Change(areaCode=u['TRDAR_CD'],  # 상권_코드
                                            businessCode=u['SVC_INDUTY_CD'][2:],  # 업종_코드
                                            closure=u['CLSBIZ_RT'])  # 업종 폐업률
                db.add(db_change)

    db.commit()
    print("데이터 저장 완료!")


# 노원구 매출영역 db저장
def create_sales():
    sales_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarSelngQq/1/5/2021"

    content = requests.get(sales_url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['VwsmTrdarSelngQq'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    # 매출 데이터 총 개수
    total_cnt = int(jsonObj['list_total_count'])

    # 노원구 상권코드 리스트
    area_code_db = db.query(Area.areaCode)
    area_codes = []
    for area_code in area_code_db:
        area_codes.append(area_code[0])

    cnt = 0  # 요일별 매출 데이터 id값
    print("노원구 매출영역의 데이터를 찾고 있습니다...")
    for i in range(1, math.ceil(total_cnt/1000)+1):
        end = i * 1000
        start = end - 1000 + 1
        if end > total_cnt:
            end = total_cnt

        # openapi
        sales_url = f"http://openapi.seoul.go.kr:8088/{key}/xml/VwsmTrdarSelngQq/{start}/{end}/2021"

        content = requests.get(sales_url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['VwsmTrdarSelngQq'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for u in jsonObj['row']:
            if int(u['TRDAR_CD']) in area_codes and int(u['STOR_CO']) != 0:
                # 분기당 평균 매출
                db_sales = models.Sales(areaCode=u['TRDAR_CD'], # 상권_코드
                                        businessCode=u['SVC_INDUTY_CD'][2:], # 업종_코드
                                        amount=int(int(u['THSMON_SELNG_AMT'])/int(u['STOR_CO']))) # 분기당_평균_매출
                db.add(db_sales)
                db.commit()
                cnt += 1

                # 요일별 매출 비율
                db_daysales = models.DaySales(salesId=cnt, # Sales테이블의 id값
                                                mondayRatio=int(u['MON_SELNG_RATE']),  # 월요일 매출 비율
                                                tuesdayRatio=int(u['TUES_SELNG_RATE']),  # 화요일 매출 비율
                                                wednesdayRatio=int(u['WED_SELNG_RATE']),  # 수요일 매출 비율
                                                thursdayRatio=int(u['THUR_SELNG_RATE']),  # 목요일 매출 비율
                                                fridayRatio=int(u['FRI_SELNG_RATE']),  # 금요일 매출 비율
                                                saturdayRatio=int(u['SAT_SELNG_RATE']),  # 토요일 매출 비율
                                                sundayRatio=int(u['SUN_SELNG_RATE']))  # 일요일 매출 비율
                db.add(db_daysales)
                
                # 시간대별 매출 비율
                db_timesales = models.TimeSales(salesId=cnt, # Sales테이블의 id값
                                                time0006=int(u['TMZON_00_06_SELNG_RATE']),  # 00~06 매출 비율
                                                time0611=int(u['TMZON_06_11_SELNG_RATE']),  # 06~11 매출 비율
                                                time1114=int(u['TMZON_11_14_SELNG_RATE']),  # 11~14 매출 비율
                                                time1417=int(u['TMZON_14_17_SELNG_RATE']),  # 14~17 매출 비율
                                                time1721=int(u['TMZON_17_21_SELNG_RATE']),  # 17~21 매출 비율  
                                                time2124=int(u['TMZON_21_24_SELNG_RATE']))  # 21~24 매출 비율
                db.add(db_timesales)

                # 고객 매출 비율
                db_custommersales = models.CustomerSales(salesId=cnt, # Sales테이블의 id값
                                                        man=int(u['ML_SELNG_RATE']),  # 남성 매출 비율
                                                        woman=int(u['FML_SELNG_RATE']),  # 여성 매출 비율
                                                        age10=int(u['AGRDE_10_SELNG_RATE']),  # 10대 매출 비율
                                                        age20=int(u['AGRDE_20_SELNG_RATE']),  # 20대 매출 비율
                                                        age30=int(u['AGRDE_30_SELNG_RATE']),  # 30대 매출 비율
                                                        age40=int(u['AGRDE_40_SELNG_RATE']),  # 40대 매출 비율
                                                        age50=int(u['AGRDE_50_SELNG_RATE']),  # 50대 매출 비율
                                                        age60=int(u['AGRDE_60_ABOVE_SELNG_RATE']))  # 60대 이상 매출 비율
                db.add(db_custommersales)

    # print(f"총 {cnt}개를 찾았습니다.")
    db.commit()
    print("데이터 저장 완료!")

def create_store():
    f = open('nowon_store2.csv', 'r', encoding='cp949')
    rdr = csv.reader(f)
    for line in rdr:
        if line[0] != '상호명':
            print(line[0])
            db_store = models.Store(sotreName=line[0],
                                    areaCode=int(line[3]),
                                    businessCode=int(line[1]),
                                    latitude=float(line[6]),
                                    longitude=float(line[5]))
            db.add(db_store)
    db.commit()
    f.close()
    


if __name__ == '__main__':
    # create_area()
    # add_status()
    # create_business()
    # create_change()
    # create_sales()
    create_store()