
""" Status: be able to communicate with the server. """


# Import the protobuf python file
import satellite_pb2

# Try creating a satellite request, modify its fields
this_req = satellite_pb2.SatelliteRequest();
this_req.sat_id = 69;
this_req.req_type = satellite_pb2.SatelliteRequest.RequestType.LOCATION_REQ;

# Serialize this_req to a string
serial_req = this_req.SerializeToString();

# Try writing the shit to a file for now
with open("sample_database.txt", "w") as open_file:
    open_file.write(serial_req.decode());

