from yahoo_finance import Share
from classes import *
import time, threading

allStocks = {}
allStocks["Volvo-B"] = 'VOLV-B.ST'
allStocks["Google"] = 'GOOG'
allStocks["Apple"] = 'AAPL'
allStocks["Facebook"] = 'FB'
allStocks["Audi"] = 'AUDVF'
#allStocks["Samsung Korea"] = '005930.KS'
stockClasses = {}
result = []
mainThreadList = []
def boot(name):
    stockClasses[name] = Stock(name,code)
for name,code in allStocks.iteritems():
        mainThreadList.append(threading.Thread(target=boot,args=(name,)))
        mainThreadList[-1].start()
        time.sleep(1.5)
while True:
    for thread in mainThreadList:
        thread.join()
    break
for name,code in allStocks.iteritems():
        mainThreadList = []
        mainThreadList.append(threading.Thread(target=stockClasses[name].trend(),args=()))
        mainThreadList[-1].start()
while True:
    for thread in mainThreadList:
        thread.join()
    break
print("\n")
for stock in stockClasses:
    print stockClasses[stock].result
    time.sleep(0.1)
    print("")
print("Fredrik Valdt GNU3.0")
