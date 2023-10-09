
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




# Import socket library
import socket;

# --- Defining Global Variables ---

satellite_addr = ('localhost', 4444); # For convenience, creating a server address var

# --- Defining Functions ---


# --- Main Entry Point ---

# Create ground station object. Invoke its main loop method
this_gs = GroundStation.GroundStation(satellite_addr);
this_gs.run_ground_station();
