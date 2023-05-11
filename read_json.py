import json

def read_json(filename):

    with open(filename, 'r') as f:
        data = json.load(f)

    result = convert_list_to_dict(data)
    return result


# Convert list of dictionaries to list of dictionaries 
def convert_list_to_dict(data):
    result = {}
    for d in data:
        event_id = d['EventId']
        if event_id not in result:
            result[event_id] = []
        result[event_id].append(d)
    return result

if __name__ == '__main__':
    print(read_json('FICC-code_to_connect/sample_events.json'))