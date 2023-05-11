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

def app():
    events = read_json('FICC-code_to_connect/sample_events.json')
    inputs = read_json('FICC-code_to_connect/sample_input.json')
    
    events_dict = convert_list_to_dict(events)
    first_input = inputs[0]

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

    quote_status = ""
    if len(all_event_types) != 0:
        quote_status = "EXCEPTION"
    

    net_quantity = 0
    for one_event in temp_event_list:
        if one_event['EventType'] == 'TradeEvent':
            if one_event['Ccy'] == first_input['Ccy'] and one_event['Tenor'] == first_input['Tenor']:
                net_quantity += calc.change_quantity(one_event)

    print(net_quantity)
    

if __name__ == '__main__':
    app()