from boardgame import Board
from boardgame import Position
from chess import ChessMatch
from chess import ChessPiece
from chess import Color
from chess.pieces import Rook


class King(ChessPiece):
    def __init__(self, board: Board, color: Color, chess_match: ChessMatch):
        super().__init__(board, color)
        self.chess_match = chess_match

    def __str__(self):
        return "K"

    def can_move(self, position: Position) -> bool:
        p = self.get_board().piece(position)
        return p is None or p.get_color() != self.get_color()

    def test_rook_castling(self, position: Position) -> bool:
        p = self.get_board().piece(position)
        return p is not None and isinstance(p, Rook) and p.get_color() == self.get_color() and p.get_move_count() == 0

    def possible_moves(self):
        mat = [[False for _ in range(self.get_board().get_columns())] for _ in range(self.get_board().get_rows())]
        p = Position(0, 0)

        # acima
        p.set_values(self.position.get_row() - 1, self.position.get_column())
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # abaixo
        p.set_values(self.position.get_row() + 1, self.position.get_column())
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # esquerda
        p.set_values(self.position.get_row(), self.position.get_column() - 1)
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # direita
        p.set_values(self.position.get_row(), self.position.get_column() + 1)
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # noroeste
        p.set_values(self.position.get_row() - 1, self.position.get_column() - 1)
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # nordeste
        p.set_values(self.position.get_row() - 1, self.position.get_column() + 1)
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # sudoeste
        p.set_values(self.position.get_row() + 1, self.position.get_column() - 1)
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # sudeste
        p.set_values(self.position.get_row() + 1, self.position.get_column() + 1)
        if self.get_board().position_exists(p) and self.can_move(p):
            mat[p.get_row()][p.get_column()] = True

        # castling
        if self.get_move_count() == 0 and not self.chess_match.get_check():
            # castling kingside rook
            pos_t1 = Position(self.position.get_row(), self.position.get_column() + 3)
            if self.test_rook_castling(pos_t1):
                p1 = Position(self.position.get_row(), self.position.get_column() + 1)
                p2 = Position(self.position.get_row(), self.position.get_column() + 2)
                if self.get_board().piece(p1) is None and self.get_board().piece(p2) is None:
                    mat[self.position.get_row()][self.position.get_column() + 2] = True

            # castling queenside rook
            pos_t2 = Position(self.position.get_row(), self.position.get_column() - 4)
            if self.test_rook_castling(pos_t2):
                p1 = Position(self.position.get_row(), self.position.get_column() - 1)
                p2 = Position(self.position.get_row(), self.position.get_column() - 2)
                p3 = Position(self.position.get_row(), self.position.get_column() - 3)
                if (self.get_board().piece(p1) is None and self.get_board().piece(p2) is None and
                        self.get_board().piece(p3) is None):
                    mat[self.position.get_row()][self.position.get_column() - 2] = True

        return mat
