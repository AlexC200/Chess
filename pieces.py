from piece_model import *
from game import *


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        if self.color == Color.White:
            self.set_image(0, 0)
        else:
            self.set_image(0, 105)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        valid_moves = []
        valid_moves += self._horizontal_moves(y, x, 1, 0, 1)
        valid_moves += self._horizontal_moves(y, x, -1, 0, 1)
        valid_moves += self._vertical_moves(y, x, 0, 1, 1)
        valid_moves += self._vertical_moves(y, x, 0, -1, 1)
        valid_moves += self._diagonal_moves(y, x, -1, 1, 1)
        valid_moves += self._diagonal_moves(y, x, -1, -1, 1)
        valid_moves += self._diagonal_moves(y, x, 1, 1, 1)
        valid_moves += self._diagonal_moves(y, x, 1, -1, 1)
        return valid_moves

    def __copy__(self):
        return King(self.color)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.max_distance = 8
        if self.color == Color.White:
            self.set_image(1, 1)
        else:
            self.set_image(0, 106)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        valid_moves = []
        valid_moves += self._horizontal_moves(y, x, 1, 0, 8)
        valid_moves += self._horizontal_moves(y, x, -1, 0, 8)
        valid_moves += self._vertical_moves(y, x, 0, 1, 8)
        valid_moves += self._vertical_moves(y, x, 0, -1, 8)
        valid_moves += self._diagonal_moves(y, x, -1, 1, 8)
        valid_moves += self._diagonal_moves(y, x, -1, -1, 8)
        valid_moves += self._diagonal_moves(y, x, 1, 1, 8)
        valid_moves += self._diagonal_moves(y, x, 1, -1, 8)
        return valid_moves

    def __copy__(self):
        return Queen(self.color)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == Color.White:
            self.set_image(2, 2)
        else:
            self.set_image(0, 105)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        moves = []
        moves += self.get_diagonal_moves(y,x,8)
        return moves


    # def get_moves(self, position):
    #     for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
    #         for i in range(1, 8):
    #             new_x, new_y = x + i * dx, y + i * dy
    #             if not self.is_valid_position((new_x, new_y)):
    #                 break
    #             moves.append((new_x, new_y))
    #             if self.board[new_x][new_y] is not None:
    #                 break
    #     return moves

    def __copy__(self):
        return Bishop(self.color)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == Color.White:
            self.set_image(3, 3)
        else:
            self.set_image(0, 105)

    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        possible_moves = [
            (y-2, x-1), (y-2, x+1), (y-1, x-2), (y-1, x+2),
            (y+1, x-2), (y+1, x+2), (y+2, x-1), (y+2, x+1)
        ]
        valid_moves = []
        for move in possible_moves:
            y_new, x_new = move
            if 0 <= y_new < self._game.board.size and 0 <= x_new < self._game.board.size:
                if self._game.board.grid[y_new][x_new] is None or self._game.board.grid[y_new][x_new].color != self.color:
                    valid_moves.append(move)
        return valid_moves

    def __copy__(self):
        return Knight(self.color)


'''Rook class checks if the given move is either horizontal 
or vertical by comparing the x and y coordinates.'''


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color == Color.White:
            self.set_image(4, 4)
        else:
            self.set_image(0, 105)

    def valid_moves(self, x, y):
        if x == self.x or y == self.y:
            if abs(x - self.x) <= 8 and abs(y - self.y) <= 8:
                return True
        return False

    def __copy__(self):
        return Rook(self.color)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        if self.color == Color.White:
            self.set_image(5, 5)
        else:
            self.set_image(0, 105)
        self.has_moved = False

    def valid_moves(self, pos, board):
        moves = []
        if self.color == "white":
            if not board[self.x][y+1]:
                moves.append((self.x, self.y+1))
                if not self.has_moved and not board[self.x][self.y+2]:
                    moves.append((self.x, self.y+2))
            if self.x > 0 and self.y < 7 and board[self.x-1][self.y+1] and board[self.x-1][self.y+1].color != self.color:
                moves.append((self.x-1, self.y+1))
            if self.x < 7 and self.y < 7 and board[self.x+1][self.y+1] and board[self.x+1][self.y+1].color != self.color:
                moves.append((self.x+1, self.y+1))

        else: # black
            if not board[self.x][self.y-1]:
                moves.append((self.x, self.y-1))
                if not self.has_moved and not board[self.x][self.y-2]:
                    moves.append((self.x, self.y-2))
            if self.x > 0 and self.y > 0 and board[self.x-1][self.y-1] and board[self.x-1][self.y-1].color != self.color:
                moves.append((self.x-1, self.y-1))
            if self.x < 7 and self.y > 0 and board[self.x+1][self.y-1] and board[self.x+1][self.y-1].color != self.color:
                moves.append((self.x+1, self.y-1))

        return moves

    def __copy__(self):
        copy_pawn = Pawn(self.color)
        copy_pawn.has_moved = self.has_moved
        return copy_pawn
