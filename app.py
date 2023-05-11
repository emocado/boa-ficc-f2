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

def process_one_json_input(events_dict, first_input):
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
    
    # check if TradeEvent is present in all_event_types
    trade_exist = False
    if "TradeEvent" not in all_event_types:
        net_quantity = "NA"
        quote_status = "EXCEPTION"
    else:
        net_quantity = 0
        for one_event in temp_event_list:
            if one_event['EventType'] == 'TradeEvent':
                if one_event['Ccy'] == first_input['Ccy'] and one_event['Tenor'] == first_input['Tenor']:
                    trade_exist = True
                    net_quantity += calc.change_quantity(one_event)

    small_output_json = {
        "EventId": None, 
        "Ccy": None,
        "Tenor": None,
        "Position": "NA",
        "Bid": "NA",
        "Ask": "NA",
        "QuoteStatus": None
    }

    small_output_json['EventId'] = first_input['EventId']
    small_output_json['Ccy'] = first_input['Ccy']
    small_output_json['Tenor'] = first_input['Tenor']
    small_output_json['Position'] = net_quantity if trade_exist else "NA"
    small_output_json['QuoteStatus'] = quote_status if trade_exist else "EXCEPTION"

    return small_output_json
   
def app():
    events = read_json('FICC-code_to_connect/sample_events.json')
    inputs = read_json('FICC-code_to_connect/sample_input.json')
    
    events_dict = convert_list_to_dict(events)
    print(process_one_json_input(events_dict, inputs[0]))

    
    

if __name__ == '__main__':
    app()