"""

Notes:
    1) Should the start always be bottom-left? Should this be adjustable by the user? And what about the terminal state?
"""

import pandas as pd
import numpy as np
import random
import math
from functools import reduce

class Gridworld:
    """

    """

    def __init__(self,
                 area,
                 seed=None,
                 grid_type='square',
                 obstacles=None):

        self.seed = seed
        self.area = area
        self.grid_type = grid_type
        self.height = None
        self.width = None
        self.obstacles = obstacles
        self.grid = None
        self.start = None
        self.terminal = None
        self.protected_spaces = None


    def _create(self):
        """"""

        if self.grid_type not in ['square', 'rectangle']:
            raise AttributeError('Given grid_type is not currently supported.')

        if self.obstacles not in [None, 'random']:
            if type(self.obstacles) is not int:
                raise AttributeError('Given obstacles is not currently supported.')


        # If no seed was passed by user, create it
        if not self.seed:
            self.seed = random.randint(0, 100000)

        ###############################
        # === BUILDING THE LAYOUT === #
        ###############################
        # Depending on the grid_type, we'll need to create some cool shapes
        # If square...
        if self.grid_type == 'square':

            # Find the sqrt of the area and round
            # Obvoiusly, the width and length will be the same
            self.length = round(math.sqrt(self.area))
            self.width = self.length

            # Building out the grid as an array full of 0s
            self.grid = np.zeros((self.height, self.width))

            # Starting and terminal states
            self._build_start_terminal()

        # How about a rectangle?
        if self.grid_type == 'rectangle':

            # Randomly produce some factor pairs
            factor_pair = np.random.choice(self._factor_pairs(n=self.area))

            # An explicit check to see if the given number if prime
            # If it is, give the user the choice of whether or not to proceed
            if len(factor_pair) == 0:

                choice = input('Given area is prime. This will create'
                               'a long, skinny rectangle. Proceed? (y/n)')

                if choice == 'y':

                    self.height = self.area
                    self.width = 1

                    # Building out the grid as an array full of 0s
                    self.grid = np.zeros((self.height, self.width))

                    # Starting and terminal states
                    self._build_start_terminal()

                else:

                    raise ValueError('Given area was prime.')

            # If it's not prime, assign...
            else:

                self.height = factor_pair[0]
                self.width = factor_pair[1]

                # Building out the grid as an array full of 0s
                self.grid = np.zeros((self.height, self.width))

                # Starting and terminal states
                self._build_start_terminal()

        ###############################
        # === BUILDING OBSTACLES  === #
        ###############################


    def _obstacles(self):
        """"""

        if self.obstacles == 'random':

            # What should the upper limit of obstacles be?
            # Need to ensure that there is a solvable path to the terminal
            num_obstacles = np.random.randint(1, 0.15*self.area)

            # Looping through and placing obstacles num_obstacles times
            i = 0

            while i < num_obstacles:

                obstacle_space = (np.random.randint(0, self.grid.shape[0]),
                                  np.random.randint(0, self.grid.shape[1]))

                # Need to make sure that the randomly generated coordinate is not protected
                if obstacle_space not in self.protected_spaces:

                    # Set a very low reward
                    self.grid[obstacle_space[0], obstacle_space[1]] = -100

                    # Increment
                    i += 1

                # If the randomly generated coordinate is protected, try again
                else:

                    continue

        if type(self.obstacles) is int:
            pass

    def _build_start_terminal(self):
        """"""

        # Now placing the start state and terminal state
        # Should the start always be bottom-left? Should this be adjustable by the user?
        # And what about the terminal state?
        # Terminal = (bottom_row, rightest_col)
        # Start = (bottom_row, first_col)
        self.start = (self.grid.shape[0], 0)
        self.terminal = (self.grid.shape[0], self.grid[1])

        # Now to set the "protected" spaces
        # This ensures that the agent can leave the start and also exit the grid
        self.protected_spaces = [
            (self.grid.shape[0]-1, 0), # space directly above the start
            (self.grid.shape[0], 1), # space directly right of the start
            (self.grid.shape[0], self.grid.shape[1]-1), # space directly left of the terminal
            (self.grid.shape[0]-1, self.grid.shape[1]), # space directly above the terminal
            self.start, # start, obv
            self.terminal # terminal, obv
        ]


    def _factor_pairs(self, n):
        """A helper function that will find factor pairs for a given number

        Args:
            n (int): a number

        Returns:
            a list of tuples of factor pairs
        """

        lst = []

        for i in range(int(math.sqrt(n))):

            if n % i == 0:
                lst.append((i, n / i))

        return lst
