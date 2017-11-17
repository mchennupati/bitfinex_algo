# bitfinex_algo
Orderbook based trading algorithm for Bitfinex, based on open source from jndok and dawsbot

Best used in a jupyter notebook, the python requests.get is used with a proxyDict.Y You might need to modify that if you don't need to use a proxy.

The api files are based on jndok and dawsbot. bitfinex/FinexAPI/FinexAPI.py

In order to take it further, a few other functions were added and a working trading algorithm was implemented.

trim_orderbook : This trims the orderbook to a % of the current price. So that bids and offers that are far away can be removed.

simple_strategy: This relies on the calculation of imbalance in the trimmed orderbook to decide if a trade needs to be entered into.




