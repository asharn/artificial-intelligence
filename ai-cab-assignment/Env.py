# Import routines

import numpy as np
import math
import random

# Defining hyperparameters
m = 5 # number of cities, ranges from 1 ..... m
t = 24 # number of hours, ranges from 0 .... t-1
d = 7  # number of days, ranges from 0 ... d-1
C = 5 # Per hour fuel and other costs
R = 9 # per hour revenue from a passenger


class CabDriver():

    def __init__(self):
        """initialise your state and define your action space and state space"""
        ## action space is possible combinations of pick up and drop cities
        self.action_space = [(0,0)]+[(x, y) for x in range(m) for y in range(m) if x != y]
       # State space is possible combination of 
        self.state_space = [[x, y, z] for x in range(m) for y in range(t) for z in range(d)]
        self.state_init = random.choice(self.state_space)

        # Start the first round
        self.reset()


    ## Encoding state (or state-action) for NN input

    def state_encod_arch1(self, state):
        """convert the state into a vector so that it can be fed to the NN. This method converts a given state into a vector format. Hint: The vector is of size m + t + d."""
        ## state is - [m,t,d] where m is citi, t is time and d is day
        state_encod = [0 for _ in range(m+t+d)]
        state_encod[state[0]] = 1 # setting citi to 1
        state_encod[m+state[1]] = 1 # setting time to 1
        state_encod[m+t+state[2]] = 1 # setting day to 1

        return state_encod


    # Use this function if you are using architecture-2 
    # def state_encod_arch2(self, state, action):
    #     """convert the (state-action) into a vector so that it can be fed to the NN. This method converts a given state-action pair into a vector format. Hint: The vector is of size m + t + d + m + m."""

        
    #     return state_encod


    ## Getting number of requests

    def requests(self, state):
        """Determining the number of requests basis the location. 
        Use the table specified in the MDP and complete for rest of the locations"""
        location = state[0]
        if location == 0: # location A gets 2 requests
            requests = np.random.poisson(2) # gettting poison distribution
        if location == 1: # location B gets 12 requests
            requests = np.random.poisson(12) # gettting poison distribution
        if location == 2: # location C gets 4 requests
            requests = np.random.poisson(4) # gettting poison distribution
        if location == 3: # location D gets 7 requests
            requests = np.random.poisson(7) # gettting poison distribution
        if location == 4: # location E gets 8 requests
            requests = np.random.poisson(8) # gettting poison distribution
        if requests >15:
            requests =15

        possible_actions_index = random.sample(range(1, (m-1)*m +1), requests)+[0] # (0,0) is not considered as customer request
        actions = [self.action_space[i] for i in possible_actions_index]        
        return possible_actions_index,actions   



    def reward_func(self, wait_time, transit_time, ride_time):        
        # question during wait time car is turned off? of so battery cost should not be considered
        # else include batterry cost for waittime. I am including wait time and panalising at the rate
        # C as not other rate defined
        reward = (R * ride_time) - (C * (wait_time + transit_time + ride_time))        
        return reward

    def next_state_func(self, state, action, Time_matrix):
        """Takes state and action as input and returns next state"""
        next_state = []
        
        # Initialize various times
        total_time   = 0
        transit_time = 0    # to go from current  location to pickup location
        wait_time    = 0    # in case driver chooses to refuse all requests
        ride_time    = 0    # from Pick-up to drop
        
        # find out current location, current time and current time
        curr_loc = state[0] # get current location x from the state s= (x,t,d)
        pickup_loc = action[0] # get pickup location from action (p,q)
        drop_loc =  action[1] # get drop location from action (p,q)
        curr_time = state[1] # get current time t from the state s= (x,t,d)
        curr_day = state[2] # get current day d from the state s= (x,t,d)
        
        # there are three posibilities for next state
        # 1. Go offline - action(0,0) setting pickup and drop to 0
        """the driver always has the option to go ‘offline’ (accept no ride). The noride action just moves the time component by 1 hour"""
        # 2. Pick up location is same as your current location. So no transition time and no wait time
        # 3. Pickup and current location is different. Need to find transition time and drop off time
        
        if ((pickup_loc== 0) and (drop_loc == 0)):            
            wait_time = 1
            next_loc = curr_loc
        elif (curr_loc == pickup_loc):
            # means driver is already at pickup point, wait and transit are both 0 then.
            wait_time =0
            transit_time = 0
            # get ride time from time matrix which is a 4D matrix (pickup, dropoff, time, day)
            ride_time = Time_matrix[curr_loc][drop_loc][curr_time][curr_day]
            
            # set drop location as the next location
            next_loc = drop_loc
        else:            
            # find ride time to reach the pick up location from timematrix
            transit_time = Time_matrix[curr_loc][pickup_loc][curr_time][curr_day]
            
            #find new time and day
            updated_time, updated_day = self.calculate_new_time(curr_time, curr_day, transit_time)
            
            #calculate drop off time
            ride_time = Time_matrix[pickup_loc][drop_loc][updated_time][updated_day]
            next_loc  = drop_loc

        # Calculate total time as sum of all durations
        total_time = (wait_time + transit_time + ride_time)
        
        next_time, next_day = self.calculate_new_time(curr_time, curr_day, total_time)
        
        # set next state (x,t,d)
        next_state = [next_loc, next_time, next_day]
        
        return next_state, wait_time, transit_time, ride_time
    
    def calculate_new_time(self, curr_time, curr_day, ride_time):
        ride_time = int(ride_time)
        
        if (curr_time + ride_time) < 24: # rides are within a day
            curr_time = curr_time + ride_time            
        else: # rides are crossing a day            
            # format to 0-23 range
            curr_time = (curr_time + ride_time) % 24            
            # take integer division days
            days = (curr_time + ride_time) // 24            
            # format to 0-6 range
            curr_day = (curr_day + days ) % 7

        return curr_time, curr_day
    
    # defininf step function
    def step(self, state, action, Time_matrix):        
        
        # get next state
        next_state, wait_time, transit_time, ride_time = self.next_state_func(
            state, action, Time_matrix)

        # calculate  reward
        reward = self.reward_func(wait_time, transit_time, ride_time)
        total_time = wait_time + transit_time + ride_time
        
        # set the basis for next step
        return reward, next_state, total_time

    def reset(self):
        return self.action_space, self.state_space, self.state_init
