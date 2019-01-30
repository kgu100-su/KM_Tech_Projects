
import json
import os
import time
import datetime

class CoinSystem:
    def __init__(self): #Kyungmin Gu , Jeongun Lee
        self.coin_data = []
        self.coin_file = 'coin.save'
        self.downloadAPI()
        self.loadFromAPI()
        self.buy_data = []
        self.money = 0
        self.buy_file = 'buy.save'
        self.my_money_file = 'money.save'
        self.loadFromFile()

    def updateFile(self): #Kyungmin Gu , Jeongun Lee
        self.downloadAPI()
        self.coin_data = []
        self.loadFromAPI()

    def downloadAPI(self): #Jeongun Lee
        with requests.Session() as s:
            req = s.get("https://api.coinmarketcap.com/v1/ticker/")
            html = req.text
            with open(self.coin_file,'w+') as f:
                f.write(html)

    def loadFromFile(self):
        if os.path.isfile(self.buy_file):
            with open(self.buy_file,'r') as f:
                coins = json.load(f)
                for coin in coins:
                    self.buy_data.append(coin)
        if os.path.isfile(self.my_money_file):
            with open(self.my_money_file,'r') as f:
                self.money = float(f.readline())

    def loadFromAPI(self):
        with open(self.coin_file,'r') as f:
            data = json.load(f)
            for coin in data:
                self.coin_data.append(coin)

    def printCoinData(self): #Kyungmun Gu
        print("%-30s %-20s %20s %20s %30s" %('---NAME---','---PRICE---','---PERCENT_CHANGE_1H---','---PERCENT_CHANGE_24H---','-----UPDATED-----'))
        #print("--- NAME ---  --- PRICE ---  ---PERCENT_CHANGE 24H---")
        for coin in self.coin_data:
            ts_epoch = int(coin['last_updated'])
            ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
            print("%-30s $%-20s %20s %% %20s %% %30s" %(coin['name'],coin['price_usd'],coin['percent_change_1h'],coin['percent_change_24h'],ts))
            #print(coin['name'],'    ','$',coin['price_usd'],'        ',coin['percent_change_24h'],'%')
        print()

    def printMenu(self): #Kyungmin Gu , Jeongun Lee
        print('---MENU---')
        print('1. Print All Coins Prices')
        print('2. Buy')
        print('3. Print My Data')
        print('4. Sell')
        print('0. Exit')

    def runSystem(self): #Kyungmin Gu , Jeongun Lee
        user_select = 2
        while user_select is not 0:
            self.printMenu()
            user_select = int(input('select:'))
            if user_select is 1:
                self.printCoinData()
            elif user_select is 2:
                self.buyCoin()
            elif user_select is 3:
                self.printMyData()
            elif user_select is 4:
                self.Sell()
        self.saveToFile()

    def buyCoin(self): # Menu number 2
        self.updateFile()
        self.printCoinData()
        coin_name = input("Enter Coin Name : ") # coin name
        self.printMyData()
        buy_money = int(input("How much do you want to buy?")) #total Coin amount
        buy_count = 0.0 # buy coin count
        try:
            for coin in self.coin_data:
                if coin['name'] == coin_name:
                    buy_price = float(coin['price_usd']) # 1bit coin price when bought coin
                    buy_count = float(buy_money) / float(coin['price_usd'])
                    break
            buy_dict = {'name':coin_name,'buy_count':buy_count,'total_price':buy_count*buy_price,'buy_price':buy_price,'current_total_price':buy_count*buy_price,'current_usd_price':buy_price,'total_earn_percent':0,'earn_money':0.0}
            self.buy_data.append(buy_dict)
            self.money -= buy_money
        except:
            print("ERROR")

    def Sell(self): # Menu number 4
        self.printMyData()
        sell_coin_name = input("Enter Sell Coin Name: ")
        cnt = 0
        for i in range(len(self.buy_data)):
            if self.buy_data[i]['name']==sell_coin_name:
                cnt = i
                break
        self.money += self.buy_data[cnt]['current_total_price']
        del self.buy_data[cnt]


    def updataMyCoin(self):
        self.updateFile()
        for data in self.buy_data:
            for coin in self.coin_data:
                if data['name'] == coin['name']:
                    data['current_usd_price'] = float(coin['price_usd'])
                    data['current_total_price'] = data['buy_count'] * data['current_usd_price']
                    data['total_earn_percent'] = (data['current_total_price']-data['total_price'])/data['total_price']*100
                    data['earn_money'] = data['current_total_price']-data['total_price']

    def printMyData(self): #Kyungmin Gu Menu 3
        self.updataMyCoin()
        print("money : $",self.money)
        for data in self.buy_data:
            print("------------NAME-------------")
            print("|",data['name'],'\n')
            print("|","--------BUY COUNT--------")
            print("|",data['buy_count'],'\n')
            print("|","-----TOTAL BUY PRICE-----")
            print("|$",data['total_price'],'\n')
            print("|","---CURRENT TOTAL PRICE---")
            print("|$","%.2f\n" %(data['current_total_price']))
            print("|","------BUY USD PRICE------")
            print("|$","%.6f\n" %(data['buy_price']))
            print("|","----CURRENT USD PRICE----")
            print("|$","%.6f\n" %(data['current_usd_price']))
            print("|","-------EARN PERCENT-------")
            print("|","%.2f%%\n" %(data['total_earn_percent']))
            print("|","--------EARN MONEY--------")
            print("|$","%.6f\n" %(data['earn_money']))
            print("--------------------------\n")
            print()
            #print(data)

    def saveToFile(self): #Kyungmin Gu
        with open(self.buy_file,'w+') as f:
            json.dump(self.buy_data,f,indent=2)
        with open(self.my_money_file,'w+') as f:
            f.write(str(self.money))


coinSystem = CoinSystem()
coinSystem.printCoinData()
coinSystem.runSystem()
