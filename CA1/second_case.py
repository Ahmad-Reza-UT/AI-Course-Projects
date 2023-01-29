import numpy as np
from random import randint


# Getting the initial coordination from the user
def get_initial_location():
    i, j = input('Initial Coordination (with an space between, start: 0, end: 9): ').split(' ')
    i = int(i)
    j = int(j)
    while i > 10 or j > 10:
        i, j = input('Please enter valid coordination: ').split(' ')
        i = int(i)
        j = int(j)
    return i, j


# Reading the file of environment and store it into a numpy array
def import_environment(which_file: int = 1):
    file = open('environment/map{}.txt'.format(which_file))
    enviro = []
    length_of_file = len(file.read())
    current_pointer = 0
    file.seek(0)
    while length_of_file > current_pointer:
        enviro.append([int(x) for x in file.readline().split(' ')])
        current_pointer = file.tell()
    return np.array(enviro)


# Function of sensor: Returns (i, j, D) where D shows whether the (i, j) is dirty or not.
def sensor(which_neighbor='self'):
    if which_neighbor == 'self':
        return i_loc, j_loc, environment[i_loc, j_loc]
    elif which_neighbor == 'top' and i_loc != 0:
        return i_loc - 1, j_loc, environment[i_loc - 1, j_loc]
    elif which_neighbor == 'button' and i_loc != 9:
        return i_loc + 1, j_loc, environment[i_loc + 1, j_loc]
    elif which_neighbor == 'left' and j_loc != 0:
        return i_loc, j_loc - 1, environment[i_loc, j_loc - 1]
    elif which_neighbor == 'right' and j_loc != 9:
        return i_loc, j_loc + 1, environment[i_loc, j_loc + 1]
    else:
        return False  # in case of being at the edge of environment, and we cannot move further


def left():
    global j_loc
    if j_loc > 0:
        j_loc -= 1


def right():
    global j_loc
    if j_loc < 9:
        j_loc += 1


def top():
    global i_loc
    if i_loc > 0:
        i_loc -= 1


def button():
    global i_loc
    if i_loc < 9:
        i_loc += 1


def suck():
    global environment
    environment[i_loc, j_loc] = 1


# Print action, sensor perception, and environment
def print_environment_and_location(action='No Operation'):
    print('Action:', action)
    print('Sensor Perception:', sensor())
    print('Environment:')
    print(environment, '\n')


# Agent function: The agent function works as follows:
# 1) It checks whether the current room and all adjacent rooms are dirty or not,
# 2) If the current room is dirty, it sucks,
# 3) If any one of the adjacent rooms is dirty, it first moves then sucks,
# 4) After doing suck, it does the first step again,
# 5) If the current room and all adjacent rooms are not dirty, we then randomly select another room and move there
#    and do the same thing again until all rooms become clean.
def neighbor_aware_agent_function():
    repeat = 0
    while True:
        while (
                (sensor('self') and sensor('self')[2] == 0) or
                (sensor('top') and sensor('top')[2] == 0) or
                (sensor('button') and sensor('button')[2] == 0) or
                (sensor('left') and sensor('left')[2] == 0) or
                (sensor('right') and sensor('right')[2] == 0)
        ):
            repeat += 1
            if sensor('self')[2] == 0:
                pass
            elif sensor('top') and sensor('top')[2] == 0:
                top()
                print_environment_and_location('Top')
            elif sensor('button') and sensor('button')[2] == 0:
                button()
                print_environment_and_location('Button')
            elif sensor('left') and sensor('left')[2] == 0:
                left()
                print_environment_and_location('Left')
            elif sensor('right') and sensor('right')[2] == 0:
                right()
                print_environment_and_location('Right')
            suck()
            print_environment_and_location('Suck')
        if not (is_there_dirty_room()):
            break
        else:
            rand_i = randint(0, 9)
            rand_j = randint(0, 9)
            should_move_right = rand_j - sensor()[1] > 0
            latitude_move = abs(rand_j - sensor()[1])
            should_move_button = rand_i - sensor()[0] > 0
            altitude_move = abs(rand_i - sensor()[0])
            for j in range(latitude_move):
                repeat += 1
                if should_move_right:
                    right()
                    print_environment_and_location('Right')
                    if sensor()[2] == 0:
                        suck()
                        print_environment_and_location('Suck')
                        repeat += 1
                else:
                    left()
                    print_environment_and_location('Left')
                    if sensor()[2] == 0:
                        suck()
                        print_environment_and_location('Suck')
                        repeat += 1
            for j in range(altitude_move):
                repeat += 1
                if should_move_button:
                    button()
                    print_environment_and_location('Button')
                    if sensor()[2] == 0:
                        suck()
                        print_environment_and_location('Suck')
                        repeat += 1
                else:
                    top()
                    print_environment_and_location('Top')
                    if sensor()[2] == 0:
                        suck()
                        print_environment_and_location('Suck')
                        repeat += 1
    print('Number of actions:', repeat)
    return repeat


def is_there_dirty_room():
    for i in range(10):
        for j in range(10):
            if environment[i, j] == 0:
                return True
    return False


# Execution Part:
environment = import_environment()
i_loc, j_loc = get_initial_location()
print('First, Sensor Perception:', sensor())
print(environment, '\n')
neighbor_aware_agent_function()


def give_avg_and_std_of_result(agent_function, iteration: int):
    global environment, i_loc, j_loc
    number_of_actions = []
    for i in range(iteration):
        number_of_actions.append(agent_function())
        environment = import_environment(randint(1, 4))
        i_loc = randint(0, 9)
        j_loc = randint(0, 9)
    number_of_actions = np.array(number_of_actions)
    return np.average(number_of_actions), number_of_actions.std()


# print(give_avg_and_std_of_result(neighbor_aware_agent_function, 10))
