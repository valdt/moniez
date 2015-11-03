from yahoo_finance import Share
yahoo = Share('VOLV-B.ST')
print (yahoo.get_open())
print (yahoo.get_price())
