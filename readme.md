# yfinance-server
A lightweight Flask server (Python) for serving stock quote data via [yfinance](https://github.com/ranaroussi/yfinance).

To Run:
```
python yfinance-server.py
```

## Dependencies:
- [yfinance](https://pypi.org/project/yfinance/) (*1.3.0 used in my case*)
- [Flask](https://pypi.org/project/Flask/) (*3.1.0 used in my case*)

## Example Request and Response
Request:
```
GET http://localhost:8080/quote/MSFT
```

Response:
```
200 OK

{
  "price": 407.78,
  "change": -16.68,
  "changePercent": -3.9
}
```

Note: `changePercent` is already multiplied by 100.

If you make a request for an invalid ticker, like "BOGUS" for example, here is what will happen:
```
GET http://localhost:8080/quote/BOGUS
```

Response:
```
404 Not Found

Data pull from yfinance did not result in any data. Are you sure you provided a valid ticker?
```

## Requesting Multiple Quotes
You can also request multiple quotes at once, like so:

```
GET http://localhost:8080/quote/MSFT,PG,AAPL
```

And this will return:
```
200 OK

{
  "MSFT": {
    "price": 407.78,
    "change": -16.68,
    "changePercent": -3.9
  },
  "PG": {
    "price": 147.09,
    "change": 0.63,
    "changePercent": 0.4
  },
  "AAPL": {
    "price": 271.35,
    "change": 1.18,
    "changePercent": 0.4
  }
}
```

If there was a problem with one of the symbols you provided, it will look like this for example:

```
GET http://localhost:8080/quote/MSFT,PG,BOGUS
```

Response:
```
200 OK

{
  "MSFT": {
    "price": 407.78,
    "change": -16.68,
    "changePercent": -3.9
  },
  "PG": {
    "price": 147.09,
    "change": 0.63,
    "changePercent": 0.4
  },
  "BOGUS": "No data available."
}
```