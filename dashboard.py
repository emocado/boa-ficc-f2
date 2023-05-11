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
            fx_dict[event[0]['Ccy']] = event
        
        else: 
            if event[0]['EventType'] == 'FXMidEvent' and event[0]['Ccy'] in fx_dict:
                if event[0]['EventId'] > fx_dict[event[0]['Ccy']][0]['EventId']:
                    fx_dict[event[0]['Ccy']] = event
                    latest_fx = event

        if event[0]['EventId'] == event_id:
            break
    return fx_dict

def dashboard():
    events = read_json('new_sample_events.json')

    events_dict = convert_list_to_dict(events)
    events_dict = dict(sorted(events_dict.items()))
    output = []
    latest_config = None
    latest_fx = None
    for key, item in events_dict.items():
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

        table = PrettyTable(['Ccy', 'Tenor', 'Position', 'Bid', 'Ask', 'QuoteStatus'])
        for i in range(1, key+1):
            temp_event_list = []
            for event in events_dict[i]:
                if event['EventType'] == 'TradeEvent':
                    temp_event_list.append(event)
            if len(temp_event_list) == 0:
                continue
            for event in temp_event_list:
                if event['EventType'] == 'TradeEvent':
                    table.add_row([event['Ccy'], event['Tenor'], event['Position'], event['Bid'], event['Ask'], event['QuoteStatus']])

        print(table)


        
    
if __name__ == '__main__':
    dashboard()


