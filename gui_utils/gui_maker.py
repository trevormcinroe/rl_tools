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


    def go(self):
        self.make_board()
        self.place_robot()
        self.place_obstacles(num_obstacles=self.num_obstacles)
        self.place_goal()
        print(self.grid)



a = ArrayGui(height=15, width=15, num_obstacles=40)
a.go()

print(a.read_lidar())

# 1: [10, 25]
# # 2: [26, 60]
# # 3: [61, 130]
# # 4: [131, 400]