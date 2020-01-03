"""

"""

import tkinter as tk
import numpy as np


class ArrayGui:

    def __init__(self, height, width, num_obstacles):
        self.height = height
        self.width = width
        self.num_obstacles = num_obstacles
        self.grid = None
        self.robot_position = None
        self.obstacle_positions = None
        self.goal_position = None
        self.robot_orientation = None
        self.historical_data = []
        self.historical_actions = []

    def make_board(self):
        """"""
        board = []
        for r in range(self.height):
            holder = []
            for c in range(self.width):
                holder.append('.')
            board.append(holder)

        self.grid = np.array(board)



    def place_robot(self):
        """"""
        robot_position = []
        robot_position.append(np.random.choice(self.width))
        robot_position.append(np.random.choice(self.height))
        self.robot_position = robot_position
        self.grid[robot_position[0], robot_position[1]] = 'R'
        self.robot_orientation = 'north'

    def place_obstacles(self, num_obstacles):
        """"""
        obstacles = []

        for _ in range(num_obstacles):
            on_robot = True

            while on_robot:
                holder = []
                holder.append(np.random.choice(self.width))
                holder.append(np.random.choice(self.height))
                if not holder == self.robot_position:
                    obstacles.append(holder)
                    on_robot = False

        for ob in obstacles:
            self.grid[ob[0], ob[1]] = 'O'

        self.obstacle_positions = obstacles

    def place_goal(self):
        """"""
        invalid = True

        while invalid:
            holder = []
            holder.append(np.random.choice(self.width))
            holder.append(np.random.choice(self.height))

            if not holder == self.robot_position:
                if len([x for x in self.obstacle_positions if x == holder]) == 0:
                    invalid = False

        self.grid[holder[0], holder[1]] = 'G'
        self.goal_position = holder

    def random_lidar(self, dist_category):
        """
        Spaces away
        1: [10, 25]
        2: [26, 60]
        3: [61, 130]
        4: [131, 400]

        Args:
            dist_category:

        Returns:

        """

        if dist_category == 1:
            return np.random.randint(10, 25)
        if dist_category == 2:
            return np.random.randint(26, 60)
        if dist_category == 3:
            return np.random.randint(61, 130)
        if dist_category == 4:
            return np.random.randint(131, 400)

    def lidar_left(self):
        """"""

        spots_looked = 1
        obstacle_found = False

        while not obstacle_found:
            if spots_looked == 4:
                # If we are here in the logic flow, we have looked four spots to the left and found nothing
                # Therefore our sensor should max out!
                left_sensor_data = 400
                obstacle_found = True

            if self.robot_position[1] - spots_looked < 0:
                # If we are here in the logic flow, we have hit a wall
                left_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # If we are here in the logic flow, we have neither reached the max number of spots scanned
            # NOR have we hit a wall
            spot_looking = [self.robot_position[0], self.robot_position[1] - spots_looked]

            if spot_looking in self.obstacle_positions:
                # If here, then there is an obstacle in our current scanned spot!
                left_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # Incrementing as none of the above have returned anything
            spots_looked += 1

        return left_sensor_data

    def lidar_right(self):
        """"""

        spots_looked = 1
        obstacle_found = False

        while not obstacle_found:
            if spots_looked == 4:
                # If we are here in the logic flow, we have looked four spots to the right and found nothing
                # Therefore our sensor should max out!
                right_sensor_data = 400
                obstacle_found = True

            if self.robot_position[1] + spots_looked >= self.width:
                # If we are here in the logic flow, we have hit a wall
                right_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # If we are here in the logic flow, we have neither reached the max number of spots scanned
            # NOR have we hit a wall
            spot_looking = [self.robot_position[0], self.robot_position[1] + spots_looked]

            if spot_looking in self.obstacle_positions:
                # If here, then there is an obstacle in our current scanned spot!
                right_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # Incrementing as none of the above have returned anything
            spots_looked += 1

        return right_sensor_data

    def lidar_up(self):
        """"""

        spots_looked = 1
        obstacle_found = False

        while not obstacle_found:
            if spots_looked ==4 :
                # If we are here in the logic flow, we have looked four spots to the right and found nothing
                # Therefore our sensor should max out!
                up_sensor_data = 400
                obstacle_found = True

            if self.robot_position[0] - spots_looked < 0:
                # If we are here in the logic flow, we have hit a wall
                up_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # If we are here in the logic flow, we have neither reached the max number of spots scanned
            # NOR have we hit a wall
            spot_looking = [self.robot_position[0] - spots_looked, self.robot_position[1]]

            if spot_looking in self.obstacle_positions:
                # If here, then there is an obstacle in our current scanned spot!
                up_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # Incrementing as none of the above have returned anything
            spots_looked += 1

        return up_sensor_data

    def lidar_down(self):
        """"""

        spots_looked = 1
        obstacle_found = False

        while not obstacle_found:
            if spots_looked == 4:
                # If we are here in the logic flow, we have looked four spots to the right and found nothing
                # Therefore our sensor should max out!
                down_sensor_data = 400
                obstacle_found = True

            if self.robot_position[0] + spots_looked >= self.height:
                # If we are here in the logic flow, we have hit a wall
                down_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # If we are here in the logic flow, we have neither reached the max number of spots scanned
            # NOR have we hit a wall
            spot_looking = [self.robot_position[0] + spots_looked, self.robot_position[1]]

            if spot_looking in self.obstacle_positions:
                # If here, then there is an obstacle in our current scanned spot!
                down_sensor_data = self.random_lidar(dist_category=spots_looked)
                obstacle_found = True

            # Incrementing as none of the above have returned anything
            spots_looked += 1

        return down_sensor_data


    def read_lidar(self):
        """
        The scanning should work by looking, at most 4 places in each direction until either an obstacle or
        wall is hit!

        Left/Right deal with column changes
        Up/Down deal with row changes

        The purpose of this method is to handle routing to the proper lidar reading methods based on the robot's
        current orientation



        Returns:

        """
        data = {
            'agent_gps': self.robot_position,
            'goal_gps': self.goal_position,
            'left_lidar': None,
            'right_lidar': None,
            'forward_lidar': None,
            'backward_lidar': None
        }

        if self.robot_orientation == 'north':
            data['left_lidar'] = self.lidar_left()
            data['right_lidar'] = self.lidar_right()
            data['forward_lidar'] = self.lidar_up()
            data['backward_lidar'] = self.lidar_down()

        if self.robot_orientation == 'south':
            data['left_lidar'] = self.lidar_right()
            data['right_lidar'] = self.lidar_left()
            data['forward_lidar'] = self.lidar_down()
            data['backward_lidar'] = self.lidar_up()

        if self.robot_orientation == 'east':
            data['left_lidar'] = self.lidar_down()
            data['right_lidar'] = self.lidar_up()
            data['forward_lidar'] = self.lidar_left()
            data['backward_lidar'] = self.lidar_right()

        if self.robot_orientation == 'west':
            data['left_lidar'] = self.lidar_up()
            data['right_lidar'] = self.lidar_down()
            data['forward_lidar'] = self.lidar_right()
            data['backward_lidar'] = self.lidar_left()

        return data

    def move_robot(self, action):
        """

        Args:
            action: ['w', 'a', 's', 'd']

        Returns:

        """

        if self.robot_orientation == 'north':
            if action == 'w':
                self.robot_position = [self.robot_position[0]-1, self.robot_position[1]]
                return self
            if action == 'a':
                self.robot_orientation = 'west'
                return self
            if action == 's':
                self.robot_position = [self.robot_position[0]+1, self.robot_position[1]]
                return self
            if action == 'd':
                self.robot_orientation = 'east'
                return self

        if self.robot_orientation == 'south':
            if action == 'w':
                self.robot_position = [self.robot_position[0]+1, self.robot_position[1]]
                return self
            if action == 'a':
                self.robot_orientation = 'east'
                return self
            if action == 's':
                self.robot_position = [self.robot_position[0]-1, self.robot_position[1]]
                return self
            if action == 'd':
                self.robot_orientation = 'west'
                return self

        if self.robot_orientation == 'east':
            if action == 'w':
                self.robot_position = [self.robot_position[0], self.robot_position[1]+1]
                return self
            if action == 'a':
                self.robot_orientation = 'north'
                return self
            if action == 's':
                self.robot_position = [self.robot_position[0], self.robot_position[1]-1]
                return self
            if action == 'd':
                self.robot_orientation = 'south'
                return self

        if self.robot_orientation == 'west':
            if action == 'w':
                self.robot_position = [self.robot_position[0], self.robot_position[1]-1]
                return self
            if action == 'a':
                self.robot_orientation = 'south'
                return self
            if action == 's':
                self.robot_position = [self.robot_position[0], self.robot_position[1]+1]
                return self
            if action == 'd':
                self.robot_orientation = 'north'
                return self

    def redraw_grid(self):
        """"""
        # Redrawing the base board in the same way as the .make_board() method
        board = []
        for r in range(self.height):
            holder = []
            for c in range(self.width):
                holder.append('.')
            board.append(holder)

        self.grid = np.array(board)

        # Placing in the obstacles
        for ob in self.obstacle_positions:
            self.grid[ob[0], ob[1]] = 'O'

        # Placing the robot
        self.grid[self.robot_position[0], self.robot_position[1]] = 'R'

        # Placing the goal
        self.grid[self.goal_position[0], self.goal_position[1]] = 'G'

    def collision_check(self):
        """To be called after the robot moves and before the grid is redrawn..."""

        # (0) Checking to see if robot has hit an obstacle
        if len([x for x in self.obstacle_positions if x == self.robot_position]) > 0:
            return True

        # (1) Checking to see if robot has hit a wall
        if self.robot_position[0] < 0:
            return True
        if self.robot_position[0] >= self.height:
            return True
        if self.robot_position[1] < 0:
            return True
        if self.robot_position[1] >= self.width:
            return True

        return False


    def go(self):
        """"""

        # (0) Making the board and placing all of the pieces...
        self.make_board()
        self.place_robot()
        self.place_obstacles(num_obstacles=self.num_obstacles)
        self.place_goal()

        # (1) Printing the grid and the robot orientation for the player
        print(self.grid)
        print(f'Robot facing: {self.robot_orientation}')

        # (2) Recording the data
        self.historical_data.append(self.read_lidar())

        # Quick condition check injection...
        collided = False

        # (3) The main loop of the game which is:
        # Do until either robot hits goal OR robot hits wall/obstacle
        # (a) Collection action
        # (b) Record action
        # (c) Update robot position
        # (d) Read sensors
        # (e) Record sensor data
        while not self.robot_position == self.goal_position:
            action = input('Move?')
            self.historical_actions.append(action)
            self.move_robot(action=action)
            if self.collision_check():
                collided = True
                self.robot_position = self.goal_position

            self.redraw_grid()
            self.historical_data.append(self.read_lidar())

            print(self.grid)
            print(f'Robot facing: {self.robot_orientation}')

        # If here, we have either won the game or died...
        if collided:
            print('You died.')
        else:
            print('You won!')





a = ArrayGui(height=15, width=15, num_obstacles=40)
a.go()


