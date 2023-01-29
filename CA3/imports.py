import time
import pprint
from isolation import Board
from copy import deepcopy
from copy import copy
from random import *
from math import *
# -----------------------------------
#Attributes
TIME_LIMIT_MILLIS = 1000
MIN = -10000
MAX = 10000
DEPTH = 5
board, temp_board = [[]]
player1 = "X"
player2 = "O"
has_seen_sign = "*"
player_turn = player1

max_counter, min_counter = 1

SIZE = 8

player1_col = 0
player1_row = 0

player2_col = 7
player2_row = 7