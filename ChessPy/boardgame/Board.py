class BoardException(Exception):
    pass

class Piece:
    def __init__(self):
        self.position = None

    # A classe Piece deve ser estendida por outras peças como Rei, Rainha, etc.

class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def __repr__(self):
        return f"({self.row}, {self.column})"

    # Permite verificar as comparações de posições facilmente
    def __eq__(self, other):
        return isinstance(other, Position) and self.row == other.row and self.column == other.column

class Board:

    def __init__(self, rows, columns):
        if rows < 1 or columns < 1:
            raise BoardException("Error creating board: there must be at least 1 row and 1 column")
        self.rows = rows
        self.columns = columns
        self.pieces = [[None for _ in range(columns)] for _ in range(rows)]

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def piece(self, row, column):
        if not self.position_exists(row, column):
            raise BoardException("Position not on the board")
        return self.pieces[row][column]

    def piece_by_position(self, position):
        if not self.position_exists(position):
            raise BoardException("Position not on the board")
        return self.pieces[position.get_row()][position.get_column()]

    def place_piece(self, piece, position):
        if self.there_is_a_piece(position):
            raise BoardException(f"There is already a piece on position {position}")
        self.pieces[position.get_row()][position.get_column()] = piece
        piece.position = position

    def remove_piece(self, position):
        if not self.position_exists(position):
            raise BoardException("Position not on the board")
        if self.piece_by_position(position) is None:
            return None
        aux = self.piece_by_position(position)
        aux.position = None
        self.pieces[position.get_row()][position.get_column()] = None
        return aux

    def position_exists(self, position):
        # Este método agora recebe um objeto Position diretamente
        return 0 <= position.get_row() < self.rows and 0 <= position.get_column() < self.columns

    def there_is_a_piece(self, position):
        if not self.position_exists(position):
            raise BoardException("Position not on the board")
        return self.piece_by_position(position) is not None


# Exemplo de uso do código

# Suponha que o tabuleiro seja 8x8 e tenha peças
board = Board(8, 8)
position = Position(1, 1)

# Criando uma peça fictícia para ser colocada no tabuleiro
piece = Piece()

board.place_piece(piece, position)

# Verificando se a peça foi colocada corretamente
print(board.piece_by_position(position))  # Deve mostrar a peça na posição (1, 1)

# Remover a peça
removed_piece = board.remove_piece(position)
print(removed_piece)  # Mostrando que a peça foi removida da posição
