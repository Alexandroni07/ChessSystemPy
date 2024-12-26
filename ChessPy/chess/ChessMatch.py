from chess.pieces import Bishop, King, Knight, Pawn, Queen, Rook
from boardgame import Board, Piece, Position
from chess.ChessPiece import ChessPiece
from chess.ChessPosition import ChessPosition
from enum import Enum
import copy
from chess import Color
from chess import ChessException


class ChessMatch:
    def __init__(self):
        self.board = Board(8, 8)
        self.turn = 1
        self.current_player = Color.WHITE
        self.check = False
        self.checkmate = False
        self.en_passant_vulnerable = None
        self.promoted = None
        self.pieces_on_the_board = []
        self.captured_pieces = []
        self.initial_setup()

    def get_turn(self):
        return self.turn

    def get_current_player(self):
        return self.current_player

    def get_check(self):
        return self.check

    def get_check_mate(self):
        return self.checkmate

    def get_en_passant_vulnerable(self):
        return self.en_passant_vulnerable

    def get_promoted(self):
        return self.promoted

    def get_pieces(self):
        pieces_matrix = [[None for _ in range(self.board.get_columns())] for _ in range(self.board.get_rows())]
        for i in range(self.board.get_rows()):
            for j in range(self.board.get_columns()):
                pieces_matrix[i][j] = self.board.piece(i, j)
        return pieces_matrix

    def possible_moves(self, source_position):
        position = source_position.to_position()
        self.validate_source_position(position)
        return self.board.piece(position).possible_moves()

    def perform_chess_move(self, source_position, target_position):
        source = source_position.to_position()
        target = target_position.to_position()
        self.validate_source_position(source)
        self.validate_target_position(source, target)
        captured_piece = self.make_move(source, target)

        if self.test_check(self.current_player):
            self.undo_move(source, target, captured_piece)
            raise ChessException("You can't put yourself in check")

        moved_piece = self.board.piece(target)

        # Promotion
        self.promoted = None
        if isinstance(moved_piece, Pawn):
            if (moved_piece.get_color() == Color.WHITE and target.get_row() == 0) or \
                (moved_piece.get_color() == Color.BLACK and target.get_row() == 7):
                self.promoted = self.board.piece(target)
                self.promoted = self.replace_promoted_piece("Q")

        self.check = self.test_check(self.opponent(self.current_player))

        if self.test_check_mate(self.opponent(self.current_player)):
            self.checkmate = True
        else:
            self.next_turn()

        # En passant
        if isinstance(moved_piece, Pawn) and \
                (target.get_row() == source.get_row() - 2 or target.get_row() == source.get_row() + 2):
            self.en_passant_vulnerable = moved_piece
        else:
            self.en_passant_vulnerable = None

        return captured_piece

        position = self.promoted.get_chess_position().to_position()
        piece = self.board.remove_piece(position)
        self.pieces_on_the_board.remove(piece)

        new_piece = self.create_new_piece(piece_type, self.promoted.get_color())
        self.board.place_piece(new_piece, position)
        self.pieces_on_the_board.append(new_piece)

        return new_piece

    def create_new_piece(self, piece_type, color):
        if piece_type == "B":
            return Bishop(self.board, color)
        if piece_type == "N":
            return Knight(self.board, color)
        if piece_type == "Q":
            return Queen(self.board, color)
        return Rook(self.board, color)

    def make_move(self, source, target):
        piece = self.board.remove_piece(source)
        piece.increase_move_count()
        captured_piece = self.board.remove_piece(target)
        self.board.place_piece(piece, target)

        if captured_piece:
            self.pieces_on_the_board.remove(captured_piece)
            self.captured_pieces.append(captured_piece)

        # Castling kingside rook
        if isinstance(piece, King) and target.get_column() == source.get_column() + 2:
            source_t = Position(source.get_row(), source.get_column() + 3)
            target_t = Position(source.get_row(), source.get_column() + 1)
            rook = self.board.remove_piece(source_t)
            self.board.place_piece(rook, target_t)
            rook.increase_move_count()

        # Castling queenside rook
        if isinstance(piece, King) and target.get_column() == source.get_column() - 2:
            source_t = Position(source.get_row(), source.get_column() - 4)
            target_t = Position(source.get_row(), source.get_column() - 1)
            rook = self.board.remove_piece(source_t)
            self.board.place_piece(rook, target_t)
            rook.increase_move_count()

        # En passant
        if isinstance(piece, Pawn):
            if source.get_column() != target.get_column() and captured_piece is None:
                pawn_position = Position(target.get_row() + 1, target.get_column()) if piece.get_color() == Color.WHITE else Position(target.get_row() - 1, target.get_column())
                captured_piece = self.board.remove_piece(pawn_position)
                self.captured_pieces.append(captured_piece)
                self.pieces_on_the_board.remove(captured_piece)

        return captured_piece

    def undo_move(self, source, target, captured_piece):
        piece = self.board.remove_piece(target)
        piece.decrease_move_count()
        self.board.place_piece(piece, source)

        if captured_piece:
            self.board.place_piece(captured_piece, target)
            self.captured_pieces.remove(captured_piece)
            self.pieces_on_the_board.append(captured_piece)

        # Castling kingside rook
        if isinstance(piece, King) and target.get_column() == source.get_column() + 2:
            source_t = Position(source.get_row(), source.get_column() + 3)
            target_t = Position(source.get_row(), source.get_column() + 1)
            rook = self.board.remove_piece(target_t)
            self.board.place_piece(rook, source_t)
            rook.decrease_move_count()

        # Castling queenside rook
        if isinstance(piece, King) and target.get_column() == source.get_column() - 2:
            source_t = Position(source.get_row(), source.get_column() - 4)
            target_t = Position(source.get_row(), source.get_column() - 1)
            rook = self.board.remove_piece(target_t)
            self.board.place_piece(rook, source_t)
            rook.decrease_move_count()

        # En passant
        if isinstance(piece, Pawn):
            if source.get_column() != target.get_column() and captured_piece == self.en_passant_vulnerable:
                pawn = self.board.remove_piece(target)
                pawn_position = Position(3, target.get_column()) if piece.get_color() == Color.WHITE else Position(4, target.get_column())
                self.board.place_piece(pawn, pawn_position)

    def validate_source_position(self, position):
        if not self.board.there_is_a_piece(position):
            raise ChessException("There is no piece at the source position")
        if self.current_player != self.board.piece(position).get_color():
            raise ChessException("The selected piece is not yours")
        if not self.board.piece(position).is_there_any_possible_move():
            raise ChessException("There are no possible moves for the selected piece")

    def validate_target_position(self, source, target):
        if not self.board.piece(source).possible_move(target):
            raise ChessException("The selected piece can't move to the target position")

    def next_turn(self):
        self.turn += 1
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

    def opponent(self, color):
        return Color.BLACK if color == Color.WHITE else Color.WHITE

    def king(self, color):
        pieces = [p for p in self.pieces_on_the_board if isinstance(p, ChessPiece) and p.get_color() == color]
        for piece in pieces:
            if isinstance(piece, King):
                return piece


    def test_check(self, color):
        king_position = self.king(color).get_chess_position().to_position()
        opponent_pieces = [p for p in self.pieces_on_the_board if isinstance(p, ChessPiece) and p.get_color() == self.opponent(color)]
        for piece in opponent_pieces:
            moves = piece.possible_moves()
            if moves[king_position.get_row()][king_position.get_column()]:
                return True
        return False

    def test_check_mate(self, color):
        if not self.test_check(color):
            return False
        pieces = [p for p in self.pieces_on_the_board if isinstance(p, ChessPiece) and p.get_color() == color]
        for piece in pieces:
            moves = piece.possible_moves()
            for i in range(self.board.get_rows()):
                for j in range(self.board.get_columns()):
                    if moves[i][j]:
                        source = piece.get_chess_position().to_position()
                        target = Position(i, j)
                        captured_piece = self.make_move(source, target)
                        if not self.test_check(color):
                            self.undo_move(source, target, captured_piece)
                            return False
                        self.undo_move(source, target, captured_piece)
        return True

    def place_new_piece(self, column, row, piece):
        self.board.place_piece(piece, ChessPosition(column, row).to_position())
        self.pieces_on_the_board.append(piece)

    def initial_setup(self):
        self.place_new_piece('a', 1, Rook(self.board, Color.WHITE))
        self.place_new_piece('b', 1, Knight(self.board, Color.WHITE))
        self.place_new_piece('c', 1, Bishop(self.board, Color.WHITE))
        self.place_new_piece('e', 1, King(self.board, Color.WHITE, self))
        self.place_new_piece('f', 1, Bishop(self.board, Color.WHITE))
        self.place_new_piece('d', 1, Queen(self.board, Color.WHITE))
        self.place_new_piece('g', 1, Knight(self.board, Color.WHITE))
        self.place_new_piece('h', 1, Rook(self.board, Color.WHITE))
        self.place_new_piece('a', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('b', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('c', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('d', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('e', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('f', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('g', 2, Pawn(self.board, Color.WHITE, self))
        self.place_new_piece('h', 2, Pawn(self.board, Color.WHITE, self))

        self.place_new_piece('a', 8, Rook(self.board, Color.BLACK))
        self.place_new_piece('b', 8, Knight(self.board, Color.BLACK))
        self.place_new_piece('c', 8, Bishop(self.board, Color.BLACK))
        self.place_new_piece('d', 8, Queen(self.board, Color.BLACK))
        self.place_new_piece('e', 8, King(self.board, Color.BLACK, self))
        self.place_new_piece('f', 8, Bishop(self.board, Color.BLACK))
        self.place_new_piece('g', 8, Knight(self.board, Color.BLACK))
        self.place_new_piece('h', 8, Rook(self.board, Color.BLACK))
        self.place_new_piece('a', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('b', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('c', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('d', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('e', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('f', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('g', 7, Pawn(self.board, Color.BLACK, self))
        self.place_new_piece('h', 7, Pawn(self.board, Color.BLACK, self))
