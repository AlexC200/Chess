from enum import Enum
from abc import ABC, abstractmethod
import pygame as pg
from typing import List, Tuple
# from game import Game
from piece_model import *


class Color(Enum):
    White = 1
    Black = 2


class Piece(ABC):

    SPRITESHEET = pg.image.load("./images/pieces.png")
    _game = None

    @abstractmethod
    def move(self):
        pass

    def __init__(self, color):
        self._color = color
        self._image = pg.Surface((105, 105), pg.SRCALPHA)

    @property
    def color(self):
        return self._color

    @staticmethod
    def set_board(game):
        Piece._game = game

    @staticmethod
    def set_game(game):
        Piece._game = game

    def set_image(self, x: int, y: int) -> None:
        self._image.blit(Piece.SPRITESHEET, (0, 0), pg.Rect(x, y, 105, 105))

    def move(self, y: int, x: int):
        self.y = y
        self.x = x

    def __repr__(self):
        return f"{self.color} piece at ({self.y}, {self.x})"

    @abstractmethod
    def valid_moves(self, y: int, x: int) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def __copy__(self):
        pass


class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List[Tuple[int, int]]:
        valid_moves = []
        board = []
        for i in range(1, distance+1):
            y_new = y + i*y_d
            x_new = x + i*x_d
            if 0 <= y_new < 8  and 0 <= x_new < 0 and board [y_new][x_new] == '':
                valid_moves.append((y_new, x_new))
            else:
                break
        print(valid_moves)
        return valid_moves

    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List[Tuple[int, int]]:
        valid_moves = []
        for i in range(1, distance+1):
            x_new = x + i
            if 0 <= x_new < self.size and self.grid[y][x_new] is None:
                valid_moves.append((y, x_new))
            else:
                break
        for i in range(1, distance+1):
            x_new = x - i
            if 0 <= x_new < self.size and self.grid[y][x_new] is None:
                valid_moves.append((y, x_new))
            else:
                break
        return valid_moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int) -> List[Tuple[int, int]]:
        valid_moves = []
        for i in range(1, distance+1):
            y_new = y + y_d*i
            if 0 <= y_new < self.size and self.grid[y_new][x] is None:
                valid_moves.append((y_new, x))
            else:
                break
        for i in range(1, distance+1):
            y_new = y - y_d*i
            if 0 <= y_new < self.size and self.grid[y_new][x] is None:
                valid_moves.append((y_new, x))
            else:
                break
        return valid_moves

    def get_diagonal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        valid_moves = []
        valid_moves += self._diagonal_moves(y, x, -1, 1, distance)
        valid_moves += self._diagonal_moves(y, x, -1, -1, distance)
        valid_moves += self._diagonal_moves(y, x, 1, 1, distance)
        valid_moves += self._diagonal_moves(y, x, 1, -1, distance)
        return valid_moves

    def get_horizontal_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        valid_moves = []
        valid_moves += self._horizontal_moves(y, x, distance, 1)
        valid_moves += self._horizontal_moves(y, x, distance, -1)
        return valid_moves

    def get_vertical_moves(self, y: int, x: int, distance: int) -> List[Tuple[int, int]]:
        valid_moves = []
        valid_moves += self._vertical_moves(y, x, -1, 0, distance)
        valid_moves += self._vertical_moves(y, x, 1, 0, distance)
        return valid_moves
