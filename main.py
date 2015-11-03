from yahoo_finance import Share
yahoo = Share('VOLV-B.ST')
data = yahoo.get_historical('2015-09-1', '2015-11-3')
for item in data:
    print("On the {} Volvo B closed at {} SEK".format(item["Date"],item["Close"]))
