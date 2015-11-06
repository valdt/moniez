from yahoo_finance import Share
from datetime import datetime
import time, itertools
class Stock:
    def __init__(self,name,code):
        self.name = name
        self.code = code
        self.stock = Share(code)
        self.now = self.stock.get_price()
        self.history = self.stock.get_historical('2013-01-1', '2015-01-1')
    def trend(self):
        closingValues = []
        trendValues = []
        temp = [] #Just an holding list, not in "real" use.
        peakDate = []
        deltaList = []
        avragePeakList = []
        for day in self.history:
            if day['Close'] != "None":
                closingValues.append(float(day['Close'] ))
        closingValues.sort()
        self.avrage = closingValues[len(closingValues)/2]
        closingValues.reverse()
        for day in self.history:
            print(closingValues[0:25])
            if (float(day['Close'])) in (closingValues[0:20]):
                temp.append(day['Date'])
            elif temp != [] and float(day['Close']) not in closingValues[21:50] :
                peakDate.append(temp[len(temp)/2])
                temp = []
        date_format = "%Y-%m-%d"
        print ("The stock reach its peak at following dates: {}".format(peakDate))
        i = 0
        for n in range(len(peakDate)-1):
            try:
                print("{} and {}".format(peakDate[0+i],peakDate[1+i]))
                a = datetime.strptime(peakDate[0+i], date_format)
                b = datetime.strptime(peakDate[1+i], date_format)
                avragePeakList.append((a-b).days)
                i += 2
            except:
                pass #Out of range on uneven lists.
        totaltDays = 0
        print(avragePeakList)
        for days in avragePeakList:
            totaltDays += days
        #self.avragePeak = (totaltDays/(len(avragePeakList)-1))
        #print(self.avragePeak)
