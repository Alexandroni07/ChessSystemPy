from chess import ChessMatch
from chess import ChessException
from interface import Interface
import sys
import os

# Adicionando o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




def main():
    chess_match = ChessMatch()
    captured = []
    
    while not chess_match.get_check_mate():
        try:
            Interface.clear_screen()
            Interface.print_match(chess_match, captured)
            print()
            print("Source: ")
            source = Interface.read_chess_position()
            
            possible_moves = chess_match.possible_moves(source)
            Interface.clear_screen()
            Interface.print_board(chess_match.get_pieces(), possible_moves)
            
            print()
            print("Target: ")
            target = Interface.read_chess_position()
            
            captured_piece = chess_match.perform_chess_move(source, target)
            
            if captured_piece is not None:
                captured.append(captured_piece)
            
            if chess_match.get_promoted() is not None:
                type = input("Enter piece for promotion (B/N/R/Q): ").upper()
                while type not in ['B', 'N', 'R', 'Q']:
                    type = input("Invalid value. Enter piece for promotion (B/N/R/Q): ").upper()
                chess_match.replace_promoted_piece(type)
        
        except ChessException as e:
            print(e.message)
            input()
        
        except ValueError as e:
            print(str(e))
            input()
    
    Interface.clear_screen()
    Interface.print_match(chess_match, captured)

if __name__ == "__main__":
    main()
