from vnpy.app.data_manager import ManagerEngine
from vnpy.trader.constant import Interval, Exchange
from datetime import datetime,timedelta
import numpy as np
from vnpy.trader.engine import MainEngine
from vnpy.app.cta_strategy.backtesting import BacktestingEngine
from vnpy.app.cta_strategy.strategies.MA_strategyV4_Share import (
    MAStrategyV4_S,
)

def Op_BackTest(stock,MinRecomFactor):
    nowdate=datetime.now()
    mainengine=MainEngine()
    DataEngine=ManagerEngine(mainengine,mainengine.event_engine)
    dataKLine=DataEngine.load_bar_data(symbol=stock[1],
                                   exchange=Exchange(stock[5]),
                                   interval=Interval.DAILY,
                                   start=nowdate-timedelta(days=400),
                                   end=nowdate+timedelta(days=1))
    price=[]
    for KLine in dataKLine:
        price.append(KLine.close_price)
    price_ary=np.array(price)
    meanprice=np.mean(price_ary)
    engine = BacktestingEngine()
    slip=max(meanprice*0.002,0.01)
    capital=meanprice*100*5
    engine.set_parameters(
        vt_symbol=stock[1]+'.'+stock[5],
        interval="d",
        start=nowdate-timedelta(days=800),
        end=nowdate+timedelta(days=1),
        rate=2/1000,
        slippage=slip,
        size=1,
        pricetick=0.01,
        capital=capital,
    )
    engine.add_strategy(MAStrategyV4_S, {})
    
    engine.load_data()
    engine.run_backtesting()
    df = engine.calculate_result()
    statistics=engine.calculate_statistics()
    return engine,statistics