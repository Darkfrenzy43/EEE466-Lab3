"""
    Author: OCdt Liethan Velasco and OCdt Aaron Brown
    Version: October 9, 2023

    Description:

        This python file contains the GroundStation class. This file facilitates the UDP communications between
        the groundstation and the satellite.


    Notes:

        1. For now, we'll be assuming the message responses will all be less than 50 bytes. Accordingly, the
        receive buffer will be set globally to 50 bytes.

        2. Guess I'll be efficient in converting the unix time to a readable format with the datetime module.
        Honestly, it would be needlessly complicated making my own algorithm to find the current year, then especially
        the current month and day, etc. BECAUSE NOT ALL MONTHS ARE THE SAME LENGTH. Might as well make things easier
        for myself :/ unless if that's not allowed. oops.

        3. So if we want the socket to have 3 seconds to re-attempt 5 times to receive data from the satellite,
        then that means we have to set the timeout time to 0.6 seconds.

"""

# --- Importing Libraries ---

import socket # To use the socket libraries
import satellite_pb2 # To use the protobuf python classes
from datetime import datetime # For the time conversions

from enum import Enum; # Will need this to use enumerated constants


# --- Defining Global Variables ---

RECV_BUFFER_SIZE = 50;

# --- Defining the Class ---

class RequestType(Enum):
    """ Defines the request type constants that is used by the ground station.
    Setting the constants to their string equivalents for program flow convenience (only a python thing lol). """
    LOCA = 'location';
    TIME = 'time';
    MOVE = 'move';
    QUIT = 'quit';


