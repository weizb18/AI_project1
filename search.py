from block import *
from board import *
from utils import *

# bfs_with_limit(board, limit), bfs_without_limit(board) and bfs_without_limit_prior_connect(board)
# can deal with the cases that board have blocks
def bfs_with_limit(board, limit):
    open = Queue()
    closed = set()
    for i in range(board.m):
        for j in range(board.n):
            if board.block_posi_list[i][j] != 0 and board.block_posi_list[i][j] != -1:
                different_spot_brother = board.generate_brother()
                different_spot_brother.spot = [i, j]
                different_spot_brother.spot_init_posi = [i, j]
                open.push(different_spot_brother)
    pop_board = board
    while open.empty() == False:
        pop_board = open.pop()
        pop_board_tuple = tuple(tuple([pop_board.block_posi_list[i][j] for j in range(pop_board.n)]) for i in range(pop_board.m)) + tuple(pop_board.spot)
        # print("pop")
        # print(pop_board_tuple)
        closed.add(pop_board_tuple)
        for child_board in pop_board.available_child_board_limit(limit):
            child_board_tuple = tuple(tuple([child_board.block_posi_list[i][j] for j in range(child_board.n)]) for i in range(child_board.m)) + tuple(child_board.spot)
            if open.find_mat_spot(child_board.block_posi_list, child_board.spot) == False and (child_board_tuple not in closed):
                clean_flag = 0                        # clean sheet (all 0 or -1)
                for _ in range(child_board.m):
                    for __ in range(child_board.n):
                        if child_board.block_posi_list[_][__] != 0 and child_board.block_posi_list[_][__] != -1:
                            clean_flag = clean_flag + 1
                if clean_flag == 0:
                    return child_board
                open.push(child_board)
                # print("push")
                # print(child_board_tuple)
    while pop_board.block_posi_list[pop_board.spot_init_posi[0]][pop_board.spot_init_posi[1]] != pop_board.block_posi_list[pop_board.spot[0]][pop_board.spot[1]]:
        pop_board = pop_board.parent
    return pop_board


def bfs_without_limit(board):
    open = Queue()
    closed = set()
    for i in range(board.m):
        for j in range(board.n):
            if board.block_posi_list[i][j] != 0 and board.block_posi_list[i][j] != -1:
                different_spot_brother = board.generate_brother()
                different_spot_brother.spot = [i, j]
                different_spot_brother.spot_init_posi = [i, j]
                open.push(different_spot_brother)
    pop_board = board
    while open.empty() == False:
        pop_board = open.pop()
        pop_board_tuple = tuple(tuple([pop_board.block_posi_list[i][j] for j in range(pop_board.n)]) for i in range(pop_board.m)) + tuple(pop_board.spot)
        # print("pop")
        # print(pop_board_tuple)
        closed.add(pop_board_tuple)
        for child_board in pop_board.available_child_board():
            child_board_tuple = tuple(tuple([child_board.block_posi_list[i][j] for j in range(child_board.n)]) for i in range(child_board.m)) + tuple(child_board.spot)
            if open.find_mat_spot(child_board.block_posi_list, child_board.spot) == False and (child_board_tuple not in closed):
                clean_flag = 0                        # clean sheet (all 0 or -1)
                for _ in range(child_board.m):
                    for __ in range(child_board.n):
                        if child_board.block_posi_list[_][__] != 0 and child_board.block_posi_list[_][__] != -1:
                            clean_flag = clean_flag + 1
                if clean_flag == 0:
                    return child_board
                open.push(child_board)
                # print("push")
                # print(child_board_tuple)
    while pop_board.block_posi_list[pop_board.spot_init_posi[0]][pop_board.spot_init_posi[1]] != pop_board.block_posi_list[pop_board.spot[0]][pop_board.spot[1]]:
        pop_board = pop_board.parent
    return pop_board


def bfs_without_limit_prior_connect(board):
    open = Queue()
    closed = set()
    board.simple_connect()
    for i in range(board.m):
        for j in range(board.n):
            if board.block_posi_list[i][j] != 0 and board.block_posi_list[i][j] != -1:
                different_spot_brother = board.generate_brother()
                different_spot_brother.spot = [i, j]
                different_spot_brother.spot_init_posi = [i, j]
                open.push(different_spot_brother)
    pop_board = board
    while open.empty() == False:
        pop_board = open.pop()
        pop_board_tuple = tuple(tuple([pop_board.block_posi_list[i][j] for j in range(pop_board.n)]) for i in range(pop_board.m)) + tuple(pop_board.spot)
        # print("pop")
        # print(pop_board_tuple)
        closed.add(pop_board_tuple)
        for child_board in pop_board.available_child_board_prior_connect():
            child_board_tuple = tuple(tuple([child_board.block_posi_list[i][j] for j in range(child_board.n)]) for i in range(child_board.m)) + tuple(child_board.spot)
            if open.find_mat_spot(child_board.block_posi_list, child_board.spot) == False and (child_board_tuple not in closed):
                clean_flag = 0                        # clean sheet (all 0 or -1)
                for _ in range(child_board.m):
                    for __ in range(child_board.n):
                        if child_board.block_posi_list[_][__] != 0 and child_board.block_posi_list[_][__] != -1:
                            clean_flag = clean_flag + 1
                if clean_flag == 0:
                    return child_board
                open.push(child_board)
                # print("push")
                # print(child_board_tuple)
    while pop_board.block_posi_list[pop_board.spot_init_posi[0]][pop_board.spot_init_posi[1]] != pop_board.block_posi_list[pop_board.spot[0]][pop_board.spot[1]]:
        pop_board = pop_board.parent
    return pop_board


def bfs_with_limit_prior_connect(board, limit):
    open = Queue()
    closed = set()
    board.simple_connect()
    for i in range(board.m):
        for j in range(board.n):
            if board.block_posi_list[i][j] != 0 and board.block_posi_list[i][j] != -1:
                different_spot_brother = board.generate_brother()
                different_spot_brother.spot = [i, j]
                different_spot_brother.spot_init_posi = [i, j]
                open.push(different_spot_brother)
    pop_board = board
    while open.empty() == False:
        pop_board = open.pop()
        pop_board_tuple = tuple(tuple([pop_board.block_posi_list[i][j] for j in range(pop_board.n)]) for i in range(pop_board.m)) + tuple(pop_board.spot)
        # print("pop")
        # print(pop_board_tuple)
        closed.add(pop_board_tuple)
        for child_board in pop_board.available_child_board_limit_prior_connect(limit):
            child_board_tuple = tuple(tuple([child_board.block_posi_list[i][j] for j in range(child_board.n)]) for i in range(child_board.m)) + tuple(child_board.spot)
            if open.find_mat_spot(child_board.block_posi_list, child_board.spot) == False and (child_board_tuple not in closed):
                clean_flag = 0                        # clean sheet (all 0 or -1)
                for _ in range(child_board.m):
                    for __ in range(child_board.n):
                        if child_board.block_posi_list[_][__] != 0 and child_board.block_posi_list[_][__] != -1:
                            clean_flag = clean_flag + 1
                if clean_flag == 0:
                    return child_board
                open.push(child_board)
                # print("push")
                # print(child_board_tuple)
    while pop_board.block_posi_list[pop_board.spot_init_posi[0]][pop_board.spot_init_posi[1]] != pop_board.block_posi_list[pop_board.spot[0]][pop_board.spot[1]]:
        pop_board = pop_board.parent
    return pop_board
    # return [pop_board, simple_stack]