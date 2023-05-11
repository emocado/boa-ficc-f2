import json
import calculations as calc

def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data

def convert_list_to_dict(data):
    result = {}
    for d in data:
        event_id = d['EventId']
        if event_id not in result:
            result[event_id] = []
        result[event_id].append(d)
    return result

def process_one_json_input(events_dict,first_input):
    small_output_json = {
        "EventId": first_input['EventId'], 
        "Ccy": first_input['Ccy'],
        "Tenor": first_input['Tenor'],
        "Position": "NA",
        "Bid": "NA",
        "Ask": "NA",
        "QuoteStatus": "EXCEPTION"
    }
    event_id = first_input['EventId']
    temp_event_list = []
    all_event_types = set(("TradeEvent", "FXMidEvent", "ConfigEvent"))
    for i in range(1, event_id+1):
        temp_event_list.extend(events_dict[i])

    # check if all event types are present
    for event in temp_event_list:
        event_type = event['EventType']
        if event_type in all_event_types:
            all_event_types.remove(event_type)

    # check if TradeEvent is present in all_event_types
    if 'TradeEvent' in all_event_types:
        return small_output_json
    
    trade_exist = False
    
    net_quantity = 0
    for one_event in temp_event_list:
        if one_event['EventType'] == 'TradeEvent':
            if one_event['Ccy'] == first_input['Ccy'] and one_event['Tenor'] == first_input['Tenor']:
                trade_exist = True
                net_quantity += calc.change_quantity(one_event)
    if not trade_exist:
        return small_output_json
    # check if FXMidEvent or ConfigEvent is present in all_event_types
    if 'FXMidEvent' in all_event_types or 'ConfigEvent' in all_event_types:
        small_output_json['Position'] = net_quantity
        return small_output_json


    for event in temp_event_list:
        if event['EventType'] == 'FXMidEvent' and event['Ccy'] == first_input['Ccy']:
            latest_FXMidEvent = event
        elif event['EventType'] == 'ConfigEvent':
            latest_ConfigEvent = event

    rate = latest_FXMidEvent['rate']
    skew_ratio = latest_ConfigEvent['DivisorRatio']
    spread = latest_ConfigEvent['Spread']
    m = latest_ConfigEvent['m']
    b = latest_ConfigEvent['b']
    tenor = first_input['Tenor']

    # calculate variance
    variance = calc.variance(m, tenor, b)
    # calculate skew
    skew = calc.skew(net_quantity, skew_ratio, variance)
    # calculate new_mid
    new_mid = calc.new_mid(rate, skew)
    # calculate bid
    bid = calc.bid(new_mid, spread)
    # calculate ask
    ask = calc.ask(new_mid, spread)

    small_output_json["Bid"] = bid
    small_output_json["Ask"] = ask
    small_output_json["Position"] = net_quantity
    small_output_json["QuoteStatus"] = "TRADABLE"
    if bid > ask or calc.varies(bid, rate) or calc.varies(ask, rate):
        small_output_json["QuoteStatus"] = "NON-TRADABLE"
    
    return small_output_json

def app():
    events = read_json('FICC-code_to_connect/sample_events.json')
    inputs = read_json('FICC-code_to_connect/sample_input.json')
    outputs = read_json('FICC-code_to_connect/sample_output.json')
    
    events_dict = convert_list_to_dict(events)
        
    for i, input in enumerate(inputs):
        my_output = process_one_json_input(events_dict, input)
        if my_output != outputs[i]:
            print("Wrong")
            print(my_output)
            print(outputs[i])
    
    
if __name__ == '__main__':
    app()