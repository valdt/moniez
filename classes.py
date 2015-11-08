from yahoo_finance import Share
from datetime import datetime
import time, itertools, threading
class Stock:
    def __init__(self,name,code):
        self.threadList = []
        self.name = name
        self.code = code
        self.stock = Share(code)
        self.historyDic = {}
        self.history = []
        self.historyHandler()
        self.buy = False
        self.now = float(self.stock.get_price())
        self.avrage = 0
    def historyHandler(self):
        print("Collecting...")
        years = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
        for data in years:
            print("Data collector name: {}, id: {} started from 20{}-01-1 too the 20{}-12-31").format(self.name,years.index(data),data,data)
            year = '20'+data
            self.threadList.append(threading.Thread(target=self.historyBuilder, args=(year,)))
            self.threadList[-1].start()
        while True:
            for thread in self.threadList:
                thread.join()
            break


        for data in years:
            key = '20'+data
            self.history.extend(self.historyDic[key])
        print("Data collection complete.")

    def historyBuilder(self,year):
        start = year + '-01-1'
        stop = year + '-12-31'
        self.historyDic[year] = self.stock.get_historical(start, stop)

    def trend(self):
        closingValues = []
        trendValues = []
        temp = {} #Just an holding list, not in "real" use.
        peakDate = []
        deltaList = []
        avragePeakList = []
        self.avrage = float(self.history[0]['Close'])
        #Select all the closing values.
        for day in self.history:
            if day['Close'] != "None" and float(day['Close']) <= self.avrage*2:
                try:
                    closingValues.append((int(float(day['Close'])*float(10)))/float(10))
                    self.avrage = (self.avrage + float(day['Close']))/len(closingValues)
                except:
                    print("Error on the {} due to {}".format(day['Date'],day['Close']))
        #Sort the list and set avrage
        #for closeValue in closingValues:
        #    self.avrage += closeValue
        #self.avrage = self.avrage / (len(closingValues)-1)
        if self.now < self.avrage - 2:
            self.buy = True
        #Calculate the avrage peak and low
        closingValuesUnique = []
        for closeValue in closingValues:
            if closeValue not in closingValuesUnique:
                closingValuesUnique.append(closeValue)
        closingValuesUnique.sort()
        print(closingValuesUnique)
        token = int(len(closingValuesUnique))

        self.low = sum(closingValuesUnique[int(token*0.6):int(token*0.8)]) / int(token*0.8 - token*0.6)
        closingValuesUnique.reverse()
        self.peak = sum(closingValuesUnique[int(token*0):int(token*0.2)]) / int(token*0.2 - token*0)
        print(self.low)
        print(self.peak)
        #Going through all closing values to find dates where stock is in the peak.
        inPeak = False
        inLow = False
        for day in self.history:
            if float(day['Close']) >= self.peak and inPeak == False:
                temp[day['Date']] = ['peak',day['Close']]
                inLow = False
                inPeak = True
            elif float(day['Close']) <= self.low and inLow == False:
                temp[day['Date']] = ['low',day['Close']]
                inLow = True
                inPeak = False
        for date,data in temp.items():
            print("On the {} {} closed at {} resulting in entering a {}".format(date,self.name,data[1],data[0]))
        #date_format = "%Y-%m-%d"
        #print ("The stock reach its peak at following dates: {}".format(peakDate))
        #i = 0
        #for n in range(len(peakDate)-1):
        #    try:
        #        print("{} and {}".format(peakDate[0+i],peakDate[1+i]))
        #        a = datetime.strptime(peakDate[0+i], date_format)
        #        b = datetime.strptime(peakDate[1+i], date_format)
        #        avragePeakList.append((a-b).days)
        #        i += 2
        #    except:
        #        pass #Out of range on uneven lists.
        #totaltDays = 0
        #print(avragePeakList)
        #for days in avragePeakList:
        #    totaltDays += days
        #self.avragePeak = (totaltDays/(len(avragePeakList)-1))
        #print(self.avragePeak)
