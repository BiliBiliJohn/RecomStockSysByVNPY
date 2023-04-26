import time
from GetStockKLineData import AllFuturesContract,SaveAllShareDaily
from Op_BackTest_MA import Op_BackTest
import pandas as pd
import emailtest
import multiprocessing

StopStrategy=False

def run_child(StopStrategy):
    MinRecomFactor=1.0
    Futurelist=AllFuturesContract()#获取股票列表
    stocklist=[]
    RecomTable=pd.DataFrame(columns=['股票代码','股票名称','交易所',"最新价格(元)",'趋势因子','近期趋势','400天总收益','年化收益率',"夏普比率"])
    RecomTable1=pd.DataFrame(columns=['股票代码','股票名称','交易所',"最新价格(元)",'趋势因子','近期趋势','400天总收益','年化收益率',"夏普比率"])
    #下载行情
    SaveAllShareDaily()
    for stock in Futurelist.values:
        try:
            onestockengine,statistics=Op_BackTest(stock,MinRecomFactor)#回测
            stocklist.append(onestockengine)
            if onestockengine.strategy.duosign:
                onestockdict={"股票代码":onestockengine.symbol,
                              "股票名称":stock[2],
                              "交易所":onestockengine.exchange.name,
                              "最新价格(元)":onestockengine.bar.close_price,
                              "400天总收益":round(statistics.get("total_return"),3),
                              "年化收益率":round(statistics.get("annual_return"),3),
                              "夏普比率":round(statistics.get("sharpe_ratio"),3)}
                RecomTable=RecomTable.append(onestockdict,ignore_index=True)
                pass
            pass
            if onestockengine.strategy.kongsign:
                onestockdict={"股票代码":onestockengine.symbol,
                              "股票名称":stock[2],
                              "交易所":onestockengine.exchange.name,
                              "最新价格(元)":onestockengine.bar.close_price,
                              "400天总收益":round(statistics.get("total_return"),3),
                              "年化收益率":round(statistics.get("annual_return"),3),
                              "夏普比率":round(statistics.get("sharpe_ratio"),3)}
                RecomTable1=RecomTable1.append(onestockdict,ignore_index=True)
                pass
            pass        
            onestockengine.clear_data()
        except Exception as e:
            print(e)
    emailtest.sendEmail(RecomTable.to_html(index=False),RecomTable1.to_html(index=False))
    StopStrategy.value=True

def run_parent():
    manual_test=True
    CTPchild_process = None
    print("启动CTA策略守护父进程")
    while 1:
        timehour=time.localtime().tm_hour
        timemin=time.localtime().tm_min
        timesec=time.localtime().tm_sec
        time.sleep(0.5)
        trading = False
        if (timehour==0 and timemin==5 and timesec==0 and time.localtime().tm_wday<5) or (manual_test):
            trading=True
            manual_test=False
        
        if trading and CTPchild_process is None:
            StopStrategy=multiprocessing.Value('b',False)
            print("启动CTP子进程")
            CTPchild_process = multiprocessing.Process(target=run_child,args=(StopStrategy,))
            CTPchild_process.start()
            print("CTP子进程启动成功")

        # 非记录时间则退出子进程
        if (not trading) and CTPchild_process is not None:
            if StopStrategy.value:
                print("关闭CTP子进程")
                CTPchild_process.terminate()
                CTPchild_process.join()
                CTPchild_process = None
                print("CTP子进程关闭成功")
                StopStrategy=False

if __name__ == "__main__":
    run_parent()