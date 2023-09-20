from piece_model import Board


def _diagonal_moves(y: int, x: int, y_d: int, x_d: int, distance: int):
    board = [[ '' for y in range(8)] for x in range(8)]
    for i in range(8):
        board[0][i] = 'B'
        board[1][i] = 'B'
        board[6][i] = 'W'
        board[7][i] = 'W'
    for row in board:
        for col in row:
            print(col,end='')
        print()
#     valid_moves = []
#     for i in range(1, distance+1):
#          y_new = y + i*y_d
#          x_new = x + i*x_d
#          print(x_new, y_new)
#          is_y_valid = 0 <= y_new < 8
#          is_x_valid = 0 <= x_new < 8
#          is_space_empty = board[y_new][x_new] == ''
#          if is_y_valid and is_x_valid and is_space_empty:
#              valid_moves.append((y_new, x_new))
#          else:
#              break
#          return valid_moves
#     print(valid_moves)
#
# print(_diagonal_moves(3, 4, -1, -1, 8))

# def _horizontal_moves(y: int, x: int, distance: int):
#             valid_moves = []
#             for i in range(1, distance+1):
#                 x_new = x + i
#                 if 0 <= x_new < size and self.grid[y][x_new] is None:
#                     valid_moves.append((y, x_new))
#                 else:
#                     break
#             for i in range(1, distance+1):
#                 x_new = x - i
#                 if 0 <= x_new < self.size and self.grid[y][x_new] is None:
#                     valid_moves.append((y, x_new))
#                 else:
#                     break
#             return valid_moves

# print(_horizontal_moves(3, 4, -1, -1, 8))

a_board = Board(8)
print(a_board.size)
print(a_board(3,4,-1,-1,2) )
