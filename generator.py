import random
from rules import Nonogram

def crea_livello_casuale(rows=8, cols=8, density=0.5):
    temp_grid = []
    for r in range(rows):
        row_data = []
        for c in range(cols):
            # decide in base alla densità quanti 0 e 1 mettere
            val = 1 if random.random() < density else 0
            row_data.append(val)
        temp_grid.append(row_data) # <--- CORRETTO (era temp.grid)
    
    # calcola gli indizi in base alla griglia generata
    row_hints = []
    for r in range(rows):
        hints = Nonogram.extract_groups(temp_grid[r])
        row_hints.append(hints) # <--- CORRETTO (Mancava questa riga!)

    col_hints = []
    for c in range(cols):
        col_data = [temp_grid[r][c] for r in range(rows)]
        hints = Nonogram.extract_groups(col_data)
        col_hints.append(hints)

    # Ritorna l'oggetto Nonogram
    return Nonogram(rows, cols, row_hints, col_hints)