class BoardException(Exception):
    pass

class ChessException(BoardException):
    def __init__(self, msg):
        super().__init__(msg)
