
# ayyy commit this my guy from GENESIS

import satellite_pb2

# Reads the data written in sample_database.txt

read_sat_req = satellite_pb2.SatelliteRequest();

with open("sample_database.txt", 'r') as open_file:
    read_data = bytes(open_file.read(), 'utf-8');

read_sat_req.ParseFromString(read_data);

print(read_sat_req.sat_id);

