from json import decoder
# import module
import requests
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import sys
cg = CoinGeckoAPI()

#user enters the start and end dates. program gives error and ends itself if the date format is incorrect.
start_date = input("Enter the start date(dd-mm-yyyy): ")
start_date2 = start_date
try:
    start_date2 = datetime.strptime(start_date,'%d-%m-%Y')
except ValueError:
    print ("Incorrect format in start date, should be dd-mm-yyyy")
    sys.exit()
end_date = input("Enter the end date(dd-mm-yyyy): ")
end_date2 = end_date
try:
    end_date2 = datetime.strptime(end_date,'%d-%m-%Y')
except ValueError:
    print ("Incorrect format in start date, should be dd-mm-yyyy")
    sys.exit()

Days = (end_date2 - start_date2).days + 1

#checks if the decrease value is bigger than the longest decrease value. If it is, then the decrease 
#value is the new longest decrease value.
def CheckLongestDecrease(Decrease, LongestDecrease):
    if Decrease > LongestDecrease:
        LongestDecrease = Decrease
    return LongestDecrease

def TradingVolume():
    volumeData = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from=1577836800&to=1609376400').text
    print(volumeData)

def Main(DateCounter, end_date2, DateID, Days):
    td = timedelta(1)
    Decrease = 0
    previous = 0
    TimeToSell = 0
    TimeToBuy = 0
    HighestValue = 0
    LowestValue = 0
    LongestDecrease = 0
    i = 0
    Change = "-"
    while DateCounter <= end_date2:
        #Makes the DateID into a string
        DateID = DateCounter.strftime("%d-%m-%Y")
        #gets the data from Coingecko
        CoinHistory = cg.get_coin_history_by_id(id='bitcoin', vs_currencies='EUR', date = DateID, localization='false')
        CoinHistoryString = str(CoinHistory)
        #finds the value of euro in the data
        PositionOFEur1 = CoinHistoryString.find("eur")
        #takes the value of euro from the data and makes it it's own variable
        BtcToEuro = CoinHistoryString[PositionOFEur1+6:PositionOFEur1+13]
        #gives the first date's value to previous and LowestValue
        while i < 1:
            LowestValue = int(float(BtcToEuro))
            previous = int(float(BtcToEuro))
            i += 1

        #Increases the decrease value if the Btc value is smaller then the previous value
        if int(float(BtcToEuro)) < previous:
            Decrease += 1
            Change = "↓"
        #If the decrease value is bigger than the previous longest decrease it sets decrease value to be the longestdecrease
        elif int(float(BtcToEuro)) > previous:
            LongestDecrease = CheckLongestDecrease(Decrease, LongestDecrease)
            Decrease = 0
            Change = "↑"
        else:
            LongestDecrease = CheckLongestDecrease(Decrease, LongestDecrease)
            Decrease = 0
            Change = "-"

        #check if the date's btc value is higher or lower than the lowest and highest values
        #if the value is higher or lower, update TimeToSell or TimeToBuy
        if int(float(BtcToEuro)) > HighestValue:
            HighestValue = int(float(BtcToEuro))
            TimeToSell = DateID
        elif int(float(BtcToEuro)) < LowestValue:
            LowestValue = int(float(BtcToEuro))
            TimeToBuy = DateID    
        previous = int(float(BtcToEuro))
    
        print("Date : ", DateID, " ",  BtcToEuro, "Change: ", Change )

        DateCounter = DateCounter + td
    LongestDecrease = CheckLongestDecrease(Decrease, LongestDecrease)
    #if the longest decrease equals the number of chosen days the program tells user to not sell or buy. Otherwise the program
    #prints the longest downward trend and the best day to sell and buy.
    if LongestDecrease == Days:
        print("Do not buy or sell")
    else:
        print("Time to buy: ", TimeToBuy, " | Time to sell ", TimeToSell)
    print("Longest downward trend: ", LongestDecrease)
    
        
Main(start_date2, end_date2, start_date, Days)
#TradingVolume()