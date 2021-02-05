import time
from iqoptionapi.stable_api import IQ_Option

class startProgram:
    def __init__(self, username, password, liveorDemo):
        self.username = username
        self.password = password
        self.liveorDemo = liveorDemo
        self.startingBot()
    
    def runningBot(self):
        if self.liveorDemo == 'demo':
            self.I_want_money.change_balance('PRACTICE')
        elif self.liveorDemo == 'live':
            self.I_want_money.change_balance('REAL')
        else:
            print('Oops i could not understand which sesion you choosed')
            exit()
        print('\nYour account balance is: %s %s'%(self.I_want_money.get_balance(), self.I_want_money.get_currency()))
        
    
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
            #if see this you can close network for test
            while True: 
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
                    self.runningBot()
        else:
            
            if reason=="[Errno -2] Name or service not known":
                print("No Network")
            elif reason==error_password:
                print("Error Password")
                
                
if __name__ == '__main__':
    startProgram("julliesnyash@gmail.com","@PSD95isNOTt" ,'demo') #Use demo/live