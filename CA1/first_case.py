from imports import *
import directions


def get_initial_location():
    i, j = input('Initial Coordination (with an space between, start: 0, end: 9): ').split(' ')
    i, j = int(i), int(j)
    while i > 10 or j > 10:
        i, j = input('Please enter valid coordination: ').split(' ')
        i, j = int(i), int(j)
    return i, j


#
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



def sensor():
    return i_loc, j_loc, environment[i_loc, j_loc]



def suck():
    global environment
    environment[i_loc, j_loc] = 1



def print_environment_and_location(action='No Operation'):
    print('Action:', action)
    print('Sensor Perception:', sensor())
    print('Environment:')
    print(environment, '\n')



def regular_agent_function():
    repeat = 0
    if sensor()[2] == 0:
        suck()
        print_environment_and_location(action='Suck')
        repeat += 1
    for y in range(sensor()[1] - 1, -1, -1):
        directions.left()
        print_environment_and_location(action='Left')
        repeat += 1
    for x in range(sensor()[0] - 1, -1, -1):
        directions.top()
        print_environment_and_location(action='Top')
        repeat += 1
    for x in range(10):
        if x != 0:
            directions.button()
        if x % 2 == 0:
            for y in range(10):
                if y != 0:
                    directions.right()
                print_environment_and_location('Right')
                repeat += 1
                if sensor()[2] == 0:
                    suck()
                    print_environment_and_location('Suck')
                    repeat += 1
        else:
            for y in range(9, -1, -1):
                if y != 9:
                    directions.left()
                print_environment_and_location('Left')
                repeat += 1
                if sensor()[2] == 0:
                    suck()
                    print_environment_and_location('Suck')
                    repeat += 1
    print('Number of actions:', repeat)
    return repeat



def random_agent_function():
    repeat = 0
    while is_there_dirty_room():
        rand_i = randint(0, 9)
        rand_j = randint(0, 9)
        should_move_right = rand_j - sensor()[1] > 0
        latitude_move = abs(rand_j - sensor()[1])
        should_move_button = rand_i - sensor()[0] > 0
        altitude_move = abs(rand_i - sensor()[0])
        for j in range(latitude_move):
            repeat += 1
            if should_move_right:
                directions.right()
                print_environment_and_location('Right')
            else:
                directions.left()
                print_environment_and_location('Left')
        for j in range(altitude_move):
            repeat += 1
            if should_move_button:
                directions.button()
                print_environment_and_location('Button')
            else:
                directions.top()
                print_environment_and_location('Top')
        if sensor()[2] == 0:
            suck()
            print_environment_and_location('Suck')
        else:
            print_environment_and_location()
    print('Number of actions:', repeat)
    return repeat



def random_agent_function_2():
    repeat = 0
    while is_there_dirty_room():
        rand_i = randint(0, 9)
        rand_j = randint(0, 9)
        should_move_right = rand_j - sensor()[1] > 0
        latitude_move = abs(rand_j - sensor()[1])
        should_move_button = rand_i - sensor()[0] > 0
        altitude_move = abs(rand_i - sensor()[0])
        for j in range(latitude_move):
            repeat += 1
            if should_move_right:
                directions.right()
                print_environment_and_location('Right')
                if sensor()[2] == 0:
                    suck()
                    print_environment_and_location('Suck')
                    repeat += 1
            else:
                directions.left()
                print_environment_and_location('Left')
                if sensor()[2] == 0:
                    suck()
                    print_environment_and_location('Suck')
                    repeat += 1
        for j in range(altitude_move):
            repeat += 1
            if should_move_button:
                directions.button()
                print_environment_and_location('Button')
                if sensor()[2] == 0:
                    suck()
                    print_environment_and_location('Suck')
                    repeat += 1
            else:
                directions.top()
                print_environment_and_location('Top')
                if sensor()[2] == 0:
                    suck()
                    print_environment_and_location('Suck')
                    repeat += 1
        if sensor()[2] == 0:
            suck()
            print_environment_and_location('Suck')
            repeat += 1
        else:
            print_environment_and_location()
    print('Number of actions:', repeat)
    return repeat


def is_there_dirty_room():
    for i in range(10):
        for j in range(10):
            if environment[i, j] == 0:
                return True
    return False





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



if __name__ == "__main__": 
    env = import_environment()
    i_loc, j_loc = get_initial_location()
    print('First, Sensor Perception:', sensor())
    print(env, '\n')
    regular_agent_function()

