from abc import ABC, ABCMeta, abstractmethod
import numpy as np

class Piece:
    def __init__(self, board):
        self.board = board
        self.position = None  # A posição começa como None

    def get_board(self):
        # Método para obter o tabuleiro da peça
        return self.board

    @abstractmethod
    def possible_moves(self):
        """
        Método abstrato para calcular os movimentos possíveis.
        Cada tipo de peça deve implementar esse método.
        """
        pass

    def possible_move(self, position):
        """
        Verifica se o movimento para a posição fornecida é válido.
        :param position: Posição do destino no tabuleiro
        :return: True se o movimento for possível, False caso contrário
        """
        moves = self.possible_moves()
        # Verifica se a posição está dentro do tabuleiro e se o movimento é possível
        return moves[position.get_row()][position.get_column()]

    def is_there_any_possible_move(self):
        """
        Verifica se há qualquer movimento possível em qualquer posição no tabuleiro.
        :return: True se houver qualquer movimento possível, False caso contrário
        """
        mat = self.possible_moves()
        # Itera pela matriz de movimentos e verifica se algum movimento é válido
        for row in range(len(mat)):
            for col in range(len(mat[row])):
                if mat[row][col]:
                    return True
        return False