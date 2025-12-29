class Nonogram:
    def __init__(self, rows: int, cols: int, row_hints: list, col_hints: list):
        # settare la dimensione della griglia
        self.rows = rows
        self.cols = cols

        # valori griglia:
        # None = non deciso
        # 1 = cella piena
        # 0 = cella vuota
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # indizi: lista di liste
        self.row_hints = row_hints
        self.col_hints = col_hints
    
    # funzione per impostare il valore di una cella
    def set_cell(self, r: int, c: int, value: int) -> None:
        if value not in (0, 1):
            raise ValueError("Valore cella non valido.")
        self.grid[r][c] = value

    # restituisce il valore della cella
    def get_cell(self, r: int, c: int):
        return self.grid[r][c]
    
    # dati dei vettori di 0 e 1 restituisce le sequenze di 1 consecutivi
    def extract_groups(self, line:list) -> list:
        groups = []
        count = 0

        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                groups.append(count)
                count = 0
            
        if count > 0:
            groups.append(count)
        
        return groups

    # verifica se la riga r rispetta gli indizi, ritorna True, False o None se ci sono delle celle None
    def row_valid(self, r: int) -> bool | None:
        extracted = self.extract_groups(self.grid[r])
        if extracted is None:
            return None
        return extracted == self.row_hints[r]
    
    def col_valid(self, c: int) -> bool | None:
        col = [self.grid[r][c] for r in range(self.rows)]
        extracted = self.extract_groups(col)
        if extracted is None:
            return None
        return extracted == self.col_hints(c)
    
    # controlla se tutte le righe e colonne rispetto gli indizi
    def is_solved(self) -> bool:
        for r in range(self.rows):
            if self.row_valid(r) is not True:
                return False
        for c in range(self.cols):
            if self.col_valid(c) is not True:
                return False
        return True
    