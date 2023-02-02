from Imports import *

# ******************************************************************************************************************** #
class Node:
    def __init__(self, square, fitness):
        self.square = square
        self.fitness = fitness

    def __repr__(self):
        return str(self.square) + " " + str(self.fitness)

    def __str__(self):
        return str(self.square) + " " + str(self.fitness)

    def getSquare(self):
        return self.square

    def getFitness(self):
        return self.fitness

# ******************************************************************************************************************** #
class Agent:
    def __init__(self, w, popnum, ngen):
        self.problem = Problem(w)
        self.w = w
        self.popnum = popnum
        self.ngen = ngen
        self.all = [j for j in range(1, self.w ** 2 + 1)]

    def GA(self):
        population = self.init()
        for i in range(self.ngen):
            new_population = []
            for j in range(self.popnum):
                x = random.choice(population[:int(self.popnum / 2)])
                y = random.choice(population[:int(self.popnum / 2)])
                c = self.reproduce(x.getSquare(), y.getSquare())
                if probability(0.8):
                    c = self.mutate(c)
                fit = self.problem.fitness(c)
                if fit == 0:
                    return Node(c, fit)
                else:
                    fit = 1 / fit
                new_population.append(Node(c, fit))
            population = new_population
            population.sort(key=lambda x: x.fitness, reverse=True)
        return population[0]

    def init(self):
        q = int(self.w)
        base = [[i + j for i in range(1, q + 1)] for j in range(0, q ** 2, q)]
        base = np.array(base)
        shape = base.shape
        base = base.flatten()
        population = []
        for j in range(self.popnum):
            c = base.reshape(shape).tolist()
            fit = self.problem.fitness(c)
            if fit == 0:
                return c
            else:
                fit = 1 / fit
            population.append(Node(c, fit))

            np.random.shuffle(base)
        return population

    def reproduce(self, x, y):
        helper = self.all[:]

        x = np.array(x)
        y = np.array(y)

        shape = x.shape

        x = x.flatten()
        y = y.flatten()

        mid = random.randint(0, x.size - 1)

        for item in x[:mid]:
            helper.remove(item)
        for item in y[mid:]:
            try:
                helper.remove(item)
            except:
                pass

        temp = []
        for i in range(mid, len(y)):
            if y[i] in x[:mid]:
                temp.append(helper[0])
                helper.remove(helper[0])
            else:
                temp.append(y[i])

        c = np.concatenate([x[:mid], temp]).astype(int)
        c = c.reshape(shape)

        return c.tolist()

    def mutate(self, c):
        c = np.array(c)
        shape = c.shape

        c = c.flatten()

        i = random.randint(0, c.size - 1)
        j = random.randint(0, c.size - 1)

        c[i], c[j] = c[j], c[i]
        c = c.reshape(shape)

        return c.tolist()

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

    def fitness(self, square):
        test_list = [0] * (2 * self.size + 2)
        for i in range(0, self.size):
            for j in range(0, self.size):
                test_list[i] += square[i][j]
                test_list[j + self.size] += square[i][j]
                if i == j:
                    test_list[-2] += square[i][j]
                if j == self.size - i - 1:
                    test_list[-1] += square[i][j]
        return sum([abs(i - self.magic_number) for i in test_list])


# ******************************************************************************************************************** #
def probability(p):
    return p < random.uniform(0.0, 1.0)
# ******************************************************************************************************************** #
def exp_schedule(t, k=20, lam=0.005, limit=100):
    if t < limit:
        return k * math.exp(-lam * t)
    else:
        return 0
# ******************************************************************************************************************** #
def Convert_f2L(filename: str):
    with open(filename) as file:
        lines = file.read().splitlines()

        for line in lines:
            size = int(line[2:4])

            s = str(line).find('[')
            f = str(line).find(']') + 1
            l = line[s:f]
            l = json.loads(l)
            l = np.array(l).reshape(size, size)

            yield size, l.tolist()
# ******************************************************************************************************************** #
def goalTest(square):
    test_list = [0] * (2 * 3 + 2)
    for i in range(3):
        for j in range(3):
            test_list[i] += square[i][j]
            test_list[j + 3] += square[i][j]
            if i == j:
                test_list[-2] += square[i][j]
            if j == 3 - i - 1:
                test_list[-1] += square[i][j]
    return sum([abs(i - 15) for i in test_list])
# ******************************************************************************************************************** #
def mgoalTest(square):
    test_list = [0] * (2 * 3 + 2)
    for i in range(3):
        for j in range(3):
            test_list[i] += square[i][j]
            test_list[j + 3] += square[i][j]
            if i == j:
                test_list[-2] += square[i][j]
            if j == 3 - i - 1:
                test_list[-1] += square[i][j]

    return test_list
# ******************************************************************************************************************** #
if __name__ == "__main__":
    fields = list()
    for size, square in Convert_f2L("a.in"):
        fields.append((size, square))

    agent = Agent(fields[0][0], 100, 50)
    tick = datetime.now()
    result = agent.GA()
    print(goalTest(result.square))
    print(mgoalTest(result.square))

    tack = datetime.now()
    pprint(result)
    print(tack - tick)
    with open('genetic.out', 'w') as f:
        f.write('out=' + str(result) + ', t=' + str(tack - tick))