# rate is taken from fx mid event
def new_mid(rate,skew):
    return rate - skew

# net position is taken into consideration all the sequence of events of the events up till the stated event id 
# skew ratio is taken from config event 
def skew(net_position, skew_ratio, var):
    return net_position/skew_ratio*var

# this requires getting number of days and the config values from config events
def variance(m,x,b):
    x = int(x[0:-1])
    days = x*30
    return m*days + b

# spread is taken from config event
def bid(new_mid,spread):
    bid = new_mid - (0.5*spread/10000)
    return round(bid,4)

# spread is taken from config event
def ask(new_mid,spread):
    ask = new_mid + (0.5*spread/10000)
    return round(ask,4)

def change_quantity(trade):
    status = trade['BuySell']
    quantity = trade['Quantity']

    if status == 'sell':
        return -1*quantity
    return quantity

def varies(price,rate):
    min_rate = 0.9(rate)
    max_rate = 1.1(rate)
    if price < min_rate or price > max_rate:
        return True
    return False