from abc import ABC, ABCMeta, abstractmethod
from chess.ChessPosition import ChessPosition
from boardgame import Piece

class ChessPiece:
    """
    Classe ChessPiece que herda de Piece e ABC.
    Agora, a herança das metaclasses é feita corretamente com ABCMeta.
    """

    def __init__(self, board, color):
        super().__init__(board)  # Chama o construtor da classe base 'Piece'
        self.board = board
        self.color = color
        self.move_count = 0

    @abstractmethod
    def possible_moves(self):
        pass   

    def get_color(self):
        return self.color

    def get_move_count(self):
        return self.move_count

    def increase_move_count(self):
        self.move_count += 1

    def decrease_move_count(self):
        self.move_count -= 1

    def get_chess_position(self):
        return ChessPosition.from_position(self.position)

    def is_there_opponent_piece(self, position):
        piece = self.get_board().piece(position)
        return piece is not None and piece.get_color() != self.color