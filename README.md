## challenge.py

### Connects to a virtual market and performs some predefined tasks

- Get credentials logging with a Google account at https://remarkets.primary.ventures/
- List of instruments (tickers) at https://api.remarkets.primary.com.ar/rest/instruments/all

Usage:  
`~$ challenge.py [-h] -u REMARKETS_USER -p REMARKETS_PASSWORD -a REMARKETS_ACCOUNT`

Detail: Connects to a market and gets the last price for a given instrument (ticker).
If there is a BID it puts an order $0,01 below, otherwise it puts an order at $75.25.