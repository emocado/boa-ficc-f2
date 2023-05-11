import json
# import time

def read_json(filename):

    with open(filename, 'r') as f:
        data = json.load(f)

    result = read_fx_config(data)
    return result

# Convert list of dictionaries to list of dictionaries 
def read_fx_config(filename):

    with open(filename, 'r') as f:
        data = json.load(f)

    result = {}
    for d in data:
        event_type = d['EventType']
        event_id = d['EventId']
        if event_type != 'FXMidEvent' and event_type != 'ConfigEvent':
            continue
        if event_type not in result:
            result[event_type] = {}
        result[event_type][event_id] = d
    return result

def read_trade_event(filename):

    with open(filename, 'r') as f:
        data = json.load(f)

    result = {}
    for d in data:
        event_type = d['EventType']
        event_id = d['EventId']
        if event_type != 'TradeEvent':
            continue
        if event_type not in result:
            result[event_type] = {}
        result[event_type][event_id] = d
    return result

def pricing_engine(json_data):
    fx_mid_event = {}
    config_event = {}
    trade_event = []

    fx_config_data = read_fx_config('FICC-code_to_connect/sample_events.json')
    fx_mid_event = fx_config_data['FXMidEvent']
    #get latest mid event lesser than a certain number
    for key, values in fx_mid_event.items():
        if json_data['EventId'] > key:
            fx_mid_event = values
    config_event = fx_config_data['ConfigEvent']
    


