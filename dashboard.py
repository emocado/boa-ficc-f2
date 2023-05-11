import app
import json
from prettytable import PrettyTable
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

def get_latest_config(event_id, event_list):
    latest_config = None
    for event in event_list.values():
        if event[0]['EventType'] == 'ConfigEvent':
            latest_config = event
        if event[0]['EventId'] == event_id:
            break

    return latest_config

def get_latest_fx(event_id, event_list):
    latest_fx = None
    fx_dict = {}
    for event in event_list.values():
        if event[0]['EventType'] == 'FXMidEvent' and event[0]['Ccy'] not in fx_dict:
            latest_fx = event
            fx_dict[event[0]['Ccy']] = event[0]['rate']
        
        else: 
            if event[0]['EventType'] == 'FXMidEvent' and event[0]['Ccy'] in fx_dict:
                if event[0]['EventId'] > latest_fx[0]['EventId']:
                    fx_dict[event[0]['Ccy']] = event[0]['rate']
                    latest_fx = event

        if event[0]['EventId'] == event_id:
            break
    return fx_dict

def dashboard():
    events = read_json('new_sample_events.json')

    events_dict = convert_list_to_dict(events)
    events_dict = dict(sorted(events_dict.items()))
    output_dict = {}
    latest_config = None
    latest_fx = None
    table = PrettyTable(['Ccy', 'Tenor', 'Position', 'Bid', 'Ask', 'QuoteStatus'])
    temp = []
    for key, item in events_dict.items():
        print(key,item)
        # need to get latest fx
        latest_config = get_latest_config(key,events_dict)
        latest_fx = get_latest_fx(key,events_dict)

        if latest_config == None or latest_fx == None:
            continue

        print('-----------------------------------------------------DASHBOARD-----------------------------------------------------')
        print('EventId: ', key)
        print('Event Type: ', item[0]['EventType'])
        # get the latest config
        print('Config', latest_config[0])
        # get the latest fx
        print('FX', latest_fx)

        if item[0]['EventType'] == 'TradeEvent':
            # find the corresponding output in output.json
            output = app.process_one_json_input(events_dict,item[0])
            output_dict[output['Ccy']] = output
        for i in output_dict.values():
            table.add_row([i['Ccy'], i['Tenor'], i['Position'], i['Bid'], i['Ask'], i['QuoteStatus']])

        print(table)
        table.clear_rows()

        print('-------------------------------------------------------------------------------------------------------------------')
        
    
if __name__ == '__main__':
    dashboard()


