from boardgame import Board
from boardgame import Position
from chess import ChessPiece
from chess import Color

class Queen(ChessPiece):

    def __init__(self, board: Board, color: Color):
        super().__init__(board, color)

    def __str__(self):
        return "Q"

    def possible_moves(self):
        mat = [[False for _ in range(self.get_board().get_columns())] for _ in range(self.get_board().get_rows())]

        p = Position(0, 0)

        # above
        p.set_values(self.position.get_row() - 1, self.position.get_column())
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_row(p.get_row() - 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # left
        p.set_values(self.position.get_row(), self.position.get_column() - 1)
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_column(p.get_column() - 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # right
        p.set_values(self.position.get_row(), self.position.get_column() + 1)
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_column(p.get_column() + 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # below
        p.set_values(self.position.get_row() + 1, self.position.get_column())
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_row(p.get_row() + 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # nw
        p.set_values(self.position.get_row() - 1, self.position.get_column() - 1)
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_values(p.get_row() - 1, p.get_column() - 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # ne
        p.set_values(self.position.get_row() - 1, self.position.get_column() + 1)
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_values(p.get_row() - 1, p.get_column() + 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # se
        p.set_values(self.position.get_row() + 1, self.position.get_column() + 1)
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_values(p.get_row() + 1, p.get_column() + 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        # sw
        p.set_values(self.position.get_row() + 1, self.position.get_column() - 1)
        while self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
            mat[p.get_row()][p.get_column()] = True
            p.set_values(p.get_row() + 1, p.get_column() - 1)
        if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
            mat[p.get_row()][p.get_column()] = True

        return mat
