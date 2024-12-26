class Position:

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def get_row(self):
        return self.row

    def set_row(self, row):
        self.row = row

    def get_column(self):
        return self.column

    def set_column(self, column):
        self.column = column

    def set_values(self, row, column):
        self.row = row
        self.column = column

    def __str__(self):
        return f"{self.row}, {self.column}"
