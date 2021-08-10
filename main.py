import yfinance as yf
import time, check_price_movement 
import jullies_strategy
import datetime
import os
from dateutil import tz
#import train_data
import iq_optionRun 

class run:
    def __init__(self):
        self.datetime = datetime
        #self.botUser = iq_optionRun.startProgram("Jullies", 'demo')
        #self.balance = self.botUser.checkBalance()
        
        #maxleverage = max(self.botUser.getAvailableLeverages('crypto', 'BTCUSD'))
        #make_order = self.botUser.initiateTrade(instrument_type="crypto", instrument_id="BTCUSD", side="sell", amount=1, leverage=maxleverage)
        self.balance = 10
        self.use_balance = self.balance/2
        while True:
            self.tradingHistory = {}
            start_time  = time.time()
            self.check_online()
            print("Time elasped: ----- %s Seconds-----" % round((time.time() - start_time)))
            time.sleep((time.time() - start_time))
            exit()
    
    def check_online(self):
        self.currencies = {'USD/CAD' : 'USDCAD=X', 
                           'USD/JPY' : 'USDJPY=X', 
                           'USD/CHF' : 'USDCHF=X', 
                           'EUR/GBP': 'EURGBP=X', 
                           'EUR/CHF': 'EURCHF=X',
                           'EUR/JPY': 'EURJPY=X',
                           'EUR/CAD': 'EURCAD=X' ,  
                           'EUR/SEK': 'EURSEK=X',
                           'EUR/USD': 'EURUSD=X',
                           'AUD/USD': 'AUDUSD=X', 
                           'NZD/USD': 'NZDUSD=X',
                           'GBP/USD': 'GBPUSD=X', 
                           'GBP/JPY': 'GBPJPY=X'
                           }
        self.priceFigure = check_price_movement.showInBrowser()
        for setpair in self.currencies:
            pair = self.currencies[setpair]
            ''' valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo  
            '''
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            
            #data = yf.download(tickers=pair, period='1d', interval='1m')  
            #data.index = data.index.tz_convert('Africa/Nairobi')
            #self.priceFigure.saveCurrentFigure(data, pair)
            
            start_time  = time.time()
            custom_strategy = jullies_strategy.apply_methodOne(self)
            custom_strategy.read_work_book(pair)
            print("Time elasped: ----- %s Seconds-----" % (time.time() - start_time))
            exit()
            print()
            
    def keysToList(self, dictData):
        newlist = list()
        for i in dictData.keys():
            newlist.append(i)
        return newlist
    
    def write_log(self, pair, message):
        pairPath = 'website/bot/assets/%s/log/actions.txt'%(pair)
        if os.path.exists(pairPath) == False:
            with open(pairPath, 'w') as file:
                file.write('')
        with open(pairPath, 'a') as file:
                file.write('\n%s ~ %s\n'%(message, datetime.datetime.now()))
            

if __name__ == '__main__':
    run()
    