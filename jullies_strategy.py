import xlrd, math
import numpy as np
from dateutil import tz
import random

xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True

class apply_methodOne:
    def __init__(self, from_main):
        self.from_main = from_main
        
    def read_work_book(self, pair):
        print("Doing a custom strategy for %s"%(pair))
        pair = pair.replace('/','_').replace("=X", "")        
        self.from_main.write_log(pair, "Doing a custom strategy for %s"%(pair))
        if pair not in self.from_main.keysToList(self.from_main.tradingHistory):
            self.from_main.tradingHistory[pair] = {'movement': [], 'previous_time': '',
                                                   'call': {'trade':[], 'ids': [], 'pos': []},
                                                   'put': {'trade': [], 'ids': [], 'pos': []}}
        
        wb = xlrd.open_workbook('website/bot/assets/%s/excel/current.xlsx'%(pair))
        sheet = wb.sheet_by_index(0)
        nmb_rows = sheet.nrows
        #nmb_cols = sheet.ncols
        for row in range(1, nmb_rows):
            date_time = self.from_main.datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(row, 0), 0))
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            utc = date_time.replace(tzinfo=from_zone)
            local_date_time = utc.astimezone(to_zone)
            
            adj_closed = sheet.cell_value(row, 4)
            self.from_main.tradingHistory[pair]['movement'].append(adj_closed)
            if len(self.from_main.tradingHistory[pair]['movement']) > 120:
                b = (len(self.from_main.tradingHistory[pair]['movement'])//120)*120
                a = (len(self.from_main.tradingHistory[pair]['movement'])//120 -1)*120
                my_test_data = self.from_main.tradingHistory[pair]['movement'][a:b]
                all_test_data = self.from_main.tradingHistory[pair]['movement']
                if self.isTrendDown(all_test_data) and self.isTrendDown(my_test_data):
                    self.initiateTrading("put", pair, date_time, adj_closed)
                elif self.isTrendUp(all_test_data) and self.isTrendUp(my_test_data):
                    self.initiateTrading("call", pair, date_time, adj_closed)
                else:
                    self.initiateTrading("med", pair, date_time, adj_closed)
                
            self.from_main.tradingHistory[pair]['previous_time'] = date_time
    
    def initiateTrading(self, trade_type, tradePair, date_time, adj_closed, forceTrade = False):
        its_data = self.from_main.tradingHistory[tradePair]
        if trade_type == 'put':
            if len(its_data['put']['trade']) == 0:
                self.from_main.tradingHistory[tradePair]['put']['trade'].append([date_time, adj_closed])
                getIDentinty = random.randint(100, 1000)
                self.from_main.tradingHistory[tradePair]['put']['ids'].append(getIDentinty)
                print("Put ", tradePair, date_time, forceTrade)    
            else:
                lasttradingTime = its_data['put']['trade'][-1][0]
                tradng_time_diff = (date_time - lasttradingTime).total_seconds()/60   
                if forceTrade:
                    self.from_main.tradingHistory[tradePair]['put']['trade'].append([date_time, adj_closed])
                    getIDentinty = random.randint(100, 1000)
                    self.from_main.tradingHistory[tradePair]['put']['ids'].append(getIDentinty)                    
                    print("Put ", tradePair, date_time, forceTrade)                   
                elif tradng_time_diff > 60 and (adj_closed > its_data['put']['trade'][0][1]):
                    self.from_main.tradingHistory[tradePair]['put']['trade'].append([date_time, adj_closed])
                    getIDentinty = random.randint(100, 1000)
                    self.from_main.tradingHistory[tradePair]['put']['ids'].append(getIDentinty)                    
                    print("Put ", tradePair, date_time, forceTrade)  
        elif trade_type == 'call':
            if len(its_data['call']['trade']) == 0:
                self.from_main.tradingHistory[tradePair]['call']['trade'].append([date_time, adj_closed])
                getIDentinty = random.randint(100, 1000)
                self.from_main.tradingHistory[tradePair]['call']['ids'].append(getIDentinty)                
                print("Call", tradePair, date_time, forceTrade)                    
            else:
                lasttradingTime = its_data['call']['trade'][-1][0]
                tradng_time_diff = (date_time - lasttradingTime).total_seconds()/60  
                if forceTrade:
                    self.from_main.tradingHistory[tradePair]['call']['trade'].append([date_time, adj_closed])
                    getIDentinty = random.randint(100, 1000)
                    self.from_main.tradingHistory[tradePair]['call']['ids'].append(getIDentinty)                      
                    print("Call ", tradePair, date_time)                    
                elif tradng_time_diff > 60 and adj_closed < its_data['call']['trade'][0][1]:
                    self.from_main.tradingHistory[tradePair]['call']['trade'].append([date_time, adj_closed])
                    getIDentinty = random.randint(100, 1000)
                    self.from_main.tradingHistory[tradePair]['call']['ids'].append(getIDentinty)                      
                    print("Call 2. ", adj_closed, tradePair, date_time, its_data['call']['trade'])  
        
        ''' HERE WE'RE GOING TO STRATEGISE HOW TO CLOSE TRADES '''
        #runningPutTrades = self.from_main.tradingHistory[tradePair]['put']
        #start_put = 0
        #stop_put = len(runningPutTrades['trade'])
        #while start_put < stop_put:
            #thisPutTrade = runningPutTrades['trade'][start_put]
            #putTradeDateTime =thisPutTrade[0]
            #putTradeValue =thisPutTrade[1]
            #pipsMoved = math.trunc((putTradeValue - adj_closed)*10000)
            #minutesMoved = (date_time - putTradeDateTime).total_seconds()/60
            #historyMovement = self.from_main.tradingHistory[tradePair]['movement']
            #if minutesMoved > 5:
                #print("Tade id", runningPutTrades['ids'][start_put])
                #print("Is trend down", self.isTrendDown(historyMovement))
                #print(putTradeDateTime, putTradeValue)
                #print(date_time, adj_closed)            
                #print(pipsMoved, minutesMoved)
                #print()
                #pass
            #start_put+=1
            
        runningCallTrades = self.from_main.tradingHistory[tradePair]['call']  
        start_call = 0
        stop_call = len(runningCallTrades['trade'])
        while start_call < stop_call:
            thiscallTrade = runningCallTrades['trade'][start_call]
            callTradeDateTime, callTradeValue = thiscallTrade
            minutesMoved = (date_time - callTradeDateTime).total_seconds()/60
            historyMovement = self.from_main.tradingHistory[tradePair]['movement']
            if minutesMoved > 15:
                top = max(historyMovement)
                bottom = min(historyMovement)
                print((top-adj_closed)/(top - callTradeValue)*100, self.isTrendUp(historyMovement[-60:]))
                max(historyMovement) - callTradeValue
                print("Tade id", runningCallTrades['ids'][start_call])
                print(callTradeDateTime, callTradeValue, ' | ', date_time, adj_closed) 
                print("Moved: ", ((adj_closed-callTradeValue)*1000))
                print('____________________________________________________________')
                print()
                #del runningCallTrades['ids'][start_call]
                #del runningCallTrades['trade'][start_call]
            start_call+=1   
     
    
    def decisionTree(self, decision="call"):
        return True
    
    def isTrendUp(self, testData = []):
        res = np.all(np.diff(self.moving_average(np.array(testData), n=len(testData)-1))>0)
        resTwo = np.all(np.diff(self.moving_average(np.array(testData[60:]), n=len(testData[60:])-1))>0) 
        return res and resTwo
    
    def isTrendDown(self, testData = []):
        res =  np.all(np.diff(self.moving_average(np.array(testData), n=len(testData)-1))<0) 
        resTwo = np.all(np.diff(self.moving_average(np.array(testData[60:]), n=len(testData[60:])-1))<0) 
        return res and resTwo        
    
    def moving_average(self, a, n=3) :
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n    
        
            
                
            