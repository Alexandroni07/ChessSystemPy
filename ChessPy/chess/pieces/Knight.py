from boardgame import Board
from boardgame import Position
from chess import ChessPiece
from chess import Color

class Knight(ChessPiece):

    def __init__(self, board: Board, color: Color):
        super().__init__(board, color)

    def __str__(self):
        return "N"

    def can_move(self, position: Position) -> bool:
        p = self.get_board().piece(position)
        return p is None or p.get_color() != self.get_color()

    def possible_moves(self):
        mat = [[False for _ in range(self.get_board().get_columns())] for _ in range(self.get_board().get_rows())]
        
        p = Position(0, 0)

        # Movimentos em forma de "L"
        moves = [
            (-1, -2), (-2, -1), (-2, 1), (-1, 2), 
            (1, 2), (2, 1), (2, -1), (1, -2)
        ]

        for move in moves:
            p.set_values(self.position.get_row() + move[0], self.position.get_column() + move[1])
            if self.get_board().position_exists(p) and self.can_move(p):
                mat[p.get_row()][p.get_column()] = True

        return mat
