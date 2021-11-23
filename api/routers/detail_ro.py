from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math

from api import database
from api import models
from api.schemas import detail_sc, area_sc


router = APIRouter(
    prefix="/detail",
    tags=["Detail"],
    responses={404: {"description": "Not found"}},
)

get_db = database.get_db

@router.get("/", response_model=detail_sc.DetailSchema)
def getDetail(areaCode: int, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    """
    `완료`\n
    `area`          : 선택한 상권 정보\n
    `areaCode`      : 상권 코드\n
    `areaName`      : 상권 이름\n
    `businessList`  : 가게 정보\n
    `businessCode`  : 업종 코드\n
    `businessName`  : 업종 이름\n
    `businessCount` : 상권내 해당 업종의 수\n
    -> businessCode1~3가 None이면 : 상권내의 가장 많은 업종 best3\n
    -> businessCode1~3에 값이 있으면 : 상권내의 선택한 업종 수
    """
    area = db.query(models.Area).filter(models.Area.areaCode == areaCode).first()
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 상권을 찾을 수 없습니다."
        )
    
    result = []
    storeList = db.query(models.Store).filter(models.Store.areaCode == areaCode)
    if not (businessCode1 or businessCode2 or businessCode3):
        # best3 뽑기
        storeDict: dict = {}
        for store in storeList.all():
            if store.businessCode in storeDict.keys():
                storeDict[store.businessCode] += 1
            else:
                storeDict[store.businessCode] = 1
        for bestKey in sorted(storeDict, key=storeDict.get, reverse=True)[:3]:
            result.append(
                detail_sc.DetailBusiness(
                    businessCode = bestKey,
                    businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == bestKey).first().businessName,
                    businessCount = storeDict[bestKey]
                )
            )
    else:
        # 선택한 애들의 수 뽑기
        for businessCode in (businessCode1, businessCode2, businessCode3):
            if businessCode:
                result.append(
                    detail_sc.DetailBusiness(
                        businessCode = businessCode,
                        businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == businessCode).first().businessName,
                        businessCount = storeList.filter(models.Store.businessCode == businessCode).count()
                    )
                )
    return detail_sc.DetailSchema(
        area = area_sc.Area(
            areaCode = area.areaCode,
            areaName = area.areaName,
        ),
        businessList = result
    )

