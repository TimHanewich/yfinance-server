import yfinance as yf

ticker = yf.Ticker("PG")
data = ticker.history(period="2d")
print(str(data))
prev_close:float = data["Close"].iloc[-2]
current_price:float = data["Close"].iloc[-1]

# Calculate
dollar_change:float = current_price - prev_close
percent_change:float = dollar_change / prev_close

# Construct
ToReturn:dict = {"price": round(current_price, 2), "change": round(dollar_change, 2), "changePecent": round(percent_change*100, 1)}

import json
print(json.dumps(ToReturn))