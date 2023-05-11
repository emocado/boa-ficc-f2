from app import process_one_json_input, convert_list_to_dict, read_json
import json

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
    sample_test_case()
    with open('FICC-code_to_connect_final_data_set/output.json', 'w') as f:
        json.dump(final_test_case(), f)