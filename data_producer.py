import json
import time

def read_json(filename):

    with open(filename, 'r') as f:
        data = json.load(f)

    result = convert_list_to_dict(data)
    return result


# Convert list of dictionaries to list of dictionaries 
def convert_list_to_dict(data):
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

def data_producer():
    data = read_json('FICC-code_to_connect/sample_events.json')
    return data
    # simulate streaming data by chunking the data and print it with 1 second interval
    # for event_type in data:
    #     for event_id in data[event_type]:
    #         yield data[event_type][event_id]
    #         time.sleep(1)
    


if __name__ == '__main__':
    print(data_producer())
    