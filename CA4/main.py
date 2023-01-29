

check = []
number_domain = []
op = []
nine_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

number_domain = [number_domain.append(nine_numbers) for i in range(44)]
check = [check.append(True) for i in range(20)]
index = 0

line = open("input.in", "r").read().splitlines()

for i in range(0, len(line[0], 1)):
    op = [line[0][i:i+1]]

number = line[1].split(',')

for i in range(len(number)):
    if number[i] != '_':
        number_domain[i] = []
########################################################################################################################
def finish(number):
    for i in range(0, len(number)):
        if number[i] == '_':
            return False
    return True
########################################################################################################################
def check(A, B, op, y):
    if A != '_' and B != '_':
        if (len(y) == 2 and y[0] != '_' and y[1] != '_') or (y[0] != '_' and len(y) == 1):
            A = int(A)
            b = int(B)
            y = int(y)
            if op == '+':
                if y != A + B:
                    return False
            elif op == '*':
                if y != A * B:
                    return False
            elif op == '-':
                if y != A - B:
                    return False
        else:
            return True
    else:
        return True
########################################################################################################################
def constraint(number, op, check):
    check[0] = check(number[0], number[1], op[0], number[2])
    check[1] = check(number[3], number[4], op[1], number[5])
    check[2] = check(number[7], number[8], op[6], number[9])
    check[3] = check(number[15], number[16], op[7], number[17])
    check[4] = check(number[18], number[19], op[8], number[20])
    check[5] = check(number[23], number[24], op[11], number[25])
    check[6] = check(number[26], number[27], op[12], number[28])
    check[7] = check(number[30], number[31], op[17], number[32])
    check[8] = check(number[38], number[39], op[18], number[40])
    check[9] = check(number[41], number[42], op[19], number[43])
    check[10] = check(number[16], number[21], op[9], number[24])
    check[11] = check(number[19], number[22], op[10], number[27])
    check[12] = check(number[0], number[6], op[2], number[11] + number[15])
    check[13] = check(number[2], number[7], op[3], number[12] + number[17])
    check[14] = check(number[3], number[9], op[4], number[13] + number[18])
    check[15] = check(number[5], number[10], op[5], number[14] + number[20])
    check[16] = check(number[23], number[29], op[13], number[34] + number[38])
    check[17] = check(number[25], number[30], op[14], number[35] + number[40])
    check[18] = check(number[26], number[32], op[15], number[36] + number[41])
    check[19] = check(number[28], number[33], op[16], number[37] + number[43])

    for i in range(0, len(check)):
        if check[i] is False:
            return False
    return True
########################################################################################################################
def main(number, number_domain, op, index, check):
    if not constraint(number, op, check):
        return False
    if finish(number):
        print("Puzzle Solved... ")
        print('Answer:')
        f = open("Output.out", "w")
        for i in range(44):
            f.write(number[i])
            f.write(", ")
        print(number)
        return True
    else:
        for x in range(len(number)):
            if number[x] == '_':
                index = x
                break
        possibilities = number_domain[index]
        for z in range(len(possibilities)):
            number[index] = possibilities[z]
            if main(number, number_domain, op, index, check):
                return
        number[index] = '_'
########################################################################################################################
if __name__ == "__main__":
    main(number, number_domain, op, index, check)