@router.get("/sales", response_model=detail_sc.SalesSchema)
def getSales(areaCode: int, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    """
    `완료`\n
    `area`          : 선택한 상권 정보\n
    `sales`         : 상권의 매출 최소, 최대, 평균\n
    `day`           : 상권의 요일별 평균 매출비율\n
    `time`          : 상권의 시간대별 평균 매출비율\n
    `businessList`  : 선택한 업종의 정보\n
    `businessSale`  : 업종 매출액\n
    `businessDay`   : 업종의 요일별 매출비율\n
    `businessTime`  : 업종의 시간대별 매출비율\n
    -> businessCode1~3가 None이면 : []\n
    -> businessCode1~3에 값이 있으면 : 만약 해당 상권에 해당 업종이 없으면 추가 되지 않음.
    """
    # 상권
    area = db.query(models.Area).filter(models.Area.areaCode == areaCode).first()
    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 상권을 찾을 수 없습니다."
        )
    
    # 최소, 최대, 평균 매출
    sales = db.query(models.Sales).filter(models.Sales.areaCode == areaCode)
    amountList = [sale.amount for sale in sales.all()]
    resultSales = detail_sc.Sales(
        min = min(amountList),
        max = max(amountList),
        avg = sum(amountList) / len(amountList),
    )
    
    # 요일별 매출
    salesIdList = [sale.id for sale in sales.all()]
    salesIdListCount = len(salesIdList)
    
    daySales = db.query(models.DaySales).filter(models.DaySales.salesId.in_(salesIdList)).all()
    resultDaySales = detail_sc.Day()
    
    for sale in daySales:
        resultDaySales.mon += sale.mondayRatio
        resultDaySales.tue += sale.tuesdayRatio
        resultDaySales.wed += sale.wednesdayRatio
        resultDaySales.thu += sale.thursdayRatio
        resultDaySales.fri += sale.fridayRatio
        resultDaySales.sat += sale.saturdayRatio
        resultDaySales.sun += sale.sundayRatio
        
    resultDaySales.mon = round(resultDaySales.mon / salesIdListCount)
    resultDaySales.tue = round(resultDaySales.tue / salesIdListCount)
    resultDaySales.wed = round(resultDaySales.wed / salesIdListCount)
    resultDaySales.thu = round(resultDaySales.thu / salesIdListCount)
    resultDaySales.fri = round(resultDaySales.fri / salesIdListCount)
    resultDaySales.sat = round(resultDaySales.sat / salesIdListCount)
    resultDaySales.sun = round(resultDaySales.sun / salesIdListCount)

    # 시간대별 매출
    timeSales = db.query(models.TimeSales).filter(models.TimeSales.salesId.in_(salesIdList)).all()
    resultTimeSales = detail_sc.Time()
    
    for sale in timeSales:
        resultTimeSales.time0006 += sale.time0006
        resultTimeSales.time0611 += sale.time0611
        resultTimeSales.time1114 += sale.time1114
        resultTimeSales.time1417 += sale.time1417
        resultTimeSales.time1721 += sale.time1721
        resultTimeSales.time2124 += sale.time2124
        
    resultTimeSales.time0006 = round(resultTimeSales.time0006 / salesIdListCount)
    resultTimeSales.time0611 = round(resultTimeSales.time0611 / salesIdListCount)
    resultTimeSales.time1114 = round(resultTimeSales.time1114 / salesIdListCount)
    resultTimeSales.time1417 = round(resultTimeSales.time1417 / salesIdListCount)
    resultTimeSales.time1721 = round(resultTimeSales.time1721 / salesIdListCount)
    resultTimeSales.time2124 = round(resultTimeSales.time2124 / salesIdListCount)
    
    # 선택한 업종의 
    resultBusinessList: list[detail_sc.SalesBusiness] = []
    if businessCode1 or businessCode2 or businessCode3:
        for businessCode in (businessCode1, businessCode2, businessCode3):
            if businessCode:
                targetSales = sales.filter(models.Sales.businessCode == businessCode).first()
                if not targetSales:
                    continue
                targetDay = db.query(models.DaySales).filter(models.DaySales.id == targetSales.id).first()
                targetTime = db.query(models.TimeSales).filter(models.TimeSales.salesId == targetSales.id).first()
                
                resultBusinessList.append(
                    detail_sc.SalesBusiness(
                        businessCode = businessCode,
                        businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == businessCode).first().businessName,
                        businessSale = targetSales.amount,
                        businessDay = detail_sc.Day(
                            mon = targetDay.mondayRatio,
                            tue = targetDay.tuesdayRatio,
                            wed = targetDay.wednesdayRatio,
                            thu = targetDay.thursdayRatio,
                            fri = targetDay.fridayRatio,
                            sat = targetDay.saturdayRatio,
                            sun = targetDay.sundayRatio,
                        ),
                        businessTime = detail_sc.Time(
                            time0006 = targetTime.time0006,
                            time0611 = targetTime.time0611,
                            time1114 = targetTime.time1114,
                            time1417 = targetTime.time1417,
                            time1721 = targetTime.time1721,
                            time2124 = targetTime.time2124,
                        )
                    )
                )
    
    return detail_sc.SalesSchema(
        area = area_sc.Area(
            areaCode = area.areaCode,
            areaName = area.areaName,
        ),
        sales = resultSales,
        day = resultDaySales,
        time = resultTimeSales,
        businessList = resultBusinessList
    )

