from imports import *
import directions

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


# Execution part:
i_loc, j_loc = get_initial_location()


# Function of sensor: Returns (i, j, D) where D shows whether the (i, j) is dirty or not.
def sensor(i, j):
    return i, j, environment[i, j]





def suck():
    global environment
    environment[i_loc, j_loc] = 1


# Print action, sensor perception, and environment
def print_environment_and_location(action='No Operation'):
    print('Action:', action)
    print('Sensor Perception:', sensor(i_loc, j_loc))
    print('Environment:')
    print(environment, '\n')


# Agent function:
def full_aware_agent_function():
    global i_loc, j_loc
    repeat = 0
    if sensor(i_loc, j_loc)[2] == 0:
        suck()
        print_environment_and_location('Suck')
        repeat += 1
    for i in range(10):
        for j in range(10):
            if sensor(i, j)[2] == 0:
                should_move_right = j - sensor(i_loc, j_loc)[1] > 0
                latitude_move = abs(j - sensor(i_loc, j_loc)[1])
                should_move_button = i - sensor(i_loc, j_loc)[0] > 0
                altitude_move = abs(i - sensor(i_loc, j_loc)[0])
                for k in range(latitude_move):
                    repeat += 1
                    if should_move_right:
                        directions.right()
                        print_environment_and_location('Right')
                        if sensor(i_loc, j_loc)[2] == 0:
                            suck()
                            print_environment_and_location('Suck')
                            repeat += 1
                    else:
                        print(i_loc, j_loc)
                        directions.left()
                        print(i_loc, j_loc)
                        print_environment_and_location('Left')
                        if sensor(i_loc, j_loc)[2] == 0:
                            suck()
                            print_environment_and_location('Suck')
                            repeat += 1
                for k in range(altitude_move):
                    repeat += 1
                    if should_move_button:
                        directions.button()
                        print_environment_and_location('Button')
                        if sensor(i_loc, j_loc)[2] == 0:
                            suck()
                            print_environment_and_location('Suck')
                            repeat += 1
                    else:
                        directioons.top()
                        print_environment_and_location('Top')
                        if sensor(i_loc, j_loc)[2] == 0:
                            suck()
                            print_environment_and_location('Suck')
                            repeat += 1
                suck()
                print('Sensor Perception:', sensor(i_loc, j_loc), 'Sucked')
                print(environment, '\n')
                repeat += 1
    print('Number of actions:', repeat)
    return repeat


# Execution Part:
environment = import_environment()
print('First, Sensor Perception:', sensor(i_loc, j_loc))
print(environment, '\n')
full_aware_agent_function()


def give_avg_and_std_of_result(agent_function, iteration: int):
    global environment, i_loc, j_loc
    number_of_actions = []
    for i in range(iteration):
        number_of_actions.append(agent_function())
        environment = import_environment(randint(1, 4))
        i_loc , j_loc = randint(0, 9)
    number_of_actions = np.array(number_of_actions)
    return np.average(number_of_actions), number_of_actions.std()

# print(give_avg_and_std_of_result(full_aware_agent_function, 10))
