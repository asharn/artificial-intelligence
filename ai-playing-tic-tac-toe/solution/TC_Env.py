'''
The environment class for the Tic-Tac-Toe problem. Provides methods for initialising a state,
checking whether the state is terminal or not,
computing new states and rewards given state and action etc.
'''


from gym import spaces
import numpy as np
import csv
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum"""
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for line in lines:
            if not np.isnan(curr_state[line[0]]) and not np.isnan(curr_state[line[1]]) and not np.isnan(curr_state[line[2]]):
                line_state = curr_state[line[0]] + curr_state[line[1]] + curr_state[line[2]]
                if line_state == 15:
                    return True
                else:
                    return False
            else:
                return False


    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'



    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)


    """This functions will be used only if environment is playing with the odd numbers, i.e., the environment has to make first move"""
    # def initial_step(self, curr_state):

    #     value = random.choice(self.allowed_values(curr_state)[0])
    #     position = random.choice([i for i in self.allowed_positions(curr_state)])

    #     curr_state[position] = value
    #     return curr_state


    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move."""

        position = curr_action[0]
        value = curr_action[1]

        curr_state[position] = value 

        return curr_state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state and reward. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status."""

        terminal_state = False
        temp_state = self.state_transition(curr_state, curr_action)


        terminal_state, game_status = self.is_terminal(temp_state)

        if terminal_state == True:
            if game_status == 'Win':
                reward=10
            else:
                reward=0

        else:
            position = random.choice(self.allowed_positions(temp_state))
            value = random.choice(self.allowed_values(temp_state)[1])

            temp_state[position]= value

            terminal_state, game_status = self.is_terminal(temp_state)


            if terminal_state == True:
                if game_status == 'Win':
                    reward=-10
                else:
                    reward=0
                    
            else:
                reward=-1

        return temp_state, reward, terminal_state




    def reset(self):
        return self.state
