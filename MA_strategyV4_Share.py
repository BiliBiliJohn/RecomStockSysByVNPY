from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)
from vnpy.trader.database import database_manager
import datetime
import time
import numpy as np
import pandas as pd

class MAStrategyV4_S(CtaTemplate):
    """"""

    author = "BiliBiliJohn"

    ma_window = 10
    fsign_up=1.0#%百分比
    fsign_down=1.0#%百分比
    am_size = 100
    new_trade_enable = 1
    fixed_size = 100
    full_size = 100

    closeprice=0
    ma=[]
    ma_value=0
    f=0.0
    f_list=np.zeros(20)
    duosign=False
    kongsign=False

    parameters = ["ma_window","fsign_up","fsign_down","am_size","new_trade_enable","fixed_size","full_size"]
    variables = ["closeprice","ma_value","f"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager(self.am_size)

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(60)
        

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.initok=True

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)


    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.cancel_all()

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            self.lasttradetime=bar.datetime
            return
        
        self.bardatetime=datetime.datetime.strftime(bar.datetime,'%Y-%m-%d %H:%M:%S')
        self.closeprice=bar.close_price
        self.ma=am.sma(n=self.ma_window, array=True)
        self.ma_value=self.ma[-1]
        self.f=(self.ma[-4]-6*self.ma[-3]+3*self.ma[-2]+2*self.ma[-1])*100/(6*self.ma_value)
        self.f_list=np.append(self.f_list[1:],[self.f])
        
        if self.cta_engine.engine_type.name=='BACKTESTING':
            pass
        elif self.initok:
            datatemp=pd.DataFrame(self.get_variables(),index=[self.bardatetime])
            self.write_log(datatemp.to_dict(orient='index'))
#         self.recorddata=self.recorddata.append(datatemp)
        
        pricenow=bar.close_price
        pricelast=self.am.close[-2]
        if self.cta_engine.engine_type.name=='BACKTESTING':
            pricebuy=pricenow
        else:
            AllOrders=self.cta_engine.main_engine.get_all_active_orders()
            pricetick=self.cta_engine.main_engine.get_tick(self.vt_symbol)
            if pricetick.ask_price_1==0 or pricetick.bid_price_1==0:
                pricebuy=pricenow
            else:
                pricebuy=pricetick.ask_price_1
            if len(AllOrders)>0:
                self.cancel_all()
                return
            else:
                pass
            
        self.duosign=self.f>=self.fsign_up
        self.kongsign=self.f<=-self.fsign_down       
         
        if self.pos == 0:
            if self.new_trade_enable==1:
                if self.duosign:
                    self.buy(pricebuy, self.fixed_size)
                elif self.kongsign:
                    pass
        elif self.pos > 0:
            if self.kongsign:
                self.sell(pricebuy, abs(self.pos))
            else:
                if self.full_size>abs(self.pos):
                    if bar.close_price>self.am.close[-2]:
                        self.buy(pricebuy, self.full_size-abs(self.pos))
        elif self.pos < 0:
            if self.duosign:
                self.cover(pricebuy, abs(self.pos))
            else:
                if self.full_size>abs(self.pos):
                    if bar.close_price<self.am.close[-2]:
                        self.short(pricebuy, self.full_size-abs(self.pos))
                        
        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
