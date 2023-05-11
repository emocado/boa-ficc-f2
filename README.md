# Code to Connect 2023 FICC F2
# output.json for the final dataset is in FICC-code_to_connect_final_data_set/output.json
- this output.json can be created by running test_case.py

# create virtual environment and install dependencies
- python -m venv venv
- pip install -r requirements.txt

# Market Data Producer and Trade Event Data Producer
- run producer.py
- this will read from sample_events.json and stream the json data into new_sample_events.json

# Report Generator (Consumer)
- run app.py
- this will 'consume' events from new_sample_events.json by 'polling' (reading the new_sample_events.json at 3s interval) and printing the output onto the console

#  Dashboard (user interface CLI)
- run dashboard.py

