from piece_model import *
from pieces import *
import random



class Game:
    # Start with a comprehension list
    def __init__(self):
        self.board = [[None for i in range(8)] for i in range(8)]
        self._setup_pieces()
        self.player = Color.White
        # Pieces for board
        # Stack (list) for board states
        self.board_state = []
        Piece.set_game(self)

        # reset method
    def reset(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.player = Color.White
        self.board_state = []

        # _setup_pieces method
    def _setup_pieces(self):
        # fill board with pieces
        for row in range(8):
            if 1 < row < 6:
                continue
            if row == 0:
                self.board[row] = [Rook(Color.Black), Knight(Color.Black), Bishop(Color.Black),
                                   Queen(Color.Black), Knight(Color.Black), Bishop(Color.Black),
                                   Knight(Color.Black), Rook(Color.Black)]
            if row == 7:
                self.board[row] = [Rook(Color.White), Knight(Color.White), Bishop(Color.White),
                                   Queen(Color.White), Knight(Color.White), Bishop(Color.White),
                                   Knight(Color.White), Rook(Color.White)]
            if row == 1:
                self.board[row] = [Pawn(Color.Black) for x in range (8)]
            if row == 6:
                self.board[row] = [Pawn(Color.White) for x in range (8)]

        # get method
    def get(self, y: int, x:int):
        if x in range(8) and y in range(8):
            return self.board[y][x]
        else:
            return None

        # switch method
    def switch_player(self):
        if self.player == Color.White:
            self.player = Color.Black

    def undo(self):
        if self.board_state[-1] == []:
            return False
        else:
            self.board = self.board_state.pop()
            return True

    def copy_board(self) -> 'Board':
        new_board = Board(self.size)
        for y in range(self.size):
            for x in range(self.size):
                piece = self.grid[y][x]
                if piece is not None:
                    new_board.grid[y][x] = piece.copy()
        return new_board

        # move
    def moves(self, piece: Piece, y: int, x: int, y2: int, x2: int) -> bool:
        prior_state = [row[:] for row in self.board]
        self.prior_states.append(prior_state)

        # perform the move
        self.board[y2][x2] = piece
        self.board[y][x] = None

        # update pawn's first move status
        if isinstance(piece, Pawn):
            piece.has_moved = True

            # check for promotion to queen
            if y2 == 0 and piece.color == 'black':
                self.board[y2][x2] = Queen('black')
            elif y2 == 7 and piece.color == 'white':
                self.board[y2][x2] = Queen('white')

        # determine if the move resulted in the current player being in check
        in_check = self.is_check(self.current_player)

        # undo the move if the current player is in check
        if in_check:
            self.board = self.prior_states.pop()
            return False

        # switch the current player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True

    def is_check(self, color: str) -> bool:
        # determine if the player of the given color is in check
        pass


class Piece:
    def __init__(self, color: str):
        self.color = color


class Pawn(Piece):
    def __init__(self, color: str):
        super().__init__(color)
        self.has_moved = False


#class Queen(Piece):
    pass

        # get_piece_location
        # Do we use 'self.board_state' in this function?
    def get_piece_locations(self, color: Color) -> List[Tuple[int, int]]:
        locations = []
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color == color:
                    locations.append((y, x))
        return locations


        # find_king
    def find_king(self, color: Color) -> Tuple[int, int]:
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if isinstance(piece, King) and piece.color == color:
                    return (y, x)

        # check
    def check(self, color: Color) -> bool:
        # get locations of opposing pieces
        opposing_color = "white" if color == "black" else "black"
        opposing_piece_locations = self.get_piece_locations(opposing_color)

        # get possible moves for opposing pieces
        possible_moves = []
        for location in opposing_piece_locations:
            piece = self.board[location[0]][location[1]]
            moves = piece.valid_moves(self)
            possible_moves.extend(moves)

        # check if king is in possible moves
        King_location = self.find_king(color)
        if King_location in possible_moves:
            return True
        else:
            return False

    def mate(self, color: Color) -> bool:
        # first, call the check function to check if the king is in check
        if not self.check(color):
            return False

        # get the king's location and a list of possible moves for the king
        king_location = self.find_king(color)
        king_possible_moves = self.board[king_location[0]][king_location[1]].valid_moves(self)

        # check if there is a move the king can perform to escape check
        for move in king_possible_moves:
            # check if the move is not in the list of the opponent's possible moves
            if move not in self.get_opponent_moves(color):
                return False

        # check if there is another piece that can block the check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    # get a list of possible moves for the current piece
                    possible_moves = piece.valid_moves(self)
                    for move in possible_moves:
                        # try each move and check if the king is still in check
                        temp_board = self.copy()
                        temp_board.move((row, col), move)
                        if not temp_board.check(color):
                            return False

        # if no move can get the king out of check and no piece can block the check, the king is in checkmate
        return True


        # _computer_move
    def computer_move(self,board):
        possible_moves = self.get_piece_locations(Color.Black)
        y,x = random.choice(possible_moves)
        moves = self.board[y][x].valid_moves(y,x)
        for move in moves:
            self.move(self.board[y][x],y,x,move[0],move[1])
        board = self.board
        # for i in range(len(board)):
        #     for j in range(len(board[i])):
        #         if board[i][j] == 'P':
        #             # Check if the pawn can move one or two squares forward
        #             if i == 1 and board[2][j] is None:
        #                 possible_moves.append((i, j, i+2, j))
        #             if board[i+1][j] is None:
        #                 possible_moves.append((i, j, i+1, j))
        #
        # random_move = random.choice(possible_moves)
        # return random_move[0], random_move[1], random_move[2], random_move[3]