@router.get("/customer")
def getCustomer(areaCode: int, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    area = db.query(models.Area).filter(models.Area.areaCode == areaCode).first()

    resultCustomerList: list[detail_sc.CustomerBusiness] = []

    sales = db.query(models.Sales).filter(models.Sales.areaCode == areaCode)
    salesIdList = []
    for sale in sales:
        salesIdList.append(sale.id)

    customers = db.query(models.CustomerSales).filter(models.CustomerSales.salesId.in_(salesIdList))

    # 선택 업종이 없는 경우
    # 남여 비율 계산하기
    man_sum = woman_sum = 0
    for customer in customers:
        man_sum += customer.man
        woman_sum += customer.woman

    man_ratio = round(man_sum/len(salesIdList) * (100/((man_sum/len(salesIdList)) + woman_sum/len(salesIdList))))
    woman_ratio = round(woman_sum/len(salesIdList) * (100/((man_sum/len(salesIdList)) + woman_sum/len(salesIdList))))

    # 나이대별 비율 계산하기
    age_sum_list = []
    age10_sum = age20_sum = age30_sum = age40_sum = age50_sum = age60_sum = 0
    for customer in customers:
        age10_sum += customer.age10
        age20_sum += customer.age20
        age30_sum += customer.age30
        age40_sum += customer.age40
        age50_sum += customer.age50
        age60_sum += customer.age60 
    age_sum_list.extend([age10_sum, age20_sum, age30_sum, age40_sum, age50_sum, age60_sum])   
    age_ratio = [] 
    for age in age_sum_list:
        ratio = (age/len(salesIdList)) * (100/(sum(age_sum_list)/len(salesIdList)))
        age_ratio.append(round(ratio))
    age10_ratio = age_ratio[0]
    age20_ratio = age_ratio[1]
    age30_ratio = age_ratio[2]
    age40_ratio = age_ratio[3]
    age50_ratio = age_ratio[4]
    age60_ratio = age_ratio[5]

    # 선택 업종이 있는 경우
    if businessCode1 or businessCode2 or businessCode3: 
        for businessCode in (businessCode1, businessCode2, businessCode3):
            if not businessCode:
                continue
            try:
                targetSales = sales.filter(models.Sales.businessCode == businessCode).first()
                targetCustomer = db.query(models.CustomerSales).filter(models.CustomerSales.id == targetSales.id).first()

                # 업종 남녀비율 계산
                man_ratio1 = targetCustomer.man * (100/(targetCustomer.man + targetCustomer.woman))
                woman_ratio1 = targetCustomer.woman * (100/(targetCustomer.man + targetCustomer.woman))

                # 업종 나이대별 비율 계산
                age_sum = targetCustomer.age10 + targetCustomer.age20 + targetCustomer.age30 + targetCustomer.age40 + targetCustomer.age50 + targetCustomer.age60 
                age10_ratio1 = targetCustomer.age10 * (100/age_sum)
                age20_ratio1 = targetCustomer.age20 * (100/age_sum)
                age30_ratio1 = targetCustomer.age30 * (100/age_sum)
                age40_ratio1 = targetCustomer.age40 * (100/age_sum)
                age50_ratio1 = targetCustomer.age50 * (100/age_sum)
                age60_ratio1 = targetCustomer.age60 * (100/age_sum)  

                resultCustomerList.append(
                    detail_sc.CustomerBusiness(
                        businessCode = businessCode,
                        businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == businessCode).first().businessName,
                        businessGender = detail_sc.CustomerGenderRatio(
                            male = round(man_ratio1),
                            female = round(woman_ratio1)
                        ),
                        businessAge = detail_sc.CustomerAgeRatio(
                            age10 = round(age10_ratio1),
                            age20 = round(age20_ratio1),
                            age30 = round(age30_ratio1),
                            age40 = round(age40_ratio1),
                            age50 = round(age50_ratio1),
                            age60 = round(age60_ratio1) 
                        )
                    )
                )
            except:
                continue   

    return detail_sc.CustomerSchema(
        area = area_sc.Area(
            areaCode = area.areaCode,
            areaName = area.areaName,
        ),
        genderRatio = detail_sc.CustomerGenderRatio(
            male = man_ratio,
            female = woman_ratio
        ),
        ageRatio = detail_sc.CustomerAgeRatio(
            age10 = age10_ratio,
            age20 = age20_ratio,
            age30 = age30_ratio,
            age40 = age40_ratio,
            age50 = age50_ratio,
            age60 = age60_ratio            
        ),
        business = resultCustomerList
    )

@router.get("/future", response_model=detail_sc.FutureSchema)
def getFuture(areaCode: int, businessCode1: Optional[int]=None, businessCode2: Optional[int]=None, businessCode3: Optional[int]=None, db: Session=Depends(get_db)):
    situationStr = { 1: "정체", 2: "상권축소", 3: "상권확장", 4: "다이나믹" }
    area = db.query(models.Area).filter(models.Area.areaCode == areaCode).first()

    resultFutureList: list[detail_sc.FutureBusiness] = []

    # 선택 업종이 없는 경우  
    # 상권내 전체 점포 폐업률의 합/전체 점포의 수 
    change_sum = change_cnt = 0
    changeList = db.query(models.Change).filter(models.Change.areaCode == areaCode)
    for change in changeList:
        change_sum += change.closure
        change_cnt += 1
    area_closure = int(change_sum / change_cnt)

    # 선택 업종이 있는 경우
    if businessCode1 or businessCode2 or businessCode3: 
        for businessCode in (businessCode1, businessCode2, businessCode3):
            if not businessCode:
                continue            
            targetClosure = db.query(models.Change).filter(models.Change.areaCode == areaCode) \
                                                    .filter(models.Change.businessCode == businessCode).first()

            try:
                resultFutureList.append(
                    detail_sc.FutureBusiness(
                        businessCode = businessCode,
                        businessName = db.query(models.Businesss).filter(models.Businesss.businessCode == businessCode).first().businessName,
                        businessClosure = targetClosure.closure
                    )
                )
            except:
                continue

    return detail_sc.FutureSchema(
        area = area_sc.Area(
            areaCode = area.areaCode,
            areaName = area.areaName,
        ),
        areaSituation = situationStr[area.status],
        areaClosure = area_closure,
        business = resultFutureList
    )