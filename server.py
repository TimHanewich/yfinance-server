# LATEST VERSION OF THIS FILE CAN BE FOUND HERE: https://raw.githubusercontent.com/TimHanewich/yfinance-server/refs/heads/master/server.py

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

        # Split into individual symbols (they may have provided both)
        symbols:list[str] = symbol.upper().split(",")
        print(str(symbols))

        # pull down data for all
        printnr("Pulling data using yfinance... ")
        data = yf.download(symbols, period="2d", group_by="ticker")
        print("done")

        # loop through each to extract data, construct body to return
        ToReturn:dict = {}
        for symb in symbols:
            ThisSymbData = data[symb.upper()]
            if ThisSymbData.isna().all().all(): # if it is all NaN data (not valid symbol probably)
                pass
            else:

                # Extract current price
                printnr("Extracting current price... ")
                current_price:float = ThisSymbData["Close"].iloc[-1]
                print("done")

                # Extract previous close
                printnr("Extracting previous close... ")
                if len(ThisSymbData) < 2: # if our request for 2 days of data only returned 1 day of data, that means it is an IPO (rare). So there isn't a "previous close" to compare to. So in that case, just do the changes against the opening price.
                    prev_close = ThisSymbData["Open"].iloc[-1]
                else: # there was data for a day before yesterday... not an IPO. most common obviously.
                    prev_close:float = ThisSymbData["Close"].iloc[-2]
                print("done")

                # Calculate
                dollar_change:float = current_price - prev_close
                percent_change:float = dollar_change / prev_close

                # Construct
                # Percent change is sent already pre-multiplied by 100
                ToReturn[symb.upper()] = {"price": round(current_price, 2), "change": round(dollar_change, 2), "changePercent": round(percent_change*100, 1)}

        
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