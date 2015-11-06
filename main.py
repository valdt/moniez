from yahoo_finance import Share
from classes import *

allStocks = {}
allStocks["Volvo-B"] = 'VOLV-B.ST'
stockClasses = {}
for name,code in allStocks.iteritems():
    if Share(code).get_price() != "None":
        stockClasses[name] = Stock(name,code)
print( stockClasses["Volvo-B"].trend() )
