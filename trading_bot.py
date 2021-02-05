import time
from iqoptionapi.stable_api import IQ_Option

class startProgram:
    def __init__(self, username, password, liveorDemo):
        self.username = username
        self.password = password
        self.liveorDemo = liveorDemo
        self.loginToAccount()
        
    
    def loginToAccount(self):
        print('Connecting to your account')
        I_want_money=IQ_Option(self.username, self.password)
        I_want_money.connect()#connect to iqoption
        error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
        iqoption = IQ_Option("email", "password")
        check,reason=iqoption.connect()
        if check:
            print("Start your robot")
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
                    time.sleep(1)
        else:
            
            if reason=="[Errno -2] Name or service not known":
                print("No Network")
            elif reason==error_password:
                print("Error Password")
                
                
if __name__ == '__main__':
    startProgram("julliesnyash@gmail.com","@PSD95isNOTt" ,'demo')