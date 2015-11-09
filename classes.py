from yahoo_finance import Share
from datetime import datetime
import time, itertools, threading
class Stock:
    def __init__(self,name,code,):
        self.result = ""
        self.threadList = []
        self.name = name
        self.code = code
        self.stock = Share(code)
        self.historyDic = {}
        self.history = []
        self.historyHandler()
        self.buy = False
        self.now = float(self.stock.get_price())
        self.average = 0
        self.high = 0
        self.low = 0
        self.trend()
    def historyHandler(self):
        yearSubfix = int(time.strftime("%Y-%m-%d")[2:4])
        years = []
        for i in range(5):
            years.append(str(yearSubfix-i))
        years.reverse()
        years = ["10","11","12","13","14","15"]
        for data in years:
            print("Data collector thread named: {}, id: {} started from 20{}-01-1 too the 20{}-12-31").format(self.name,years.index(data),data,data)
            year = '20'+data
            self.threadList.append(threading.Thread(target=self.historyBuilder, args=(year,)))
            self.threadList[-1].start()
            time.sleep(0.1)
        while True:
            for thread in self.threadList:
                thread.join()
            break
        for data in years:
            key = '20'+data
            self.history.extend(self.historyDic[key])

    def historyBuilder(self,year): #Notice: This function is made to be threaded
        start = year + '-01-1'
        stop = year + '-12-31'
        self.historyDic[year] = self.stock.get_historical(start, stop)

    def trend(self):
        closingValues = []
        trendValues = []
        peakDropDic = {} #Just an holding list, not in "real" use.
        peakDate = []
        deltaList = []
        averagePeakList = []
        self.average = float(self.history[0]['Close'])
        #Select all the closing values.
        for day in self.history:
            if day['Close'] != "None":
                try:
                    closingValues.append((int(float(day['Close'])*float(10)))/float(10))
                except:
                    print("Error on the {} due to {}".format(day['Date'],day['Close']))
        if self.now < self.average - 2:
            self.buy = True
        #Calculate the average peak and low
        closingValuesUnique = []
        for closeValue in closingValues:
            if closeValue not in closingValuesUnique:
                closingValuesUnique.append(closeValue)
        closingValuesUnique.sort()
        token = int(len(closingValuesUnique)) -1
        if token <= 11:
            self.drop = sum(closingValuesUnique[0:1])/2
            self.peak = sum(closingValuesUnique[token-2:token])/2
            self.low = closingValuesUnique[2]
            self.high = closingValuesUnique[-2]
        elif token <= 101:
            self.drop = sum(closingValuesUnique[0:10])/10
            self.peak = sum(closingValuesUnique[token-10:token])/10
            self.low = closingValuesUnique[10]
            self.high = closingValuesUnique[token-10]
        else:
            self.drop = int(sum(closingValuesUnique[int(token*0.15):int(token*0.35)])/ int(token*0.2))
            self.peak = int(sum(closingValuesUnique[int(token*0.7):int(token*0.9)])/ int(token*0.2))
            self.low = closingValuesUnique[int(token*0.1)]
            self.high = closingValuesUnique[int(token*0.9)]

        #print("{} High:{} Low:{} Peak:{} Drop:{}".format(self.name,self.high,self.low,self.peak,self.drop))
        #Going through all closing values to find dates where stock is in the peak.
        inPeak = False
        inLow = False
        self.lastPeakorDrop = "none"
        for day in self.history:
            if float(day['Close']) >= self.peak and inPeak == False:
                peakDropDic[day['Date']] = ['peak',day['Close']]
                inLow = False
                inPeak = True
                self.lastPeakorDrop = "drop"
            elif float(day['Close']) <= self.drop and inLow == False:
                peakDropDic[day['Date']] = ['low',day['Close']]
                inLow = True
                inPeak = False
                self.lastPeakorDrop = "peak"
        dateList = []
        for date,data in peakDropDic.items():
            dateList.append(date)
        dateList.sort()
        self.averageTime = 0
        date_format = "%Y-%m-%d"
        timeList = []
        i = 0
        #print(dateList)
        for n in range(len(dateList)/2):
            try:
                a = datetime.strptime(dateList[i], date_format)
                b = datetime.strptime(dateList[i+1], date_format)
            except:
                pass
            if a > b:
                timeList.append((a-b).days)
            elif b > a:
                timeList.append((b-a).days)
        self.lowData = True
        if len(timeList) >= 10:
            self.lowData = False
        i = 0
        for value in timeList:
            i += value
        self.averageTime = i/len(timeList)
        a = datetime.strptime(dateList[-1], date_format)
        #b = datetime.strptime(time.strftime("%Y-%m-%d"), date_format)
        b = datetime.strptime(self.historyDic['2015'][0]['Date'], date_format)
        self.timeInPeriod = (b-a).days

        #for date,data in peakDropDic.items():
        #    print("On the {} {} closed at {} resulting in entering a {}".format(date,self.name,data[1],data[0]))
        self.result = ("{} ocsilates at {} days with an average peak at {} and drop at {} we are currently {} from next {} and currently at {}".format(self.name,self.averageTime,self.peak,self.drop,self.timeInPeriod,self.lastPeakorDrop,self.now))
        #print (time.strftime("%Y-%m-%d"))
        #print ("The stock reach its peak at following dates: {}".format(peakDate))
        #i = 0
        #for n in range(len(peakDate)-1):
        #    try:
        #        print("{} and {}".format(peakDate[0+i],peakDate[1+i]))
        #        a =
        #        b = datetime.strptime(peakDate[1+i], date_format)
        #        averagePeakList.append((a-b).days)
        #        i += 2
        #    except:
        #        pass #Out of range on uneven lists.
        #totaltDays = 0
        #print(averagePeakList)
        #for days in averagePeakList:
        #    totaltDays += days
        #self.averagePeak = (totaltDays/(len(averagePeakList)-1))
        #print(self.averagePeak)
