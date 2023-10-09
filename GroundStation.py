"""
    Author: OCdt Liethan Velasco and OCdt Aaron Brown
    Version: October 9, 2023

    Description:

        This python file contains the GroundStation class. This file facilitates the UDP communications between
        the groundstation and the satellite.


    Status:

        1. Implement quit functionality
        2. Implement timeout/re-attempt functionality
        3. Refactor the code.


    Notes:

        1. For now, we'll be assuming the message responses will all be less than 50 bytes. Accordingly, the
        receive buffer will be set globally to 50 bytes.

        2. Guess I'll be efficient in converting the unix time to a readable format with the datetime module.
        Honestly, it would be needlessly complicated making my own algorithm to find the current year, then especially
        the current month and day, etc. BECAUSE NOT ALL MONTHS ARE THE SAME LENGTH. Might as well make things easier
        for myself :/ unless if that's not allowed. oops.


"""

# --- Importing Libraries ---

import socket # To use the socket libraries
import satellite_pb2 # To use the protobuf python classes
from datetime import datetime # For the time conversions


# --- Defining Global Variables ---

RECV_BUFFER_SIZE = 50;

# --- Defining the Class ---

class GroundStation:

    def __init__(self, satellite_addr):
        """ Constructor. Initializes the object that will communicate with the satellite via UDP.

        Args:
            <satellite_addr : (IP addr, port) > : The satellite to send the UDP traffic to.
        """

        # Save the satellite address
        self.satellite_addr = satellite_addr;

        # Initialize the ground station UDP socket
        self.gs_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"GS STATUS: UDP socket created. Sending traffic to satellite address at {self.satellite_addr}.");

        # Initialize a request counter to assign as Message IDs
        self.req_count = 0;


    def process_request(self):
        """ Method prompts user for which request type they would like to send to the satellite.
        Requests further input and calls the applicable send method depending on the user input. Accounts for bad input.

        todo: how will we handle the quit requests in this case?
        """

        # Initialize dummy vars to avoid warnings
        in_angle = 0;
        in_dura = 0;

        # Create requests list for good input
        request_types = ['location', 'time', 'move'];

        # Use while true loop to handle bad input
        while True:

            # Get user_input, clean it up
            user_input = input("\nSelect a request type to send to satellite [ 'location' | 'time' | 'move' ]: ");
            user_input = user_input.strip().lower();

            # If input unrecognized, re-prompt user. Otherwise, break.
            if user_input in request_types:

                # If input was move, get duration and angle. Handle bad input.
                if user_input == 'move':
                    try:
                        in_angle = float(input("Thruster angle (can be decimal): ").strip());
                        in_dura = float(input("Duration to fire thrusters (can be decimal): ").strip());
                    except ValueError:
                        print("GS ERROR: Input could not be converted to decimal. Try again.");
                        continue;
                break;

            else:
                print(">>> GS ERROR: Input unrecognized. Try again. <<<");


        # Have a timeout counter and timer here, probably with a loop of sorts

        # With user input, call the appropriate send method to process request, then capture response
        if user_input == 'location':

            # Call the method to send a location request and capture response
            loca_resp = self.process_loca_request();

            # Check here if response was certain characters to indicate timeout, restart as needed.

            # Display the LocationResponse fields.
            print(f"SATELLITE REPLY: Location is longitude = {loca_resp.longitude}, latitude = {loca_resp.latitude}.");

        elif user_input == 'time':

            # Call the method to send a time request and capture response
            time_resp = self.process_time_request();

            # Check here if response was certain characters to indicate timeout, restart as needed.

            # Display the TimeResponse fields.
            print(f"SATELLITE REPLY: Current satellite time is {self.unix_to_curr(time_resp.curr_time)}.");


        elif user_input == 'move':

            # Call method to send a move request and capture response
            move_resp = self.process_move_request(in_angle, in_dura);

            # Check here if response was certain characters to indicate timeout, restart as needed.

            # Display the MoveResponse fields.
            print(f"SATELLITE REPLY: Move response code {move_resp.resp_code}. "
                  f"New position: \n{move_resp.updated_loca}");


    def process_loca_request(self):
        """ Method sends a location request to the satellite.

        Returns: the reply as a LocationResponse message class object.
        """

        # Create the request
        loca_req = satellite_pb2.SatelliteRequest();
        loca_req.sat_id = self.req_count;
        loca_req.req_type = satellite_pb2.SatelliteRequest.RequestType.LOCATION_REQ;

        # Increment request count for next request ID
        self.req_count += 1;

        # Send request to satellite, wait for response
        send_msg = loca_req.SerializeToString();
        self.gs_socket.sendto(send_msg, self.satellite_addr);
        print(f"GS STATUS: Location request (ID {loca_req.sat_id}) sent to satellite. Waiting for response...");
        recv_msg = self.gs_socket.recv(RECV_BUFFER_SIZE);

        # PROCESS TIME OUT CODE HERE - RETURN EMPTY RESPONSE AFTER CERTAIN TIME

        # When response received, return it as a LocationResponse
        loca_resp = satellite_pb2.SatelliteResponse.LocationResponse();
        loca_resp.ParseFromString(recv_msg);
        return loca_resp;


    def process_time_request(self):
        """ Method sends a time request to the satellite.

        Returns: the reply as a TimeResponse message class object.
        """

        # Create the request
        time_req = satellite_pb2.SatelliteRequest();
        time_req.sat_id = self.req_count;
        time_req.req_type = satellite_pb2.SatelliteRequest.RequestType.TIME_REQ;

        # Increment request count for next request ID
        self.req_count += 1;

        # Send request to satellite, wait for response
        send_msg = time_req.SerializeToString();
        self.gs_socket.sendto(send_msg, self.satellite_addr);
        print(f"GS STATUS: Time request (ID {time_req.sat_id}) sent to satellite. Waiting for response...");
        recv_msg = self.gs_socket.recv(RECV_BUFFER_SIZE);

        # PROCESS TIME OUT CODE HERE - RETURN EMPTY RESPONSE AFTER CERTAIN TIME

        # When response received, return it as a LocationResponse
        time_resp = satellite_pb2.SatelliteResponse.TimeResponse();
        time_resp.ParseFromString(recv_msg);
        return time_resp;


    def process_move_request(self, thrust_angle, thrust_dura):
        """ Method sends a move request to the satellite.

        Args:
            <thrust_angle : double> : The angle to aim the satellite thrusters at.
            <thrust_dura : double> : The duration to fire the satellite thrusters for.
            Returns: the reply as a MoveResponse message class object.
        """

        # Create the request
        move_req = satellite_pb2.SatelliteRequest();
        move_req.sat_id = self.req_count;
        move_req.req_type = satellite_pb2.SatelliteRequest.RequestType.MOVE_REQ;
        move_req.thrust_angle = thrust_angle;
        move_req.thrust_dura = thrust_dura;

        # Increment request count for next request ID
        self.req_count += 1;

        # Send request to satellite, wait for response
        send_msg = move_req.SerializeToString();
        self.gs_socket.sendto(send_msg, self.satellite_addr);
        print(f"GS STATUS: Time request (ID {move_req.sat_id}) sent to satellite. Waiting for response...");
        recv_msg = self.gs_socket.recv(RECV_BUFFER_SIZE);

        # PROCESS TIME OUT CODE HERE - RETURN EMPTY RESPONSE AFTER CERTAIN TIME

        # When response received, return it as a LocationResponse
        move_resp = satellite_pb2.SatelliteResponse.MoveResponse();
        move_resp.ParseFromString(recv_msg);
        return move_resp;

        pass;


    def unix_to_curr(self, in_unix_time):
        """ Method converts an inputted unix time into a [Day Month Year HH:MM:SS] format. Uses datetime module.
        Note: Unix time is the elapsed time from January 1, 1970

        Args:
            <in_unix_time : int> : The current unix time in ms.
            Returns: The formatted time in a string.
        """

        # Convert ms to seconds, then convert with datetime and return
        in_unix_time /= 1000;
        return datetime.utcfromtimestamp(in_unix_time).strftime('%d %m %Y %H:%M:%S');






