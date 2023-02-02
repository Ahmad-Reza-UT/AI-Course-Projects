from Imports import *

# ******************************************************************************************************************** #
class Problem:
    def __init__(self, size):
        list = []

        self.size = size
        self.magic_number = size * (size ** 2 + 1) / 2


        for i in range(0, self.size):
            for j in range(0, self.size):
                if i == self.size - 1:
                    if j != self.size - 1:
                        list.append([(i, j), (i, j + 1)])
                elif j == self.size - 1:
                    if i != self.size - 1:
                        list.append([(i, j), (i + 1, j)])
                else:
                    list.append([(i, j), (i, j + 1)])
                    list.append([(i, j), (i + 1, j)])

        self.list = list

    def goal(self, square):
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
            return sum([abs(i - self.magic_number)])


    def actions(self):
        return self.list
# ******************************************************************************************************************** #
class Agent:
    def __init__(self, size, initial_state):
        self.problem = Problem(size)
        self.initial_state = initial_state
        self.magic_number = size * (size ** 2 + 1) / 2
        self.MAX = 100

    def IDA(self):
        for DEPTH in range(0, self.MAX):
            print("Depth", DEPTH)
            result = self.DLS(DEPTH)

            if result != "cutoff":
                return result

    def rec_DLS(self, square, limit):
        if self.problem.goal(square) == 0:
            return square
        elif limit == 0:
            return "cutoff"
        else:
            cutoff = False
            childs = self.h(self.problem.actions(), square)
            for child in childs:
                result = self.rec_DLS(child, limit - 1)
                if result == "cutoff":
                    cutoff = True
                elif result != False:
                    return result

            if cutoff:
                return "cutoff"
            else :
                return False


    def DLS(self, limit):
        return self.rec_DLS(self.initial_state, limit)


    def child_node(self, square, action):
        [(x, y), (x2, y2)] = action
        square[x][y], square[x2][y2] = square[x2][y2], square[x][y]
        return square

    def h(self, actions, square):
        childs = []
        for action in actions:
            child = self.child_node(square, action)
            child = np.array(child)
            r = self.problem.goal(child)
            childs.append((np.copy(child).tolist(), r))

        childs.sort(key=lambda x: x[1])

        for c in childs:
            return [c[0]]

# ******************************************************************************************************************** #
if __name__ == "__main__":
    fields = []

    for size, square in fileToList("a.in"):
        fields.append((size, square))

    agent = Agent(fields[0][0], fields[0][1])
    print(fields[0][0], fields[0][1])

    tick = datetime.now()
    result = agent.IDA()
    tack = datetime.now()
    pprint(result)

    print(tack - tick)

    with open('IDA.out', 'w') as f:
        f.write('out=' + str(result) + ', t=' + str(tack - tick))