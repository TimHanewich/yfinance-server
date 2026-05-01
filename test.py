import yfinance as yf

symbols = ["PG", "GARBAGE", "BOGUS"]

data = yf.download(symbols, period="2d", group_by="ticker")
print(data)

for symbol in symbols:
    data_symbol = data[symbol.upper()]
    if data_symbol.isna().all().all():
        print("Bogus: " + str(symbol))
    else:
        price:float = data_symbol["Close"].iloc[-1]
        print("Price of " + symbol + ": " + str(price))