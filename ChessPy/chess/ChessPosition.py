from boardgame import Position

class ChessException(Exception):
    pass

class ChessPosition:

    def __init__(self, column, row):
        if column < 'a' or column > 'h' or row < 1 or row > 8:
            raise ChessException("Error instantiating ChessPosition. Valid values are from a1 to h8")
        self.column = column
        self.row = row

    def get_column(self):
        return self.column

    def get_row(self):
        return self.row

    def to_position(self):
        # Converte ChessPosition para a posição interna (Position)
        return Position(8 - self.row, ord(self.column) - ord('a'))

    @staticmethod
    def from_position(position):
        # Converte Position para ChessPosition
        return ChessPosition(chr(ord('a') + position.get_column()), 8 - position.get_row())

    def __str__(self):
        return f"{self.column}{self.row}"
