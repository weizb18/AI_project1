import random
from board import *
from utils import *
from search import *
from generate_board import *
import copy

# dc_posi_list = [
#     [2, 4, 1, 5],
#     [3, 2, 1, 0],
#     [0, 4, 3, 2],
#     [2, 0, 5, 0]
# ]
# dc_posi_list = [
#     [3, 1, 2],
#     [1, 3, 2],
#     [0, 1, 1]
# ]
# dc_posi_list = [
#     [3, 0, 4, 3],
#     [0, 2, 3, 3],
#     [2, 3, 2, 0],
#     [3, 2, 4, 0]
# ]
# dc_posi_list = [
#     [3, 2, 0],
#     [2, 3, 0],
#     [0, 0, 0]
# ]
# dc_posi_list = [
#     [-1, 1, 0],
#     [1, -1, 1],
#     [2, 2, 1]
# ]
# dc_posi_list = [
#     [3, 0, 4, 3],
#     [0, -1, 3, 3],
#     [2, 3, -1, 0],
#     [3, 2, 4, 0]
# ]

dc_board = generate_random_board(4, 4, 6, 4)
# dc_board = generate_random_board_blocks(4, 4, 6, 4)
# dc_board = generate_assign_board(dc_posi_list)

limit = 2
final_board = bfs_with_limit(dc_board, limit)
# final_board = bfs_without_limit(dc_board)
# final_board = bfs_with_limit_prior_connect(dc_board, limit)
# final_board = bfs_without_limit_prior_connect(dc_board)

final_board.print_block_mat()
print("total turns = %d" % final_board.total_turns)
while final_board != None:
    final_board.print_block_mat()
    print('')
    final_board = final_board.parent

