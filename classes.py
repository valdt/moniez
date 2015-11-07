from yahoo_finance import Share
from datetime import datetime
import time, itertools
class Stock:
    def __init__(self,name,code):
        self.name = name
        self.code = code
        self.stock = Share(code)
        self.now = self.stock.get_price()
        self.history = self.stock.get_historical('2010-01-1', '2015-01-1')
        self.buy = False
        self.avrage = 0
    def trend(self):
        closingValues = []
        trendValues = []
        temp = {} #Just an holding list, not in "real" use.
        peakDate = []
        deltaList = []
        avragePeakList = []
        #Select all the closing values.
        for day in self.history:
            if day['Close'] != "None":
                closingValues.append(float(day['Close'] ))
        #Sort the list and set avrage

        for closeValue in closingValues:
            self.avrage += closeValue
        self.avrage = self.avrage / (len(closingValues)-1)
        if self.now < self.avrage - 2:
            self.buy = True
        #Calculate the avrage peak and low
        closingValuesUnique = []
        for closeValue in closingValues:
            if int(closeValue) not in closingValuesUnique:
                closingValuesUnique.append(int(closeValue))
        closingValuesUnique.sort()
        self.low = sum(closingValuesUnique[0:20]) / 20
        closingValuesUnique.reverse()
        self.peak = sum(closingValuesUnique[0:20]) / 20
        #Going through all closing values to find dates where stock is in the peak.
        inPeak = False
        inLow = False
        for day in self.history:
            if float(day['Close']) >= self.peak / 1.10 and inPeak == False:
                temp[day['Date']] = ['peak',day['Close']]
                inLow = False
                inPeak = True
            elif float(day['Close']) <= self.low * 1.10 and inLow == False:
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
