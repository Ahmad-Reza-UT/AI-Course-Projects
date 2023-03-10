from Imports import *

# ******************************************************************************************************************** #
class Agent:
    def __init__(self, size, initial_state):
        self.problem = Problem(size)
        self.initial_state = initial_state
        self.MAX = 100

    def IDS(self):
        for depth in range(0, self.MAX):
            print("Depth", depth)
            result = self.DLS(depth)

            if result != "cutoff":
                return result

    def DLS(self, limit):
        return self.recursiveDLS(self.initial_state, limit)

    def recursiveDLS(self, square, limit):
        if self.problem.goalTest(square):
            return square
        elif limit == 0:
            return "cutoff"
        else:
            cutoff = False
            actions = self.problem.actions()
            for action in actions:
                child = self.childNode(square, action)
                result = self.recursiveDLS(child, limit - 1)
                if result == "cutoff":
                    cutoff = True
                elif result != False:
                    return result
            return "cutoff" if cutoff else False

    def childNode(self, square, action):
        [(x, y), (x2, y2)] = action
        square[x][y], square[x2][y2] = square[x2][y2], square[x][y]
        return square
# ******************************************************************************************************************** #
class Problem:
    def __init__(self, size):
        self.size = size
        self.magic_number = size * (size ** 2 + 1) / 2

        action_list = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i == self.size - 1:
                    if j != self.size - 1:
                        action_list.append([(i, j), (i, j + 1)])
                elif j == self.size - 1:
                    if i != self.size - 1:
                        action_list.append([(i, j), (i + 1, j)])
                else:
                    action_list.append([(i, j), (i, j + 1)])
                    action_list.append([(i, j), (i + 1, j)])
        self.action_list = action_list

    def goalTest(self, square):
        test_list = [0] * (2 * self.size + 2)
        for i in range(0, self.size):
            for j in range(0, self.size):
                test_list[i] += square[i][j]
                test_list[j + self.size] += square[i][j]
                if i == j:
                    test_list[-2] += square[i][j]
                if j == self.size - i - 1:
                    test_list[-1] += square[i][j]

        for i in test_list:
            if i != self.magic_number:
                return False
        return True

    def actions(self):
        return self.action_list
# ******************************************************************************************************************** #
if __name__ == "__main__":
    fields = []

    for size, square in fileToList("a.in"):
        fields.append((size, square))

    agent = Agent(fields[0][0], fields[0][1])
    print(fields[0][0], fields[0][1])

    tick = datetime.now()
    result = agent.IDS()
    tack = datetime.now()
    pprint(result)

    print(tack - tick)

    with open('IDS.out', 'w') as f:
        f.write('out=' + str(result) + ', t=' + str(tack - tick))