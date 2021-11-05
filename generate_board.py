from block import *
from board import *
import copy
import random

def generate_assign_board(block_posi_list):    # input a matrix of pattern, return a Board
    m = len(block_posi_list)
    n = len(block_posi_list[0])
    pattern_type = set()
    pattern_num = 0
    for i in range(m):
        for j in range(n):
            temp_pattern = block_posi_list[i][j]
            if(temp_pattern != 0):
                pattern_type.add(temp_pattern)
                pattern_num = pattern_num + 1
    assign_board = Board(m, n, pattern_num, len(pattern_type))
    assign_board.block_posi_list = copy.deepcopy(block_posi_list)
    for i in range(m):
        for j in range(n):
            assign_board.block_mat[i][j].pattern = block_posi_list[i][j]
    for i in range(m*n):
        if block_posi_list[i//n][i%n] != 0 and block_posi_list[i//n][i%n] != -1:
            assign_board.spot = [i//n, i%n]
            assign_board.spot_init_posi = [i//n, i%n]
            break
    return assign_board

def generate_random_board(m, n, k, p):    # generate a random board with m*n size, 2*k blocks, p types of pattern
    random_board = Board(m, n, k, p)
    position_list = []
    cnt = 0
    while(len(position_list) < 2*k):    # generate positions of 2*k blocks
        posi = random.randint(0, m*n-1)
        if posi not in position_list:
            position_list.append(posi)
    while(cnt < 2*k):
        rand_pattern = random.randint(1, p)    # pattern = 0 means empty
        block_row = position_list[cnt] // n
        block_col = position_list[cnt] % n
        block1 = Block(block_row, block_col, rand_pattern)
        random_board.block_posi_list[block_row][block_col] = rand_pattern
        random_board.block_mat[block_row][block_col].pattern = rand_pattern
        cnt = cnt + 1
        block_row = position_list[cnt] // n
        block_col = position_list[cnt] % n
        block2 = Block(block_row, block_col, rand_pattern)
        random_board.block_posi_list[block_row][block_col] = rand_pattern
        random_board.block_mat[block_row][block_col].pattern = rand_pattern
        cnt = cnt + 1
    random_board.spot = [position_list[0]//n, position_list[0]%n]
    random_board.spot_init_posi = copy.deepcopy(random_board.spot)
    return random_board

def generate_random_board_blocks(m, n, k, p):    # generate a random board with m*n size, 2*k blocks, p types of pattern, and random number of obstacles
    random_board = Board(m, n, k, p)
    position_list = []
    cnt = 0
    while(len(position_list) < 2*k):    # generate positions of 2*k blocks
        posi = random.randint(0, m*n-1)
        if posi not in position_list:
            position_list.append(posi)
    while(cnt < 2*k):
        rand_pattern = random.randint(1, p)    # pattern = 0 means empty
        block_row = position_list[cnt] // n
        block_col = position_list[cnt] % n
        block1 = Block(block_row, block_col, rand_pattern)
        random_board.block_posi_list[block_row][block_col] = rand_pattern
        random_board.block_mat[block_row][block_col].pattern = rand_pattern
        cnt = cnt + 1
        block_row = position_list[cnt] // n
        block_col = position_list[cnt] % n
        block2 = Block(block_row, block_col, rand_pattern)
        random_board.block_posi_list[block_row][block_col] = rand_pattern
        random_board.block_mat[block_row][block_col].pattern = rand_pattern
        cnt = cnt + 1
    random_board.spot = [position_list[0]//n, position_list[0]%n]
    random_board.spot_init_posi = copy.deepcopy(random_board.spot)

    rest = m*n-2*k
    rest_list = []
    obstacles_list = []
    if rest > 0:
        if rest != 1:
            rest = rest // 2
        block_num = random.randint(1, rest)
        for i in range(m*n):
            if i not in position_list:
                rest_list.append(i)
        while block_num != 0:
            block_num = block_num - 1
            obstacle_position = rest_list[random.randint(0, len(rest_list)-1)]
            obstacles_list.append(obstacle_position)
            rest_list.remove(obstacle_position)
        for i in range(len(obstacles_list)):
            random_board.block_posi_list[obstacles_list[i] // n][obstacles_list[i] % n] = -1
            random_board.block_mat[obstacles_list[i] // n][obstacles_list[i] % n].pattern = -1
    if random_board.block_posi_list[1][0] == -1 and random_board.block_posi_list[0][1] == -1:
        random_board.block_posi_list[1][0] = 0
        random_board.block_mat[1][0].pattern = 0
    if random_board.block_posi_list[1][n-1] == -1 and random_board.block_posi_list[0][n-2] == -1:
        random_board.block_posi_list[1][n-1] = 0
        random_board.block_mat[1][n-1].pattern = 0
    if random_board.block_posi_list[m-2][0] == -1 and random_board.block_posi_list[m-1][1] == -1:
        random_board.block_posi_list[m-2][0] = 0
        random_board.block_mat[m-2][0].pattern = 0
    if random_board.block_posi_list[m-2][n-1] == -1 and random_board.block_posi_list[m-1][n-2] == -1:
        random_board.block_posi_list[m-2][n-1] = 0
        random_board.block_mat[m-2][n-1] = 0

    return random_board
