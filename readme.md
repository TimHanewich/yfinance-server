# yfinance-server
A lightweight Flask server (Python) for serving stock quote data via [yfinance](https://github.com/ranaroussi/yfinance).

To Run:
```
python server.py
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
{
  "price": 407.78,
  "change": -16.68,
  "changePercent": -3.9
}
```

Note: `changePercent` is already multiplied by 100.