class GroundStation:

    def __init__(self, satellite_addr):
        """ Constructor. Initializes the object that will communicate with the satellite via UDP.

        Args:
            <satellite_addr : (IP addr, port) > : The satellite to send the UDP traffic to.
        """

        # Initialize a request counter to assign as Message IDs
        self.req_count = 0;

        # Save the satellite address
        self.satellite_addr = satellite_addr;

        # Initialize the ground station UDP socket
        self.gs_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"\nGS STATUS: UDP socket created. Sending traffic to satellite address at {self.satellite_addr}.");

        # Set up the timeout time - if socket is blocking for more than this duration of time in seconds,
        # then the socket unblocks. Timeout time set to 0.6 seconds (5 attempts will take 3 seconds)
        self.gs_socket.settimeout(0.6);



    def run_ground_station(self):
        """ Method handles entire execution of the ground station program. Essentially contains the main
        while loop. This design choice was made to make the ground_station_main.py script as minimal as possible. """

        print("GS STATUS: Ground station program commencing main loop.");

        # Create dummy var to contain move request input should user request it
        move_input = (0, 0);

        # Main while loop
        while True:

            # Run method to get good user input
            user_input = self.get_input();

            # If user wants to send 'move' request, get the thrust angle and duration input
            if user_input == RequestType.MOVE:
                move_input = self.get_move_info();

            # If the user inputted 'quit', terminate the main while loop method
            elif user_input == RequestType.QUIT:
                print("GS STATUS: Detected quit request. Terminating ground station program.");
                break;

            # Set up the request to be sent to the satellite (request ID)
            send_req = satellite_pb2.SatelliteRequest();
            send_req.sat_id = self.req_count;
            self.req_count += 1;    # <-- Increment request count for next request's ID

            # Further set up the request depending on the user's input (request type, thrust angle and dura for 'move')
            if user_input == RequestType.LOCA : send_req.req_type = satellite_pb2.SatelliteRequest.RequestType.LOCATION_REQ;
            elif user_input == RequestType.TIME : send_req.req_type = satellite_pb2.SatelliteRequest.RequestType.TIME_REQ;
            elif user_input == RequestType.MOVE :
                send_req.req_type = satellite_pb2.SatelliteRequest.RequestType.MOVE_REQ;
                send_req.thrust_angle = move_input[0]; send_req.thrust_dura = move_input[1];

            # Pass the request to the send_request() method. Capture the satellite's serialized reply
            satellite_reply = self.send_request(send_req);

            # If satellite_reply is an empty byte string, means satellite never
            # sent a reply. Re-prompt user to input another request.
            if satellite_reply == b'':
                print("GS STATUS: Satellite never replied after 5 send attempts. Input another request.");
                continue;


            # Otherwise, display satellite reply accordingly with display_response() method
            self.display_response(satellite_reply, user_input);

    def get_input(self):
        """ Method prompts user for which request type they would like to send to the satellite. Handles
         bad input (unrecognized input, etc). Recognized inputs include: 'location', 'time', 'move', 'quit'.
         If the user inputs bad input, re-prompt user until we get good input.

        Returns: the RequestType enumerated constant equivalent of the input.
         """

        # Create requests list for good input
        request_type_list = ['location', 'time', 'move', 'quit'];

        # While true loop for good input
        while True:

            # Get user_input, clean it up
            user_input = input("\nSelect a request type to send to satellite "
                               "[ 'location' | 'time' | 'move' | 'quit' ]: ");
            user_input = user_input.strip().lower();

            # See if input is recognized. If so, return the user_input in the
            # RequestType enumerated constant equivalent. If not, re-prompt user.
            if user_input in request_type_list:
                return RequestType(user_input);
            else:
                print(">>> GS ERROR: Input unrecognized. Try again. <<<");


    def get_move_info(self):
        """ This method is called when the user wishes to send a move request. Prompts the user to input two
        float values that tell the satellite which angle and for what duration to fire the thrusters at.
        If user inputs bad input (input that can't be converted to float), re-prompts user.

        Returns: a tuple of floats - (<thruster angle : float>, <thrust duration : float>)
        """

        # Setting up two dummy vars for input values
        in_angle = 0;
        in_dura = 0;

        # Use two separate while true loops for each input value
        while True:

            try:
                in_angle = float(input("Input thruster angle (can be decimal): ").strip());
                break;
            except ValueError:
                print(">>> GS ERROR: Input for thruster angle unable to be converted to float. Try again. <<<");
                continue;

        while True:

            try:
                in_dura = float(input("Input thruster duration (can be decimal): ").strip());
                break;
            except ValueError:
                print(">>> GS ERROR: Input for thruster duration unable to be converted to float. Try again. <<<");
                continue;

        # Return the inputted values in tuple
        this_tup = (in_angle, in_dura);
        return this_tup;



    def send_request(self, in_request):
        """ Method sends the inputted request to the satellite server. The request must already be serialized
        by the satellite.proto protobuf protocol. Also returns the SERIALIZED reply from the satellite -
        if the satellite does not reply, the ground station will re-attempt to send the request again a total of 5
        times in 3 seconds. If satellite still does not reply in the 5 attempts, returns an empty byte string to
        indicate timeout failure.

        Args:
            <in_request : satellite_pb2.SatelliteRequest > : The non-serialized request to send to the server.
            Returns: The server's serialized response. If the server does not respond after 5 timeouts and reattempts,
                returns an empty byte string.
        """

        # Initialize a time out counter to 0
        time_outs = 0;

        # If time outs ever reaches 5, give up attempt
        while time_outs < 5:

            # Extra print msg if time out did occur
            if time_outs > 0:
                print(f"GS STATUS: {time_outs} timeout(s) encountered. Re-attempting to send...");

            # Serialize the request and send to satellite
            serialized_request = in_request.SerializeToString();
            self.gs_socket.sendto(serialized_request, self.satellite_addr);
            print(f"GS STATUS: Request (ID {in_request.sat_id}) sent to satellite. "
                  f"Waiting for response...", end = "");

            # Wait for response. If no reply received and timeout occurred,
            # increment time_outs and re-attempt to send message. If response received, return it serialized
            try:
                sat_reply = self.gs_socket.recv(RECV_BUFFER_SIZE);
                print(" Received.");
                return sat_reply;
            except TimeoutError:
                print(" Timed out.");
                time_outs += 1;
                continue;

        # If this code is reached, means satellite never responded. Return an empty byte string if so.
        return b'';


    def display_response(self, serialized_response, request_type):
        """ Method displays the satellite's response according to what the request type of the sent request was.

        Args:
            <serialized_response : string of bytes> : The raw serialized response from the satellite server.
            <request_type : RequestType enum constant> : The enumerated request type of the request that
                was sent to the satellite. This is used to figure out which type of response was sent to the
                ground station (LocationResponse, TimeResponse, MoveResponse).
        """

        # Determine what satellite's response type is depending on the type of request it was sent
        if request_type == RequestType.LOCA:

            # Parse the serialized response into LocationResponse
            loca_resp = satellite_pb2.SatelliteResponse.LocationResponse();
            loca_resp.ParseFromString(serialized_response);

            # Print reply results
            print(f"\nSATELLITE REPLY: Latitude = {loca_resp.latitude}, Longitude = {loca_resp.longitude}.");


        elif request_type == RequestType.TIME:

            # Parse the serialized response into TimeResponse
            time_resp = satellite_pb2.SatelliteResponse.TimeResponse();
            time_resp.ParseFromString(serialized_response);

            # Print reply results
            print(f"\nSATELLITE REPLY: Current satellite time is {self.unix_to_curr(time_resp.curr_time)}.");


        elif request_type == RequestType.MOVE:

            # Parse the serialized response into MoveResponse
            move_resp = satellite_pb2.SatelliteResponse.MoveResponse();
            move_resp.ParseFromString(serialized_response);

            # Print reply results accordingly (response code = 0 means move request failed.
            # response code = 1 means move request succeeded - display updated location).
            if move_resp.resp_code:
                print(f"\nSATELLITE REPLY: Satellite successfully moved. \nNew Position: \n{move_resp.updated_loca}");
            else:
                print(f"\nSATELLITE REPLY: Move request unsuccessful - satellite failed to move.");


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







