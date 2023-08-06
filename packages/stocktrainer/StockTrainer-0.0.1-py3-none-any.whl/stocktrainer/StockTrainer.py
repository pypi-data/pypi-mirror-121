import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta 
import random
import numpy as np

class Env:
     
    def __init__(self, Enviorment, ticker=None):
        self.switch_eviorment(Enviorment, ticker=ticker)

    #setup enviorment variables
    def switch_eviorment(self, Enviorment, ticker=None):
        print('Settting Up Enviorment ;)')
        eviorment_dictionary ={ "Standard": 0 , "Days":1, "Trading":2}
        while (Enviorment not in eviorment_dictionary):
            Enviorment= str(input("Enter the enviorment your want to choose\n"))
        self.typee = eviorment_dictionary.get(Enviorment)
        if(ticker == None ):
            self.ticker= str(input('Ticker of stock (All Caps)\n'))
        else:
            self.ticker = ticker
        not_done=True
        while (not_done):
            try:
                web.DataReader(self.ticker, 'yahoo', (datetime.now()-timedelta(days = 7)) , (datetime.now())) 
                not_done=False
            except:
                self.ticker= str(input('Enter Valid ticker of stock (All Caps)\n'))
               
    #get date frame with specifications   
    def setdf(self, start_date=None, end_date=None, agent_memory=None, days_ahead=None):
        if (self.typee!=4):
            if(self.typee==1):
                if not all([start_date, end_date, agent_memory, days_ahead]):
                    print('Some info missing, please enter it below \n')
            else:
                if not all([start_date, end_date, agent_memory]):
                    print('Some info missing, please enter it below \n')
                    
            if(start_date == None ):
                self.start_date = datetime.strptime(str(input("Start date: Year-Month-Day (ex. '2007-01-01') \n")), '%Y-%m-%d')
            else:
                self.start_date = start_date

            if(end_date == None ):
                end = str(input("End date: Year-Month-Day (ex. '2007-01-01') or 'now' for current date \n"))
                if end != 'now':
                    self.end_date = datetime.strptime(end, '%Y-%m-%d')
                else:
                    self.end_date = datetime.now()
            else:
                if(type(end_date) is str):
                    self.end_date = datetime.now()
                else:
                    self.end_date = end_date
                
            if(agent_memory == None ):
                self.agent_memory = int(input('Agent memory: days\n'))
            else:
                self.agent_memory = agent_memory
                
            if(self.typee == 0 or self.typee == 2):
                self.days_ahead = 1
            elif(self.typee == 1):
                if(days_ahead == None):
                    self.days_ahead = int(input('Days ahead to predict\n'))
                else: 
                    self.days_ahead = days_ahead
                    
            self.df = web.DataReader(self.ticker, 'yahoo', self.start_date, self.end_date)
            #Data comes as as: [High, Low, Open, Close, Volume, Adj Close] numpy array
            #Used to predict close of next day
        else:
            

    #returns data as needed
    def getdata(self, shuffle=True, seed= 42):
        datalist=[]
        anslist =[]
        if(self.typee == 0):    
            for i in range(len(self.df)-self.agent_memory):
                datalist.append(self.df.iloc[i:i+self.agent_memory].to_numpy())
                anslist.append(self.df.iloc[i+self.agent_memory, 3])
        elif(self.typee == 1):
            for i in range(len(self.df)-(self.agent_memory+self.days_ahead)+1):
                datalist.append(self.df.iloc[i:i+self.agent_memory].to_numpy())
                anslist.append(self.df.iloc[i+self.agent_memory:i+self.agent_memory+self.days_ahead , 3].to_numpy().reshape(self.days_ahead,1))
        if(shuffle):
            shufflelist = list(zip(datalist, anslist))
            random.seed(seed)
            random.shuffle(shufflelist)
            datalist, anslist = zip(*shufflelist)
        return datalist, anslist

    #data with train_test split
    def train_test(self, test_percent=None, shuffle = True, seed = 42, start_date=None, end_date=None, agent_memory=None, days_ahead=None):
        self.setdf(start_date, end_date, agent_memory, days_ahead)
        if (test_percent == None or  test_percent >=1):
            test_percent =.20
        datalist , anslist = self.getdata(shuffle = shuffle, seed=seed)
        
        test_data = np.asarray(datalist[int(len(datalist)*(1-test_percent)):])
        train_data = np.asarray(datalist[:int(len(datalist)*(1-test_percent))])
        test_ans = np.asarray(anslist[int(len(anslist)*(1-test_percent)):])
        train_ans = np.asarray(anslist[:int(len(anslist)*(1-test_percent))])
            
        return train_data, test_data, train_ans,test_ans 

    #data to test with if needed
    def get_testdata(self, start_date=None, end_date =None, agent_memory=None, days_ahead=None, shuffle = True, seed=42):
        self.setdf(start_date, end_date, agent_memory, days_ahead)
        datalist , anslist = self.getdata(shuffle = shuffle, seed=seed)

        return np.asarray(datalist), np.asarray(anslist)
        

    #to start rienforcemt learing agent
    #must call reset to begin for day trading bot
    def reset(self, start_date=None, end_date =None, agent_memory=None, days_ahead=None, cash=None):
        self.setdf(start_date, end_date, agent_memory, days_ahead)
        self.posbottom=0
        data = self.df.iloc[self.posbottom:self.posbottom+self.agent_memory].to_numpy()
        if (cash== None):
            self.cash = float(input("Enter starting cash\n"))
        else:
            self.cash = cash
        self.shares=0
        return data
        
    #step one day forward in time 
    def step(self, shares_bought=None):
        try:
            if(shares_bought==None):
                shares_bought=0
            self.posbottom +=1
            #One day predict
            if(self.typee == 0):
                ans = round(self.df[self.posbottom+self.agent_memory:self.posbottom+1+self.agent_memory].to_numpy()[0][3],2)
                data = self.df[self.posbottom:self.posbottom+self.agent_memory].to_numpy()
                return data,np.asarray(ans)

            #Day-Day predict
            elif(self.typee == 1):
                ans = self.df.iloc[self.posbottom+self.agent_memory:self.posbottom+self.agent_memoryself.days_ahead , 3].to_numpy()
                data = self.df[self.posbottom:self.posbottom+self.agent_memory].to_numpy()
                return data, ans
                
            #calculate money
            elif (self.typee == 2) :
                a = round(self.df[self.posbottom+self.agent_memory:self.posbottom+self.agent_memory+1].to_numpy()[0][3],2)
                e=0
                if (shares_bought*-1 > self.shares):
                    print("Can't sell more shares than you own")
                    e=1
                elif(shares_bought*a > self.cash):
                    print("You don't have enough money to buy %g shares" %(shares_bought))
                    e=1
                if (e==0):
                    cost = shares_bought*a *-1
                    self.shares+=shares_bought
                    c = self.cash
                    self.cash += cost
                    percent = round(((self.cash-c) / c)*100, 2)
                    print("Cash: %g Shares: %g Percent change: %g Close: %g" %(self.cash, self.shares,percent, a))
                data = self.df[self.posbottom+self.agent_memory:self.posbottom+self.agent_memory+1]
                d = data.to_numpy()
                return d, self.cash, self.shares
                #bot trading
        except:
            print("out of dates to step")
            return -1, -1, -1
            
    def getshares(self):
        return self.shares
