import iq_optionRun 

class run:
    def __init__(self):
        self.botUser = iq_optionRun.startProgram("Jullies2", 'demo')
        self.balance, self.tradingCurrency = self.botUser.checkBalance()
        self.use_balance = self.balance//3
        
        print(self.balance, self.use_balance)

if __name__ == "__main__":
    run()
    