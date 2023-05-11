import json
import calculations as calc
import time
from collections import defaultdict

def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data

def convert_list_to_dict(data):
    result = defaultdict(list)
    for d in data:
        event_id = d['EventId']
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

def sample_test_case():
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
            break
    else:
        print("passed")
    
def final_test_case():
    events = read_json('FICC-code_to_connect_final_data_set/events.json')
    inputs = read_json('FICC-code_to_connect_final_data_set/input.json')
    
    events_dict = convert_list_to_dict(events)
    
    res = []
    for input in inputs:
        res.append(process_one_json_input(events_dict, input))
    print("passed")
    return res
    
if __name__ == '__main__':
    # sample_test_case()
    # with open('FICC-code_to_connect_final_data_set/output.json', 'w') as f:
    #     json.dump(final_test_case(), f)

    events_dict = defaultdict(list)
    inputs = read_json('FICC-code_to_connect/sample_input.json')
    inputs_dict = convert_list_to_dict(inputs)
    my_outputs = defaultdict(list)
    events = []

    while True:
        new_events = read_json('new_sample_events.json')
        if not events_dict:
            events = new_events
            events_dict = convert_list_to_dict(new_events)
            for event_id in events_dict:
                for input in inputs_dict[event_id]:
                    my_output = process_one_json_input(events_dict, input)
                    my_outputs[event_id].append(my_output)
        else:
            latest_event_jsons = new_events[len(events):]
            events = new_events
            for event_json in latest_event_jsons:
                event_id = event_json['EventId']
                events_dict[event_id].append(event_json)
                if event_id in inputs_dict:
                    for input in inputs_dict[event_id]:
                        my_output = process_one_json_input(events_dict, input)
                        my_outputs[event_id].append(my_output)
        print("my_outputs:", my_outputs)
        time.sleep(3)
