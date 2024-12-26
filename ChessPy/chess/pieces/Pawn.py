from boardgame import Board
from boardgame import Position
from chess import ChessMatch
from chess import ChessPiece
from chess import Color

class Pawn(ChessPiece):

    def __init__(self, board: Board, color: Color, chess_match: ChessMatch):
        super().__init__(board, color)
        self.chess_match = chess_match

    def possible_moves(self):
        mat = [[False for _ in range(self.get_board().get_columns())] for _ in range(self.get_board().get_rows())]

        p = Position(0, 0)

        if self.get_color() == Color.WHITE:
            # Movimentos para as peças brancas
            p.set_values(self.position.get_row() - 1, self.position.get_column())
            if self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
                mat[p.get_row()][p.get_column()] = True

            p.set_values(self.position.get_row() - 2, self.position.get_column())
            p2 = Position(self.position.get_row() - 1, self.position.get_column())
            if (self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p) and
                self.get_board().position_exists(p2) and not self.get_board().there_is_a_piece(p2) and
                self.get_move_count() == 0):
                mat[p.get_row()][p.get_column()] = True

            p.set_values(self.position.get_row() - 1, self.position.get_column() - 1)
            if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
                mat[p.get_row()][p.get_column()] = True

            p.set_values(self.position.get_row() - 1, self.position.get_column() + 1)
            if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
                mat[p.get_row()][p.get_column()] = True

        else:
            # Movimentos para as peças pretas
            p.set_values(self.position.get_row() + 1, self.position.get_column())
            if self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p):
                mat[p.get_row()][p.get_column()] = True

            p.set_values(self.position.get_row() + 2, self.position.get_column())
            p2 = Position(self.position.get_row() + 1, self.position.get_column())
            if (self.get_board().position_exists(p) and not self.get_board().there_is_a_piece(p) and
                self.get_board().position_exists(p2) and not self.get_board().there_is_a_piece(p2) and
                self.get_move_count() == 0):
                mat[p.get_row()][p.get_column()] = True

            p.set_values(self.position.get_row() + 1, self.position.get_column() - 1)
            if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
                mat[p.get_row()][p.get_column()] = True

            p.set_values(self.position.get_row() + 1, self.position.get_column() + 1)
            if self.get_board().position_exists(p) and self.is_there_opponent_piece(p):
                mat[p.get_row()][p.get_column()] = True

        return mat

    def __str__(self):
        return "P"
