import tushare as ts
from datetime import datetime
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import BarData
from vnpy.trader.database import database_manager
from time import sleep

key="********"

def AllFuturesContract():
    ts.set_token(key)
    pro=ts.pro_api()
    sharelist=pro.stock_basic(exchange='', list_status='L', fields='ts_code,exchange,symbol,name,area,industry,list_date')
    return sharelist

def FuturesMainContract(code,start):
    ts.set_token(key)
    pro=ts.pro_api()
    Contract=pro.fut_mapping(ts_code=code,start_date=start)
    return Contract

def SaveAllShareDaily():
    ts.set_token(key)
    pro=ts.pro_api()
    sharelist=pro.stock_basic(exchange='', list_status='L', fields='ts_code,exchange,symbol,name,area,industry,list_date')
    for share in sharelist.values:
        print(share)
        try:
            oldestbar=database_manager.get_oldest_bar_data(share[1], Exchange(share[5]), Interval.DAILY)
            newestbar=database_manager.get_newest_bar_data(share[1], Exchange(share[5]), Interval.DAILY)
            if oldestbar==None:
                newestbar=BarData
                newestbar.datetime=datetime(2020,1,1)
            if newestbar.datetime!=datetime.now():
                start=newestbar.datetime.strftime("%Y%m%d")
                end=datetime.now().strftime("%Y%m%d")
                DailyKLineDF=pro.daily(ts_code=share[0],start_date=start, end_date=end)
                DailyKLine=DailyKLineDF.values
                bars=[]
                if DailyKLine!=[]:
                        for j in DailyKLine:
                            datestr=datetime.strptime(j[1], "%Y%m%d")
                            bar = BarData(
                                symbol=share[1],
                                exchange=Exchange(share[5]),
                                datetime=datestr,
                                interval=Interval.DAILY,
                                volume=j[9],
                                open_price=j[2],
                                high_price=j[3],
                                low_price=j[4],
                                close_price=j[5],
                                open_interest=0,
                                gateway_name="DB",
                            )
                            bars.append(bar)
                        database_manager.save_bar_data(bars)
                sleep(0.2)
        except:
            print("Error! "+share)
    pass
        

# contract=AllFuturesContract()
# SaveKLine2(contract)
# FuturesMainContract('RB.SHF','20150101')