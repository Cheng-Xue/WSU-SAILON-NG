import random
import numpy as np


class Agents:

    def __init__(self, novelty, difficulty, mock):
        self.novelty = novelty
        self.difficulty = difficulty
        self.mock = mock

        return None

    # Run agent behavoir here
    def act(self, state):
        # Enemies move towards player
        if self.novelty == 3:
            commands = self.move_towards(state)

        # Enemies move away from avg
        elif self.novelty == 5:
            commands = self.spread_out(state)

        else:
            commands = []
            # Random behavoiur:
            for i in range(4):
                action = random.choice(list(range(7))) + 1
                commands.append("set ai_" + str(i) + " " + str(action))

        # Enemies always check for facing to see if shoot
        commands = self.check_shoot(state, commands)

        return commands

    # Move agent towards player
    def move_towards(self, state):
        commands = []
        for ind, val in enumerate(state['enemies']):

            # Get info
            angle = self.get_angle(state['player'], val)

            # If enemy is face towards player turn away
            if np.pi * 3 / 16 < angle and np.pi * 13 / 16 > angle:
                if angle > np.pi / 2:
                    # Turn left
                    action = 6
                else:
                    # Turn right
                    action = 5

            else:
                # Forward, left, right, shoot?
                action = random.choice([1, 3, 4, 7])

            # Send ai action
            commands.append("set ai_" + str(ind) + " " + str(action))

        return commands

    def spread_out(self, state):
        commands = []
        # Find avg pos
        avg_x = 0.0
        avg_y = 0.0
        for ind, val in enumerate(state['enemies']):
            avg_x = avg_x + val['x_position']
            avg_y = avg_y + val['y_position']

        avg_x = avg_x / len(state['enemies'])
        avg_y = avg_y / len(state['enemies'])

        # Do spread out logic
        for ind, val in enumerate(state['enemies']):
            # Get info
            pl = {'x_position': avg_x, 'y_position': avg_y}

            angle = self.get_angle(pl, val)

            # If enemy is face towards player turn away
            if np.pi * 3 / 16 < angle and np.pi * 13 / 16 > angle:
                if angle > np.pi / 2:
                    # Turn right
                    action = 5
                else:
                    # Turn left
                    action = 6

            else:
                # Forward, left, right
                action = random.choice([1, 3, 4])

            # Send ai action
            commands.append("set ai_" + str(ind) + " " + str(action))

        return commands

    def check_shoot(self, state, commands):
        for ind, val in enumerate(state['enemies']):
            angle = self.get_angle(state['player'], val)

            if np.pi * 3 / 16 < angle and np.pi * 13 / 16 > angle:
                if np.random.rand() > 0.5:
                    # Shoot is action = 7
                    commands[ind] = "set ai_" + str(ind) + " " + str(7)

        return commands

    def get_angle(self, player, enemy):
        pl_x = player['x_position']
        pl_y = player['y_position']

        en_x = enemy['x_position']
        en_y = enemy['y_position']
        en_ori = enemy['angle']

        # Get angle between player and enemy
        # Convert enemy ori to unit vector
        v1_x = np.cos(en_ori)
        v1_y = np.sin(en_ori)

        enemy_vector = np.asarray([v1_x, v1_y]) / np.linalg.norm(np.asarray([v1_x, v1_y]))

        if np.linalg.norm(np.asarray([pl_x - en_x, pl_y - en_y])) == 0:
            return np.random.rand() * 3.14

        enemy_face_vector = np.asarray([pl_x - en_x, pl_y - en_y]) / np.linalg.norm(
            np.asarray([pl_x - en_x, pl_y - en_y]))

        angle = np.arccos(np.dot(enemy_vector, enemy_face_vector))
        return angle