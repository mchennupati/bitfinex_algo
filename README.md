# An orderbook based trading algorithm for bitfinex

Orderbook based trading algorithm for Bitfinex, based on open source from jndok and dawsbot. Please use at own risk !

Best used in a jupyter notebook, the python requests.get is used with a proxyDict. You might need to modify that if you don't need to use a proxy. You will also need to enter your own api keys to use Bitfinex.

The api files are based on the interface from work by jndok and dawsbot. bitfinex/FinexAPI/FinexAPI.py

In order to take it further, a few other functions were added and a working trading algorithm was implemented.

trim_orderbook : This trims the orderbook to a % of the current price. So that bids and offers that are far away can be removed.

simple_strategy: This relies on the calculation of imbalance in the trimmed orderbook to decide if a trade needs to be entered into.

run_algo: This implements the trading algorithm. It works in the following way.

A loop runs every n+(computation time) times to check if the imbalance is beyond a certain threshold. For e.g, if the amount of bids - amount of offers > 60.0, then enter a buy order.

Once a buy order is triggered, the trade is monitored for a certain amount of time. lag (=2s sat) * 60 seconds. Every 2s, the pnl is calculated and if it exceeds the gain or the loss, it's closed out. If at the end of the period, pnl is within threshold, the position is still closed.

A better strategy would be based on monitoring the orderbook changes. In order to measure the change, as the price changes, the only meaningful measure is splitting the prices into ranges (bins).  These functions are implemented in orderbook_monitor.

The code can be used to trade any cryptoccy pair by changing the symbol.





