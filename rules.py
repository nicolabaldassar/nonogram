import random

class Nonogram:
    def __init__(self, rows: int, cols: int, row_hints: list, col_hints: list):
        # settare la dimensione della griglia
        self.rows = rows
        self.cols = cols

        # valori griglia:
        # 1 = cella piena
        # 0 = cella vuota
        # -1 = cella vuota ma con la X

        # creo una griglia di zeri
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # indizi: lista di liste
        self.row_hints = row_hints
        self.col_hints = col_hints
    
    # funzione per impostare il valore di una cella
    def set_cell(self, r: int, c: int, value: int):
        if value not in [0, 1, -1]:
            raise ValueError("Valore cella non valido.")
        self.grid[r][c] = value

    # restituisce il valore della cella
    def get_cell(self, r: int, c: int):
        return self.grid[r][c]
    
    # dati dei vettori di 0 e 1 restituisce le sequenze di 1 consecutivi
    @staticmethod   # perché non dipende da un istanza della classe ma dalla classe stessa
    def extract_groups(line:list):
        groups = []
        count = 0

        # scorre colonna / riga
        for cell in line:
            if cell == 1:
                # aumenta la lunghezza dell'indizio
                count += 1
            elif count > 0:
                groups.append(count)
                count = 0
            
        if count > 0:
            groups.append(count)
        
        return groups

    # verifica se la riga r rispetta gli indizi generati
    def row_valid(self, r: int):
        return self.extract_groups(self.grid[r]) == self.row_hints[r]

    # verifica se la colonna c rispetta gli indizi generati
    def col_valid(self, c: int):
        # non ho le colonne già pronte come liste, devo crearle
        col = [self.grid[r][c] for r in range(self.rows)]
        return self.extract_groups(col) == self.col_hints[c]
    
    # controlla se tutte le righe e colonne rispettano gli indizi
    def is_solved(self):
        for r in range(self.rows):
            if self.row_valid(r) is not True:
                return False
        for c in range(self.cols):
            if self.col_valid(c) is not True:
                return False
        return True
    
    # permette di resettare la griglia
    def reset(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
