import z3

# input: dimensioni e indizi
# output: matrice di 0 e 1 se risolto, None se impossibile
def solve_nonogram(rows, cols, row_hints, col_hints):
    # crea il solver
    s = z3.Solver()

    # creiamo una matrice di variabili intere z3, una per cella
    grid_vars = [[z3.Int(f"cell_{r}_{c}") for c in range(cols)] for r in range(rows)]

    # vincolo base: ogni cella può valere solo 0 oppure 1
    for r in range(rows):
        for c in range(cols):
            s.add(z3.Or(grid_vars[r][c] == 0, grid_vars[r][c] == 1))
    
    # funzione che costruisce i vincoli
    # collega gli indizi alle variabili della griglia
    def add_line_constraint(line_vars, hints, length, name_prefix):
        # se non ci sono hints o se è 0, allora la riga è vuota
        if not hints or hints == [0]:
            for v in line_vars:
                s.add(v == 0)
            return

        # creiamo variabili per la posizione di inizio di ogni blocco
        positions = [z3.Int(f"pos_{name_prefix}_{i}") for i in range(len(hints))]

        # vincoli di ordine e spazio
        # il primo blocco deve iniziare dentro la riga
        s.add(positions[0] >= 0)

        for i in range(len(positions) - 1):
            # il blocco seguente deve iniziare dopo la fine di quello attuale
            s.add(positions[i+1] >= positions[i] + hints[i] + 1)
        
        # l'ultimo blocco non deve uscire dalla riga
        s.add(positions[-1] + hints[-1] <= length)

        # una cella è nera se cade dentro uno dei blocchi, altrimenti è bianca
        for i in range(length):
            # la cella i è dentro il blocco x?
            conditions = []
            for block_idx, start_pos_var in enumerate(positions):
                block_len = hints[block_idx]
                conditions.append(z3.And(i >= start_pos_var, i < start_pos_var + block_len))

            # se almeno una condizione è vera, la cella vale 1 altrimenti 0
            s.add(line_vars[i] == z3.If(z3.Or(conditions), 1, 0))

    # applicazione dei vincoli
    # applicazione dei vincoli alle righe
    for r in range(rows):
        add_line_constraint(grid_vars[r], row_hints[r], cols, f"row_{r}")

    # applicazione dei vincoli alle colonne
    for c in range(cols):
        col_vars = [grid_vars[r][c] for r in range(rows)]
        add_line_constraint(col_vars, col_hints[c], rows, f"col_{c}")

    
    # risoluzione
    # chiediamo a z3 se esiste una soluzione
    result = s.check()

    if result == z3.sat:
        # se esiste la soluzione
        m = s.model()
        solution = []
        for r in range(rows):
            row_sol = []
            for c in range(cols):
                # m.evaluate calcolare il valore finale della variabile
                val = m.evaluate(grid_vars[r][c]).as_long()
                row_sol.append(val)
            solution.append(row_sol)
        return solution
    else:
        return None