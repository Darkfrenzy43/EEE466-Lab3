
"""
    Author: OCdt Liethan Velasco and OCdt Aaron Brown
    Version: Oct 9, 2023

    Description:
        This file serves as the python script that facilitates the communication behaviors via the protobuf file
        satellite.proto between the simulated ground station and satellite. More specifically, this scripts
        handles communications on the ground station's side.


    Status:
        1. Establish a UDP connection with the satellite server.

    Notes:

        1.


"""

# --- Importing Libraries ---

import GroundStation    # <-- Contains the GroundStation class
import satellite_pb2    # <-- Has the protobuf python script



# Import socket library
import socket;

# --- Defining Global Variables ---

# For convenience, creating a server address var
satellite_addr = ('localhost', 4444);

# --- Defining Functions ---



# --- Main Entry Point ---

# Create ground station object, try taking a request
this_gs = GroundStation.GroundStation(satellite_addr);

# Put in a while true loop for now
while True:
    this_gs.process_request();


