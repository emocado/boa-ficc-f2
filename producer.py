import json
import time
import random
from os import path
import threading

def read_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    return data

def market_producer():
    # every 1-5 seconds read a json file from sample_events.json
    events = read_json('FICC-code_to_connect/sample_events.json')
    for event in events:
        if event['EventType'] == 'FXMidEvent' or event['EventType'] == 'ConfigEvent':
            time.sleep(random.randint(1,5))
            # if another json file does not exists, write else append
            if not path.isfile('new_sample_events.json') is False:
                with open('new_sample_events.json') as fp:
                    listObj = json.load(fp)
                    listObj.append(event)
                    with open('new_sample_events.json', 'w') as json_file:
                        json.dump(listObj, json_file, indent=4, separators = (',',':'))
            else:
                with open('new_sample_events.json', 'w') as json_file:
                    json.dump([event], json_file, indent=4, separators = (',',':'))

def data_producer():
    events = read_json('FICC-code_to_connect/sample_events.json')
    for event in events:
        if event['EventType'] == 'TradeEvent':
            time.sleep(random.randint(1,5))
            # if another json file does not exists, write else append
            if not path.isfile('new_sample_events.json') is False:
                with open('new_sample_events.json') as fp:
                    listObj = json.load(fp)
                    listObj.append(event)
                    with open('new_sample_events.json', 'w') as json_file:
                        json.dump(listObj, json_file, indent=4, separators = (',',':'))
            else:
                with open('new_sample_events.json', 'w') as json_file:
                    json.dump([event], json_file, indent=4, separators = (',',':'))     

if __name__ == '__main__':
    threading.Thread(target=market_producer).start()
    threading.Thread(target=data_producer).start()




