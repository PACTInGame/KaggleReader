import time
from api_calls import send_single_event_to_api, replay_events, send_data_to_api
from load_data import load_csv_data

# Daten laden
filepaths = ["cosmetic_archive/2019-Oct.csv", "cosmetic_archive/2019-Nov.csv"]
data = load_csv_data(filepaths)
print("Loaded data: Testing API")
send_single_event_to_api(data[1])
time.sleep(1)

print("Replaying all events 1000x faster")
# This takes ages. use higher factor or dump all as fast as possible using send_data_to_api...
# replay_events(data, speed_factor=1000.0)
# send_data_to_api(data)
