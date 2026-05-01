##### SETTINGS #####
port:int = 8080
####################

# Opening Message
print("yfinance-server")
print("github.com/TimHanewich/yfinance-server")
print()

# helper function to print but not go to new line
# "printnr" = "print no return"
def printnr(msg:str): print(msg, end="", flush=True)

# import yfinance
printnr("Importing yfinance... ")
import yfinance as yf
print("done")

# import flask
printnr("Importing Flask... ")
from flask import Flask, request, Response
import json
print("done")

server = Flask("yfinance_server")

@server.route("/alive", methods=["GET"])
def alive():
    if request.method.upper() == "GET":
        r = Response()
        r.status = 200
        return r
    
@server.route("/quote/<symbol>", methods=["GET"])
def quote(symbol:str):
    if request.method.upper() == "GET":
        print("Request for quote data for '" + symbol.upper() + "'")

        # pull down data with yfinance
        printnr("Pulling data using yfinance... ")
        ticker = yf.Ticker(symbol.upper())
        data = ticker.history(period="2d")
            
        # Do we have legit data?
        # yfinance will return just an empty data array if it didnt work (i.e. bogus symbol)
        if data.empty:
            r = Response()
            r.status = 404
            r.headers["Content-Type"] = "text/plain"
            r.set_data("Data pull from yfinance did not result in any data. Are you sure you provided a valid ticker?")
            return r

        # Extract current price
        printnr("Extracting current price... ")
        current_price:float = data["Close"].iloc[-1]
        print("done")

        # Extract previous close
        printnr("Extracting previous close... ")
        if len(data) < 2: # if our request for 2 days of data only returned 1 day of data, that means it is an IPO (rare). So there isn't a "previous close" to compare to. So in that case, just do the changes against the opening price.
            prev_close = data["Open"].iloc[-1]
        else: # there was data for a day before yesterday... not an IPO. most common obviously.
            prev_close:float = data["Close"].iloc[-2]
        print("done")

        # Calculate
        dollar_change:float = current_price - prev_close
        percent_change:float = dollar_change / prev_close

        # Construct
        # Percent change is sent already pre-multiplied by 100
        ToReturn:dict = {"price": round(current_price, 2), "change": round(dollar_change, 2), "changePercent": round(percent_change*100, 1)}

        # return
        print("Returning...")
        r = Response()
        r.status = 200
        r.headers["Content-Type"] = "application/json"
        r.set_data(json.dumps(ToReturn))
        return r

# SERVE
print()
print("----- NOW SERVING -----")
print("Example calls: ")
print("GET http://localhost:" + str(port) + "/alive")
print("GET http://localhost:" + str(port) + "/quote/msft")
print("-----------------------")
print()
server.run(host="0.0.0.0", port=port)