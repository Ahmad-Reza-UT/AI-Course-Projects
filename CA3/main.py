from imports import *


def move(SIGN, ROW, COLUMN):
    global board
    board[ROW][COLUMN] = SIGN
########################################################################################################################
def fill_board():
    global board
    for i in range(0, SIZE):
        for j in range(0, SIZE):
            board[i][j] = "-"
    board[0][0] = player1
    board[SIZE - 1][SIZE - 1] = player2
########################################################################################################################
def is_valid(BOARD, ROW, COLUMN):
    if 0 <= ROW < SIZE and 0 <= COLUMN < SIZE:
        if BOARD[ROW][COLUMN] != player1 and BOARD[ROW][COLUMN] != player2 and BOARD[ROW][COLUMN] != has_seen_sign:
            return True

    return False
########################################################################################################################
def valid_index(BOARD, ROW, COLUMN):
    list = []

    if is_valid(BOARD, ROW - 2, COLUMN - 1):
        list.append((ROW - 2, COLUMN - 1))

    if is_valid(BOARD, ROW - 2, COLUMN + 1):
        list.append((ROW - 2, COLUMN + 1))

    if is_valid(BOARD, ROW - 1, COLUMN - 2):
        list.append((ROW - 1, COLUMN - 2))

    if is_valid(BOARD, ROW - 1, COLUMN + 2):
        list.append((ROW - 1, COLUMN + 2))

    if is_valid(BOARD, ROW + 1, COLUMN - 2):
        list.append((ROW + 1, COLUMN - 2))

    if is_valid(BOARD, ROW + 1, COLUMN + 2):
        list.append((ROW + 1, COLUMN + 2))

    if is_valid(BOARD, ROW + 2, COLUMN - 1):
        list.append((ROW + 2, COLUMN - 1))

    if is_valid(BOARD, ROW + 2, COLUMN + 1):
        list.append((ROW + 2, COLUMN + 1))

    return list
########################################################################################################################
def utility(player_row, player_col, opp_row, opp_col):
    global temp_board

    player_valid_index = valid_index(temp_board, player_row, player_col)
    oppo_valid_index = valid_index(temp_board, opp_row, opp_col)
    index = list(set(player_valid_index).intersection(oppo_valid_index))
    player_size = len(player_valid_index)
    oppo_size = len(oppo_valid_index)
    size = len(index)

    return player_size - oppo_size + size
########################################################################################################################
def minimax(player_row, player_col, opp_row, opp_col):
    global temp_board
    global player_turn

    pprint.pprint(board)
    temp_board = copy.deepcopy(board)
    valid_index_list = valid_index(board, player_row, player_col)
    best_value = MIN
    best_action = 0
    if len(valid_index_list) > 0:
        print("turn: " + player_turn)
        for action in valid_index_list:
            temp = find_min(action[0], action[1], opp_row, opp_col)
            print("action: " + str(action) + " value: " + str(temp))
            if temp > best_value:
                best_value = temp
                best_action = action
        board[action[0]][action[1]] = player_turn
        board[player_row][player_col] = has_seen_sign
        print("best: " + str(best_action) + " value: " + str(best_value))
        if player_turn == player1:
            player_turn = player2
        else:
            player_turn = player1
        minimax(opp_row, opp_col, action[0], action[1])
    else:
        print("loser: " + str(player_turn))
########################################################################################################################
def find_max(player_row, player_col, opp_row, opp_col):
    global max_counter
    global temp_board

    max_counter += 1
    if max_counter >= DEPTH:
        max_counter = 1
        return utility(player_row, player_col, opp_row, opp_col)
    v = MIN
    for action in valid_index(temp_board, player_row, player_col):
        temp_board[action[0]][action[1]] = has_seen_sign
        v = max(v, find_min(player_row, player_col, action[0], action[1]))

    return v
########################################################################################################################
def find_min(player_row, player_col, opp_row, opp_col):
    global min_counter
    global temp_board

    min_counter += 1
    if min_counter >= DEPTH:
        min_counter = 1
        return utility(player_row, player_col, opp_row, opp_col)
    v = MAX
    for action in valid_index(temp_board, player_row, player_col):
        temp_board[action[0]][action[1]] = has_seen_sign
        v = min(v, find_max(action[0], action[1], opp_row, opp_col))

    return v
########################################################################################################################
if __name__ == "__main__":

    pprint.pprint(board)
    fill_board()
    pprint.pprint(board)
    minimax(0, 0, 7, 7)
    print("final board: ")
    pprint.pprint(board)
