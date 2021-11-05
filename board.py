from math import fabs, trunc
import random
import copy
from block import *
from utils import *

class Board():
    def __init__(self, m, n, k, p, parent = None):
        self.m = m    # rows of the board
        self.n = n    # cols of the board
        self.k = k    # number of blocks on the board: 2*k
        self.p = p    # types of blocks on the board: p
        self.parent = parent
        self.spot = []    # spot block position (the moving block) [row, col]
        self.spot_init_posi = []    # spot block initial position
        self.total_turns = 0

        self.block_posi_list = []
        row_vector = []
        for i in range(m):
            for j in range(n):
                row_vector.append(0)
            self.block_posi_list.append(row_vector)
            row_vector = []

        self.block_mat = []
        row_vector = []
        for i in range(m):
            for j in range(n):
                new_block = Block(i, j, 0)
                row_vector.append(new_block)
            self.block_mat.append(row_vector)
            row_vector = []
        
    def print_block_mat(self):
        for i in range(len(self.block_posi_list)):
            print(self.block_posi_list[i])

    def generate_child(self):            # generate a child board whose parent is self
        child_board = Board(self.m, self.n, self.k, self.p, self)
        for i in range(self.m):
            for j in range(self.n):
                child_board.block_posi_list[i][j] = self.block_posi_list[i][j]
                child_board.block_mat[i][j].pattern = self.block_mat[i][j].pattern
                child_board.block_mat[i][j].turn = self.block_mat[i][j].turn
                child_board.block_mat[i][j].direction = self.block_mat[i][j].direction
        child_board.spot_init_posi = copy.deepcopy(self.spot_init_posi)    # should not change spot_init_posi, and spot should be assigned (outside this function)
        child_board.total_turns = self.total_turns
        return child_board

    def generate_brother(self):            # same as self, but has different spot
        brother_board = Board(self.m, self.n, self.k, self.p, self.parent)
        for i in range(self.m):
            for j in range(self.n):
                brother_board.block_posi_list[i][j] = self.block_posi_list[i][j]
                brother_board.block_mat[i][j].pattern = self.block_mat[i][j].pattern
                brother_board.block_mat[i][j].turn = self.block_mat[i][j].turn
                brother_board.block_mat[i][j].direction = self.block_mat[i][j].direction
        brother_board.total_turns = self.total_turns
        return brother_board

    def available_row_range(self, row, obj_col):    # input: row is a vector, obj_col is the col of the obj
                                                    # return: available columns in a row
        start_col = 0
        end_col = obj_col + 1
        for cnt in range(obj_col):
            if row[cnt] != 0:
                start_col = cnt + 1
        for cnt in range(obj_col+1, len(row)):
            if row[cnt] == 0:
                end_col = cnt + 1
            else:
                end_col = cnt
                break
        col_list = list(range(start_col, end_col))
        col_list.remove(obj_col)
        return col_list
        
    def available_col_range(self, obj_row, obj_col):    # analogous to above function
        tranverse_row = []
        for cnt in range(len(self.block_posi_list)):
            tranverse_row.append(self.block_posi_list[cnt][obj_col])
        return self.available_row_range(tranverse_row, obj_row)

    def direct_connect(self, obj_row, obj_col):    # by direct connecting to generate child board, for assigned obj_row&obj_col
        child_board_list = []
        spot_pattern = self.block_posi_list[obj_row][obj_col]
        left_no_zero = -1
        right_no_zero = self.n
        up_no_zero = -1
        down_no_zero = self.m
        move_col = obj_col
        while move_col != 0:
            move_col = move_col - 1
            if self.block_posi_list[obj_row][move_col] != 0:
                left_no_zero = move_col
                break
        move_col = obj_col
        while move_col != self.n-1:
            move_col = move_col + 1
            if self.block_posi_list[obj_row][move_col] != 0:
                right_no_zero = move_col
                break
        move_row = obj_row
        while move_row != 0:
            move_row = move_row - 1
            if self.block_posi_list[move_row][obj_col] != 0:
                up_no_zero = move_row
                break
        move_row = obj_row
        while move_row != self.m-1:
            move_row = move_row + 1
            if self.block_posi_list[move_row][obj_col] != 0:
                down_no_zero = move_row
                break
        
        connect_direction = 0
        # left direct connect
        if left_no_zero != -1 and self.block_posi_list[obj_row][left_no_zero] == spot_pattern:
            connect_direction = 4
            left_connect_col = left_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][left_connect_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[obj_row][left_connect_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            child_board.block_mat[obj_row][left_connect_col].direction = connect_direction
            child_board.block_mat[obj_row][obj_col].direction = 0
            child_board.block_posi_list[obj_row][left_connect_col] = 0    # update board pattern matrix
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[obj_row][left_connect_col].pattern = 0
            child_board.block_mat[obj_row][obj_col].pattern = 0
            all_zero_flag = 0
            for i in range(child_board.m):
                for j in range(child_board.n):
                    if child_board.block_posi_list[i][j] != 0 and child_board.block_posi_list[i][j] != -1:
                        all_zero_flag = all_zero_flag + 1
                        different_spot_brother = child_board.generate_brother()
                        different_spot_brother.spot = [i, j]
                        different_spot_brother.spot_init_posi = [i, j]
                        child_board_list.append(different_spot_brother)
            if all_zero_flag == 0:
                child_board_list.append(child_board)    

        # right direct connect
        if right_no_zero != self.n and self.block_posi_list[obj_row][right_no_zero] == spot_pattern:
            connect_direction = 2
            right_connect_col = right_no_zero
            # print('-------%d-------' % right_connect_col)
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][right_connect_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[obj_row][right_connect_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            child_board.block_mat[obj_row][right_connect_col].direction = connect_direction
            child_board.block_mat[obj_row][obj_col].direction = 0
            child_board.block_posi_list[obj_row][right_connect_col] = 0    # update board pattern matrix
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[obj_row][right_connect_col].pattern = 0
            child_board.block_mat[obj_row][obj_col].pattern = 0
            all_zero_flag = 0
            for i in range(child_board.m):
                for j in range(child_board.n):
                    if child_board.block_posi_list[i][j] != 0 and child_board.block_posi_list[i][j] != -1:
                        all_zero_flag = all_zero_flag + 1
                        different_spot_brother = child_board.generate_brother()
                        different_spot_brother.spot = [i, j]
                        different_spot_brother.spot_init_posi = [i, j]
                        child_board_list.append(different_spot_brother)
            if all_zero_flag == 0:
                child_board_list.append(child_board) 

        # up direct connect
        if up_no_zero != -1 and self.block_posi_list[up_no_zero][obj_col] == spot_pattern:
            connect_direction = 1
            up_connect_row = up_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[up_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[up_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            child_board.block_mat[up_connect_row][obj_col].direction = connect_direction
            child_board.block_mat[obj_row][obj_col].direction = 0
            child_board.block_posi_list[up_connect_row][obj_col] = 0    # update board pattern matrix
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[up_connect_row][obj_col].pattern = 0
            child_board.block_mat[obj_row][obj_col].pattern = 0
            all_zero_flag = 0
            for i in range(child_board.m):
                for j in range(child_board.n):
                    if child_board.block_posi_list[i][j] != 0 and child_board.block_posi_list[i][j] != -1:
                        all_zero_flag = all_zero_flag + 1
                        different_spot_brother = child_board.generate_brother()
                        different_spot_brother.spot = [i, j]
                        different_spot_brother.spot_init_posi = [i, j]
                        child_board_list.append(different_spot_brother)
            if all_zero_flag == 0:
                child_board_list.append(child_board) 

        # down direct connect
        if down_no_zero != self.m and self.block_posi_list[down_no_zero][obj_col] == spot_pattern:
            connect_direction = 3
            down_connect_row = down_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[down_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[down_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            child_board.block_mat[down_connect_row][obj_col].direction = connect_direction
            child_board.block_mat[obj_row][obj_col].direction = 0
            child_board.block_posi_list[down_connect_row][obj_col] = 0    # update board pattern matrix
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[down_connect_row][obj_col].pattern = 0
            child_board.block_mat[obj_row][obj_col].pattern = 0
            all_zero_flag = 0
            for i in range(child_board.m):
                for j in range(child_board.n):
                    if child_board.block_posi_list[i][j] != 0 and child_board.block_posi_list[i][j] != -1:
                        all_zero_flag = all_zero_flag + 1
                        different_spot_brother = child_board.generate_brother()
                        different_spot_brother.spot = [i, j]
                        different_spot_brother.spot_init_posi = [i, j]
                        child_board_list.append(different_spot_brother)
            if all_zero_flag == 0:
                child_board_list.append(child_board)
        
        return child_board_list

    # only move to generate child board, not by connecting, and concatenate with child boards generated by connecting finally
    def available_child_board(self):
        obj_row = self.spot[0]
        obj_col = self.spot[1]
        child_board_list = []
        row_range = self.available_row_range(self.block_posi_list[obj_row], obj_col)
        col_range = self.available_col_range(obj_row, obj_col)
        parent_pattern = self.block_posi_list[obj_row][obj_col]

        for j in range(len(row_range)):
            child_board = self.generate_child()
            child_board.block_posi_list[obj_row][row_range[j]] = parent_pattern
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[obj_row][row_range[j]].pattern = parent_pattern
            child_board.block_mat[obj_row][obj_col].pattern = 0
            child_board.spot = [obj_row, row_range[j]]    # update new spot (from original posi to moved posi) ([obj_row,obj_col]->[obj_row,row_range[j]])
            if row_range[j] < obj_col:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][row_range[j]].direction = 4
            else:
                child_board.block_mat[obj_row][row_range[j]].direction = 2
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:
                child_board.block_mat[obj_row][row_range[j]].turn = child_board.block_mat[obj_row][row_range[j]].turn + 1
                child_board.total_turns = child_board.total_turns + 1
            child_board_list.append(child_board)

        for i in range(len(col_range)):
            child_board = self.generate_child()
            child_board.block_posi_list[col_range[i]][obj_col] = parent_pattern
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[col_range[i]][obj_col].pattern = parent_pattern
            child_board.block_mat[obj_row][obj_col].pattern = 0
            child_board.spot = [col_range[i], obj_col]
            if col_range[i] < obj_row:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[col_range[i]][obj_col].direction = 1
            else:
                child_board.block_mat[col_range[i]][obj_col].direction = 3
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:
                child_board.block_mat[col_range[i]][obj_col].turn = child_board.block_mat[col_range[i]][obj_col].turn + 1
                child_board.total_turns = child_board.total_turns + 1
            child_board_list.append(child_board)

        # child_board_list.extend(self.direct_connect(obj_row, obj_col))
        child_board_list_return = self.direct_connect(obj_row, obj_col)
        child_board_list_return.extend(child_board_list)

        return child_board_list_return

    # for more complex cases, we are expected to take a trade-off between the searching speed and the minimum total_turns
    # on the basis of function available_child_board(self), 
    # when the return of self.direct_connect(obj_row, obj_col) is not empty,
    # we will not compute other available child boards (child boards that only move, not connect)
    # this function is only used in unlimited cases, 
    # because limit cases can be quickly and precisely solved by function available_child_board_limit(self, limit)
    def available_child_board_prior_connect(self):
        obj_row = self.spot[0]
        obj_col = self.spot[1]
        direct_connect_return = self.direct_connect(obj_row, obj_col)
        if len(direct_connect_return) != 0:
            return direct_connect_return
        
        child_board_list = []
        row_range = self.available_row_range(self.block_posi_list[obj_row], obj_col)
        col_range = self.available_col_range(obj_row, obj_col)
        parent_pattern = self.block_posi_list[obj_row][obj_col]

        for j in range(len(row_range)):
            child_board = self.generate_child()
            child_board.block_posi_list[obj_row][row_range[j]] = parent_pattern
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[obj_row][row_range[j]].pattern = parent_pattern
            child_board.block_mat[obj_row][obj_col].pattern = 0
            child_board.spot = [obj_row, row_range[j]]    # update new spot (from original posi to moved posi) ([obj_row,obj_col]->[obj_row,row_range[j]])
            if row_range[j] < obj_col:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][row_range[j]].direction = 4
            else:
                child_board.block_mat[obj_row][row_range[j]].direction = 2
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:
                child_board.block_mat[obj_row][row_range[j]].turn = child_board.block_mat[obj_row][row_range[j]].turn + 1
                child_board.total_turns = child_board.total_turns + 1
            child_board_list.append(child_board)

        for i in range(len(col_range)):
            child_board = self.generate_child()
            child_board.block_posi_list[col_range[i]][obj_col] = parent_pattern
            child_board.block_posi_list[obj_row][obj_col] = 0
            child_board.block_mat[col_range[i]][obj_col].pattern = parent_pattern
            child_board.block_mat[obj_row][obj_col].pattern = 0
            child_board.spot = [col_range[i], obj_col]
            if col_range[i] < obj_row:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[col_range[i]][obj_col].direction = 1
            else:
                child_board.block_mat[col_range[i]][obj_col].direction = 3
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:
                child_board.block_mat[col_range[i]][obj_col].turn = child_board.block_mat[col_range[i]][obj_col].turn + 1
                child_board.total_turns = child_board.total_turns + 1
            child_board_list.append(child_board)

        return child_board_list

    
    ##########################
    # counterparts with LIMIT
    ##########################

    def direct_connect_limit(self, obj_row, obj_col, limit):    # by direct connecting to generate child board, for assigned obj_row&obj_col
        child_board_list = []
        spot_pattern = self.block_posi_list[obj_row][obj_col]
        left_no_zero = -1
        right_no_zero = self.n
        up_no_zero = -1
        down_no_zero = self.m
        move_col = obj_col
        while move_col != 0:
            move_col = move_col - 1
            if self.block_posi_list[obj_row][move_col] != 0:
                left_no_zero = move_col
                break
        move_col = obj_col
        while move_col != self.n-1:
            move_col = move_col + 1
            if self.block_posi_list[obj_row][move_col] != 0:
                right_no_zero = move_col
                break
        move_row = obj_row
        while move_row != 0:
            move_row = move_row - 1
            if self.block_posi_list[move_row][obj_col] != 0:
                up_no_zero = move_row
                break
        move_row = obj_row
        while move_row != self.m-1:
            move_row = move_row + 1
            if self.block_posi_list[move_row][obj_col] != 0:
                down_no_zero = move_row
                break
        
        connect_direction = 0
        # left direct connect
        if left_no_zero != -1 and self.block_posi_list[obj_row][left_no_zero] == spot_pattern:
            connect_direction = 4
            left_connect_col = left_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][left_connect_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[obj_row][left_connect_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            if child_board.block_mat[obj_row][left_connect_col].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_mat[obj_row][left_connect_col].direction = connect_direction
                child_board.block_mat[obj_row][obj_col].direction = 0
                child_board.block_posi_list[obj_row][left_connect_col] = 0    # update board pattern matrix
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[obj_row][left_connect_col].pattern = 0
                child_board.block_mat[obj_row][obj_col].pattern = 0
                all_zero_flag = 0
                for i in range(child_board.m):
                    for j in range(child_board.n):
                        if child_board.block_posi_list[i][j] != 0:
                            all_zero_flag = all_zero_flag + 1
                            different_spot_brother = child_board.generate_brother()
                            different_spot_brother.spot = [i, j]
                            different_spot_brother.spot_init_posi = [i, j]
                            child_board_list.append(different_spot_brother)
                if all_zero_flag == 0:
                    child_board_list.append(child_board)    

        # right direct connect
        if right_no_zero != self.n and self.block_posi_list[obj_row][right_no_zero] == spot_pattern:
            connect_direction = 2
            right_connect_col = right_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][right_connect_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[obj_row][right_connect_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            if child_board.block_mat[obj_row][right_connect_col].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_mat[obj_row][right_connect_col].direction = connect_direction
                child_board.block_mat[obj_row][obj_col].direction = 0
                child_board.block_posi_list[obj_row][right_connect_col] = 0    # update board pattern matrix
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[obj_row][right_connect_col].pattern = 0
                child_board.block_mat[obj_row][obj_col].pattern = 0
                all_zero_flag = 0
                for i in range(child_board.m):
                    for j in range(child_board.n):
                        if child_board.block_posi_list[i][j] != 0:
                            all_zero_flag = all_zero_flag + 1
                            different_spot_brother = child_board.generate_brother()
                            different_spot_brother.spot = [i, j]
                            different_spot_brother.spot_init_posi = [i, j]
                            child_board_list.append(different_spot_brother)
                if all_zero_flag == 0:
                    child_board_list.append(child_board) 

        # up direct connect
        if up_no_zero != -1 and self.block_posi_list[up_no_zero][obj_col] == spot_pattern:
            connect_direction = 1
            up_connect_row = up_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[up_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[up_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            if child_board.block_mat[up_connect_row][obj_col].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_mat[up_connect_row][obj_col].direction = connect_direction
                child_board.block_mat[obj_row][obj_col].direction = 0
                child_board.block_posi_list[up_connect_row][obj_col] = 0    # update board pattern matrix
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[up_connect_row][obj_col].pattern = 0
                child_board.block_mat[obj_row][obj_col].pattern = 0
                all_zero_flag = 0
                for i in range(child_board.m):
                    for j in range(child_board.n):
                        if child_board.block_posi_list[i][j] != 0:
                            all_zero_flag = all_zero_flag + 1
                            different_spot_brother = child_board.generate_brother()
                            different_spot_brother.spot = [i, j]
                            different_spot_brother.spot_init_posi = [i, j]
                            child_board_list.append(different_spot_brother)
                if all_zero_flag == 0:
                    child_board_list.append(child_board) 

        # down direct connect
        if down_no_zero != self.m and self.block_posi_list[down_no_zero][obj_col] == spot_pattern:
            connect_direction = 3
            down_connect_row = down_no_zero
            child_board = self.generate_child()
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:    # update block's direction and turn, and board's total_turns
                child_board.block_mat[down_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            else:
                child_board.block_mat[down_connect_row][obj_col].turn = self.block_mat[obj_row][obj_col].turn
                child_board.block_mat[obj_row][obj_col].turn = 0
            if child_board.block_mat[down_connect_row][obj_col].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_mat[down_connect_row][obj_col].direction = connect_direction
                child_board.block_mat[obj_row][obj_col].direction = 0
                child_board.block_posi_list[down_connect_row][obj_col] = 0    # update board pattern matrix
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[down_connect_row][obj_col].pattern = 0
                child_board.block_mat[obj_row][obj_col].pattern = 0
                all_zero_flag = 0
                for i in range(child_board.m):
                    for j in range(child_board.n):
                        if child_board.block_posi_list[i][j] != 0:
                            all_zero_flag = all_zero_flag + 1
                            different_spot_brother = child_board.generate_brother()
                            different_spot_brother.spot = [i, j]
                            different_spot_brother.spot_init_posi = [i, j]
                            child_board_list.append(different_spot_brother)
                if all_zero_flag == 0:
                    child_board_list.append(child_board)
        
        return child_board_list

    # only move to generate child board, not by connecting, and concatenate with child boards generated by connecting finally
    def available_child_board_limit(self, limit):
        obj_row = self.spot[0]
        obj_col = self.spot[1]
        child_board_list = []
        row_range = self.available_row_range(self.block_posi_list[obj_row], obj_col)
        col_range = self.available_col_range(obj_row, obj_col)
        parent_pattern = self.block_posi_list[obj_row][obj_col]

        for j in range(len(row_range)):    # available child board in the same row
            child_board = self.generate_child()
            child_board.spot = [obj_row, row_range[j]]    # update new spot (from original posi to moved posi) ([obj_row,obj_col]->[obj_row,row_range[j]])
            if row_range[j] < obj_col:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][row_range[j]].direction = 4
            else:
                child_board.block_mat[obj_row][row_range[j]].direction = 2
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:
                child_board.block_mat[obj_row][row_range[j]].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            if child_board.block_mat[obj_row][row_range[j]].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_posi_list[obj_row][row_range[j]] = parent_pattern
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[obj_row][row_range[j]].pattern = parent_pattern
                child_board.block_mat[obj_row][obj_col].pattern = 0
                child_board_list.append(child_board)

        for i in range(len(col_range)):
            child_board = self.generate_child()
            child_board.spot = [col_range[i], obj_col]    # update new spot (from original posi to moved posi) ([obj_row,obj_col]->[col_range[i], obj_col])
            if col_range[i] < obj_row:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[col_range[i]][obj_col].direction = 1
            else:
                child_board.block_mat[col_range[i]][obj_col].direction = 3
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:
                child_board.block_mat[col_range[i]][obj_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            if child_board.block_mat[col_range[i]][obj_col].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_posi_list[col_range[i]][obj_col] = parent_pattern
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[col_range[i]][obj_col].pattern = parent_pattern
                child_board.block_mat[obj_row][obj_col].pattern = 0
                child_board_list.append(child_board)

        child_board_list_return = self.direct_connect_limit(obj_row, obj_col, limit)
        child_board_list_return.extend(child_board_list)

        return child_board_list_return

    def available_child_board_limit_prior_connect(self, limit):
        obj_row = self.spot[0]
        obj_col = self.spot[1]
        direct_connect_return = self.direct_connect(obj_row, obj_col)
        if len(direct_connect_return) != 0:
            return direct_connect_return

        child_board_list = []
        row_range = self.available_row_range(self.block_posi_list[obj_row], obj_col)
        col_range = self.available_col_range(obj_row, obj_col)
        parent_pattern = self.block_posi_list[obj_row][obj_col]

        for j in range(len(row_range)):    # available child board in the same row
            child_board = self.generate_child()
            child_board.spot = [obj_row, row_range[j]]    # update new spot (from original posi to moved posi) ([obj_row,obj_col]->[obj_row,row_range[j]])
            if row_range[j] < obj_col:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[obj_row][row_range[j]].direction = 4
            else:
                child_board.block_mat[obj_row][row_range[j]].direction = 2
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 1 or self.block_mat[obj_row][obj_col].direction == 3:
                child_board.block_mat[obj_row][row_range[j]].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            if child_board.block_mat[obj_row][row_range[j]].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_posi_list[obj_row][row_range[j]] = parent_pattern
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[obj_row][row_range[j]].pattern = parent_pattern
                child_board.block_mat[obj_row][obj_col].pattern = 0
                child_board_list.append(child_board)

        for i in range(len(col_range)):
            child_board = self.generate_child()
            child_board.spot = [col_range[i], obj_col]    # update new spot (from original posi to moved posi) ([obj_row,obj_col]->[col_range[i], obj_col])
            if col_range[i] < obj_row:                # update block's direction and turn, and board's total_turns
                child_board.block_mat[col_range[i]][obj_col].direction = 1
            else:
                child_board.block_mat[col_range[i]][obj_col].direction = 3
            child_board.block_mat[obj_row][obj_col].direction = 0
            if self.block_mat[obj_row][obj_col].direction == 2 or self.block_mat[obj_row][obj_col].direction == 4:
                child_board.block_mat[col_range[i]][obj_col].turn = self.block_mat[obj_row][obj_col].turn + 1
                child_board.block_mat[obj_row][obj_col].turn = 0
                child_board.total_turns = child_board.total_turns + 1
            if child_board.block_mat[col_range[i]][obj_col].turn <= limit:    # spot turn should not surpass the limit
                child_board.block_posi_list[col_range[i]][obj_col] = parent_pattern
                child_board.block_posi_list[obj_row][obj_col] = 0
                child_board.block_mat[col_range[i]][obj_col].pattern = parent_pattern
                child_board.block_mat[obj_row][obj_col].pattern = 0
                child_board_list.append(child_board)
            child_board_list.append(child_board)
        
        return child_board_list


    # simple connect
    # straight forward connect all candidates on the original board
    def row_simple_connect(self):    # simple directly connect in a row
        for i in range(self.m):
            for j in range(self.n - 1):
                temp_pattern = self.block_posi_list[i][j]
                if temp_pattern != 0 and temp_pattern != -1:
                    jj = j + 1
                    while(jj < self.n):
                        if self.block_posi_list[i][jj] == 0:
                            jj = jj + 1
                        elif self.block_posi_list[i][jj] != temp_pattern:
                            break
                        else:
                            # print("eliminate: row=%d col1=%d col2=%d" % (i, j, jj))
                            self.block_posi_list[i][j] = 0
                            self.block_posi_list[i][jj] = 0
                            self.block_mat[i][j].pattern = 0
                            self.block_mat[i][jj].pattern = 0
                            break
                        
    def col_simple_connect(self):    # simple directly connect in a column
        for j in range(self.n):
            for i in range(self.m - 1):
                temp_pattern = self.block_posi_list[i][j]
                if temp_pattern != 0 and temp_pattern != -1:
                    ii = i + 1
                    while(ii < self.m):
                        if self.block_posi_list[ii][j] == 0:
                            ii = ii + 1
                        elif self.block_posi_list[ii][j] != temp_pattern:
                            break
                        else:
                            # print("eliminate: col=%d row1=%d row2=%d" % (j, i, ii))
                            self.block_posi_list[i][j] = 0
                            self.block_posi_list[ii][j] = 0
                            self.block_mat[i][j].pattern = 0
                            self.block_mat[ii][j].pattern = 0
                            break

    def simple_connect(self):
        self.row_simple_connect()
        self.col_simple_connect()

