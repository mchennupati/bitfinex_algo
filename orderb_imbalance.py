def trades(symbol='btcusd'): # get a list of the most recent trades for the given symbol.

	r = requests.get(URL + "/trades/" + symbol, verify=True, proxies = proxyDict )
	rep = r.json()

	return rep

def trim_orderbook(symbol = 'BTCUSD',current_price = 7200.0, percent = 0.02) :
    orig = orderbook(symbol)
    trim_bids = []
    for k in orig['bids']:
        if float(k['price']) > current_price*(1-percent):
            trim_bids.append([float(k['amount']),float(k['price']),float(k['timestamp'])])
            
    trim_asks = []
    for t in orig['asks']:
        if float(t['price']) < current_price*(1+percent):
            trim_asks.append([float(t['amount']),float(t['price']),float(t['timestamp'])])
    
    trim_book = {'bids': trim_bids, 'asks': trim_asks}
           
    return trim_book
            
            
def current_relevant_price(symbol = 'BTCUSD', threshold = 100.0):
    
    trades_list = trades(symbol)
    time_now = datetime.datetime.now().timestamp()
    
    volume = 0.0
    price_volume = 0.0
    
    for j in trades_list:
           if time_now - float(j['timestamp'])< threshold :  #1 min from now#
                volume = volume + float(j['amount'])
                price_volume = price_volume + float(j['amount'])* float(j['price'])
    result = price_volume/volume
    if volume == 0:
        return "volume zero error"
    else:
        return [result, volume]

def simple_strategy(price = 7150.0, symbol = 'BTCUSD'):
    book = trim_orderbook(current_price = price, percent = 0.01, symbol = symbol)
    bid_list = book['bids'] #get a list of bids and size
    ask_list = book['asks'] # get a list of asks and sizes
    
    sum_bids = 0
    sum_asks = 0
    
    for m in bid_list:
        sum_bids = sum_bids + m[0]
    for n in ask_list:
        sum_asks = sum_asks + n[0]
    
    return sum_bids - sum_asks
    
    def opp_traded(side = 'buy'):
                if side == 'buy':
                    return 'sell'
                elif side == 'sell':
                    return 'buy'
                
def active_position(symbol = 'btcusd'):
    act = active_positions()
    if act != []:
        for j in act:
            if j['symbol'] == symbol:
                return j['amount']
            else:
                return 0
    else :
        return 0

def run_algo():  # if condition is satisifed runs a trade 10 times, 

  for t in range(0,10):  # run the strategy 10 times

      time.sleep(3)  #wait for 3s before starting the next strategy - arbitrary

      symbol = 'btcusd'
      size = '0.01'                                    # size in coins

      imbalance = 30.0           # orderbook imbalance to act on
      pnl_gain_threshold = 6.00       # pnl threshold to close +ve position
      pnl_loss_threshold = -2.00      # # pnl threshold to close -ve position


      init_price = float(ticker(symbol)['last_price'])
      init_weight = simple_strategy(init_price,symbol)  # relies on the imbalance of bids/offers as defined in function above.

      if init_weight > imbalance and active_position(symbol) == 0:
          p = place_order(size,str(init_price),'buy','market', symbol = symbol)   # Initiate buy position
      elif init_weight < imbalance*-1.0 and active_position(symbol) == 0:
          p = place_order(size,str(init_price),'sell','market', symbol = symbol)  # Or initiate sell position
      else:
          p = []
          print('thresholds not satisfied to initiate position ,' + '{0:.0f}'.format(init_weight) + ',' + '{0:.7f}'.format(init_price))


      if p != []:

          time.sleep(5)  # wait 10s before trade is executed.

          status = status_order(p['id'])

          #not_executed = status['is_live']  #check if order is executed
          traded = status['side']

          print(status['side']+' ' + status['executed_amount'] +' ' + status['avg_execution_price'])

          if status['is_live'] == False:
              start_price = status['avg_execution_price']
              size_start = status['executed_amount']
              sign = [-1,1][traded == 'buy']

              for i in range(0,60):     # start monitoring every (4 + computing times) for 60 times
                  time.sleep(2)
                  price = float(ticker(symbol)['last_price'])
                  pnl = float(size_start)*(price-float(start_price))*sign
                  print('{0:.7f}'.format(pnl) + ',' + '{0:.7f}'.format(price))
                  if pnl > pnl_gain_threshold:
                          if active_position('symbol') == size:
                              t1 = place_order(size,str(price),opp_traded(traded),'market',symbol = symbol)
                              print(t1)
                              print(status_order(t1['id']))
                          break
                  elif pnl < pnl_loss_threshold:
                          if active_position('symbol') == size:
                              t2 = place_order(size,str(price),opp_traded(traded),'market',symbol = symbol)
                              print(t2)
                              print(status_order(t2['id']))
                          break

          # if time passes with pnl within range exit position.
              time.sleep(5)
              live_position = float(active_position(symbol))
              if live_position != 0:
                  order_to_close = ['buy', 'sell'][live_position > 0.0]
                  final_order = place_order(str(abs(live_position)),str(price),order_to_close,'market', symbol = symbol)

              print(active_position(symbol))


      else:
          print('no orders executed')

                        
       
