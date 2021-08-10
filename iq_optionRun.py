from connect_user import whichUser
from iqoptionapi.stable_api import IQ_Option

class startProgram:
    def __init__(self, username, liveorDemo):
        conn = whichUser(username)
        self.username = conn.user_mail
        self.password = conn.password
        self.liveorDemo = liveorDemo
        self.startingBot()
        
    
    def checkBalance(self):
        if self.liveorDemo == 'demo':
            self.I_want_money.change_balance('PRACTICE')
        elif self.liveorDemo == 'live':
            self.I_want_money.change_balance('REAL')
        else:
            print('Oops i could not understand which sesion you choosed')
            exit()
        return (self.I_want_money.get_balance(), self.I_want_money.get_currency())
    
    
    def getAvailableLeverages(self, instrument_type, actives):
        return self.I_want_money.get_available_leverages(instrument_type, actives)[1]['leverages'][0]['regulated']
    
    def getActiveCodes(self):
        return self.I_want_money.get_all_ACTIVES_OPCODE()
    
    def getTradeStatus(self, order_id):
        return self.I_want_money.get_positions(order_id)
    
    def cancelTrade(self, order_id):
        return self.I_want_money.cancel_order(order_id)
    
    def getTradeHistory(self, instrument_type):
        #instrument_type="crypto","forex","fx-option","turbo-option","multi-option","cfd","digital-option"
        return self.I_want_money.get_position_history(instrument_type) 
    
    def initiateTrade(self, instrument_type="crypto", instrument_id="BTCUSD", side="buy", amount=1, leverage=3):        
        type="market"#input:"market"/"limit"/"stop"
        
        #for type="limit"/"stop"
        
        # only working by set type="limit"
        limit_price=None#input:None/value(float/int)
        
        # only working by set type="stop"
        stop_price=None#input:None/value(float/int)
        
        #"percent"=Profit Percentage
        #"price"=Asset Price
        #"diff"=Profit in Money
        
        stop_lose_kind="percent"#input:None/"price"/"diff"/"percent"
        stop_lose_value=95#input:None/value(float/int)
        
        take_profit_kind=None#input:None/"price"/"diff"/"percent"
        take_profit_value=None#input:None/value(float/int)
        
        #"use_trail_stop"="Trailing Stop"
        use_trail_stop=True#True/False
        
        #"auto_margin_call"="Use Balance to Keep Position Open"
        auto_margin_call=False#True/False
        #if you want "take_profit_kind"&
        #            "take_profit_value"&
        #            "stop_lose_kind"&
        #            "stop_lose_value" all being "Not Set","auto_margin_call" need to set:True
        
        use_token_for_commission=False#True/False
        
        check, order_id=self.I_want_money.buy_order(instrument_type=instrument_type, instrument_id=instrument_id,
                    side=side, amount=amount,leverage=leverage,
                    type=type,limit_price=limit_price, stop_price=stop_price,
                    stop_lose_value=stop_lose_value, stop_lose_kind=stop_lose_kind,
                    take_profit_value=take_profit_value, take_profit_kind=take_profit_kind,
                    use_trail_stop=use_trail_stop, auto_margin_call=auto_margin_call,
                    use_token_for_commission=use_token_for_commission) 
        return check, order_id
        
    
    def resetDemoBalance(self):
        self.I_want_money.reset_practice_balance()
        
    
    def startingBot(self):
        print('Connecting to your account')
        self.I_want_money=IQ_Option(self.username, self.password)
        self.I_want_money.connect()#connect to iqoption
        error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
        iqoption = IQ_Option("email", "password")
        check,reason=iqoption.connect()
        if check:
            print("Starting your robot")
            #if see this you can close network for test: 
            if iqoption.check_connect()==False:#detect the websocket is close
                print("try reconnect")
                check,reason=iqoption.connect()         
                if check:
                    print("Reconnect successfully")
                else:
                    if reason==error_password:
                        print("Error Password")
                    else:
                        print("No Network")
            else:
                print('Connection was successfull')
        else:
            
            if reason=="[Errno -2] Name or service not known":
                print("No Network")
            elif reason==error_password:
                print("Error Password")