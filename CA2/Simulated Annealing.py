from Imports import *

# ******************************************************************************************************************** #
def schedule(t, k=20, lam=0.005, limit=100):
    if t < limit:
        return k * math.exp(-lam * t)
    else:
        return 0
# ******************************************************************************************************************** #
def probability(p):
    return p > random.uniform(0.0, 1.0)
# ******************************************************************************************************************** #
class Agent:
    def __init__(self, size, initial_state, limit):
        self.problem = Problem(size)
        self.initial_state = initial_state
        self.MAX = limit
        self.size = size
        self.list = self.problem.actions()

    def SA(self):
        states = []
        current = self.initial_state
        for t in range(sys.maxsize):
            states.append(current)

            if schedule(t=t, k=20, lam=0.005, limit=self.MAX) == 0:
                return states

            neighbors = []
            for l in list:
                neighbors.append(self.child_node(current, l))

            if not neighbors:
                return False

            delta_e = -1 * (self.problem.goal_test(random.choice(neighbors)) - self.problem.goal_test(current))
            print(delta_e, self.problem.goal_test(random.choice(neighbors)), self.problem.goal_test(current))

            if delta_e > 0 or probability(math.exp(delta_e / schedule(t=t, k=20, lam=0.005, limit=self.MAX))):
                current = random.choice(neighbors)

    def child_node(self, square, action):
        [(x, y), (x2, y2)] = action
        child = np.array(square)
        child[x][y], child[x2][y2] = child[x2][y2], child[x][y]
        return child.tolist()
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

    def goal_test(self, square):
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
        return self.action_list
# ******************************************************************************************************************** #
if __name__ == "__main__":
    fields = []

    for size, square in fileToList("a.in"):
        fields.append((size, square))

    agent = Agent(fields[0][0], fields[0][1], 1000)
    tick = datetime.now()
    result = agent.SA()
    tack = datetime.now()
    pprint(result)

    print(tack - tick)

    with open('SimulatedAnnealing.out', 'w') as f:
        f.write('out=' + str(result[-1]) + ', t=' + str(tack - tick))