# rate is taken from fx mid event
def new_mid(rate,skew):
    return rate - skew

# net position is taken into consideration all the sequence of events of the events up till the stated event id 
# skew ratio is taken from config event 
def skew(net_position, skew_ratio, var):
    return net_position/skew_ratio*var

# this requires getting number of days and the config values from config events
def variance(m,x,b):
    days = x*30
    return m*days + b

# spread is taken from config event
def bid(new_mid,spread):
    return new_mid - (0.5*spread/10000)

# spread is taken from config event
def ask(new_mid,spread):
    return new_mid + (0.5*spread/10000)
