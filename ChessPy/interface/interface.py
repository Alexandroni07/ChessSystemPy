import os
from typing import List
from chess import ChessPosition


# ANSI codes for colors
ANSI_RESET = "\u001B[0m"
ANSI_BLACK = "\u001B[30m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_BLUE = "\u001B[34m"
ANSI_PURPLE = "\u001B[35m"
ANSI_CYAN = "\u001B[36m"
ANSI_WHITE = "\u001B[37m"

ANSI_BLACK_BACKGROUND = "\u001B[40m"
ANSI_RED_BACKGROUND = "\u001B[41m"
ANSI_GREEN_BACKGROUND = "\u001B[42m"
ANSI_YELLOW_BACKGROUND = "\u001B[43m"
ANSI_BLUE_BACKGROUND = "\u001B[44m"
ANSI_PURPLE_BACKGROUND = "\u001B[45m"
ANSI_CYAN_BACKGROUND = "\u001B[46m"
ANSI_WHITE_BACKGROUND = "\u001B[47m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def read_chess_position():
    try:
        s = input()
        column = s[0]
        row = int(s[1])
        return ChessPosition(column, row)
    except Exception:
        raise ValueError("Error reading ChessPosition. Valid values are from a1 to h8.")


def print_match(chess_match, captured):
    print_board(chess_match.get_pieces())
    print()
    print_captured_pieces(captured)
    print()
    print(f"Turn: {chess_match.get_turn()}")
    
    if not chess_match.get_checkmate():
        print(f"Waiting player: {chess_match.get_current_player()}")
        if chess_match.get_check():
            print("CHECK!")
    else:
        print("CHECKMATE!")
        print(f"Winner: {chess_match.get_current_player()}")


def print_board(pieces):
    for i in range(len(pieces)):
        print(f"{8 - i} ", end="")
        for j in range(len(pieces)):
            print_piece(pieces[i][j], False)
        print()
    print("  a b c d e f g h")


def print_board_with_possible_moves(pieces, possible_moves):
    for i in range(len(pieces)):
        print(f"{8 - i} ", end="")
        for j in range(len(pieces)):
            print_piece(pieces[i][j], possible_moves[i][j])
        print()
    print("  a b c d e f g h")


def print_piece(piece, background):
    if background:
        print(ANSI_BLUE_BACKGROUND, end="")
        
    if piece is None:
        print(f"-{ANSI_RESET}", end="")
    else:
        if piece.get_color() == 'WHITE':
            print(f"{ANSI_WHITE}{piece}{ANSI_RESET}", end="")
        else:
            print(f"{ANSI_YELLOW}{piece}{ANSI_RESET}", end="")
    
    print(" ", end="")


def print_captured_pieces(captured):
    white = [x for x in captured if x.get_color() == 'WHITE']
    black = [x for x in captured if x.get_color() == 'BLACK']
    print("Captured pieces:")
    
    print(f"White: {ANSI_WHITE}", end="")
    print(white)
    print(ANSI_RESET, end="")
    
    print(f"Black: {ANSI_YELLOW}", end="")
    print(black)
    print(ANSI_RESET, end="")


# Assume that ChessPiece, ChessMatch, and ChessPosition are defined elsewhere
