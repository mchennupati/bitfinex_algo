def orderbook_to_df(trim_ob):      # converts orderbook to binned ranges.
    
    bids_amount = []
    bids_px = []
    asks_amount = []
    asks_px = []
    
    for i in trim_ob['bids']:
        bids_amount.append(i[0])
        bids_px.append(i[1])
    
    bids_dict = {'amount': bids_amount, 'px' : bids_px}

    for j in trim_ob['asks']:
        asks_amount.append(j[0])
        asks_px.append(j[1])
    
    asks_dict = {'amount': asks_amount, 'px' : asks_px}

    asks_df = pd.DataFrame.from_dict(asks_dict)
    bids_df = pd.DataFrame.from_dict(bids_dict)
    
    return [asks_df,bids_df]

def orderbook_tobins(symbol = 'btcusd', price = 6500.0, percent = 0.01, lag = 3.0):
    
    px_before = ticker(symbol)['last_price']
    trim_ob = trim_orderbook(symbol = symbol, current_price = float(px_before), percent = percent)
        
    time.sleep(lag)
    
    px_after = ticker(symbol)['last_price']
    trim_ob_after = trim_orderbook(symbol = symbol, current_price = float(px_after), percent =  percent)  #poll orderbook after 2s
    
    
    asks_df = orderbook_to_df(trim_ob)[0]
    bids_df = orderbook_to_df(trim_ob)[1]
    
    asks_df_after = orderbook_to_df(trim_ob_after)[0]
    bids_df_after = orderbook_to_df(trim_ob_after)[1]
    
    asks_bins = np.linspace(asks_df.px.min(),asks_df.px.max(),5)  # use same bins
    bids_bins = np.linspace(bids_df.px.min(),bids_df.px.max(),5) # use same bins
    
    grouped_asks = asks_df.groupby(pd.cut(asks_df.px,asks_bins))
    grouped_bids = bids_df.groupby(pd.cut(bids_df.px,bids_bins))
    
    grouped_asks_after = asks_df_after.groupby(pd.cut(asks_df_after.px,asks_bins))  #use same bins
    grouped_bids_after = bids_df_after.groupby(pd.cut(bids_df_after.px,bids_bins))  #use same bins
    
    binned_asks  = grouped_asks.sum().amount
    binned_bids = grouped_bids.sum().amount.sort_index(ascending = False)
    
    binned_asks_after  = grouped_asks_after.sum().amount
    binned_bids_after = grouped_bids_after.sum().amount.sort_index(ascending = False)
    
    change_asks = (binned_asks_after - binned_asks).sum()  # change the return statement to change_asks-change_bids 
    change_bids = (binned_bids_after - binned_bids).sum()  # if you need a simple signal
    
    return [grouped_asks.sum().amount, grouped_bids.sum().amount]     
