##### SETTINGS #####
port:int = 8080
####################

# import yfinance
print("Importing yfinance... ", end="")
import yfinance as yf
print("done")

# import flask
print("Importing Flask... ", end="")
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
        print("Pulling data using yfinance... ", end="")
        ticker = yf.Ticker(symbol.upper())
        data = ticker.history(period="2d")
        print("done")

        # Extract data
        print("Extracting data... ", end="")
        prev_close:float = data["Close"].iloc[-2]
        current_price:float = data["Close"].iloc[-1]
        print("done")

        # Calculate
        dollar_change:float = current_price - prev_close
        percent_change:float = dollar_change / prev_close

        # Construct
        # Percent change is sent already pre-multiplied by 100
        ToReturn:dict = {"price": round(current_price, 2), "change": round(dollar_change, 2), "changePecent": round(percent_change*100, 1)}

        # return
        print("Returning...")
        r = Response()
        r.status = 200
        r.headers["Content-Type"] = "application/json"
        r.set_data(json.dumps(ToReturn))
        return r

# SERVE
print("----- NOW SERVING -----")
print("Example calls: ")
print("GET http://localhost:" + str(port) + "/alive")
print("GET http://localhost:" + str(port) + "/quote/msft")
print("-----------------------")
server.run(host="0.0.0.0", port=port)