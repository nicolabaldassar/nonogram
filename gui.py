import tkinter as tk
import generator
from rules import Nonogram
from tkinter import messagebox
from sat_solver import solve_nonogram

# dimensione in pixel di ogni cella
CELL_SIZE = 40

# centra la finestra e ci aggiunge dello spazio tra i bordi della finestra e la griglia
def center_window(win):
    # resetta ogni posizione e dimensione precedentemente assegnata
    win.geometry("")

    # serve per applicare la modifica precedente che potrebbe essere rimasta in una coda
    win.update_idletasks()

    # calcoliamo le nuove dimensioni della finestra in base al suo contenuto e le applichiamo
    width = win.winfo_width()
    height = win.winfo_height()

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

class NonogramGUI:
    def __init__(self, master, size=8):
        # master è quella che nel main chiamiamo root, la finestra dell'applicazione
        self.master = master
        self.size = size

        # titolo finestra
        master.title(f"Nonogramma {size}x{size}")

        self.margin = 80

        # canvas dove si disegna la griglia
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack()

        # creiamo un frame, un contenitore invisibile che conterrà i 3 pulsanti sul fondo
        self.button_frame = tk.Frame(master)
        # lo mettiamo sotto alla griglia
        self.button_frame.pack(pady=20)

        self.btn_reset = tk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset_game,
            width=10
        )
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        self.btn_gen = tk.Button(
            self.button_frame,
            text="Genera",
            command=self.start_new_level,
            width=10
        )
        self.btn_gen.pack(side = tk.LEFT, padx=10)

        self.btn_solve = tk.Button(
            self.button_frame,
            text="Risolvi",
            command=self.solve_game,
            width=10,
            fg="blue"
        )
        self.btn_solve.pack(side=tk.LEFT, padx=10)

        # genera il primo livello
        self.start_new_level()

    def start_new_level(self):
        # in self.model salviamo un oggetto Nonogram che rappresenta lo stato attusle della griglia
        self.model = generator.crea_livello_casuale(rows=self.size, cols=self.size, density=0.5)
        
        # calcola dimensioni del canvas basandosi su numero celle e margine
        w = self.model.cols * CELL_SIZE + self.margin * 2
        h = self.model.rows * CELL_SIZE + self.margin * 2

        # assegnamo le dimensioni affettive al canvas che fino ad ora era solo stato creato
        self.canvas.config(width=w, height=h)
        
        self.draw_grid()
        # colleghiamo un evento, il click sinistro del mouse, a una funzione, on_click
        self.canvas.bind("<Button-1>", self.on_click)
        
        # ricentriamo la finestra sulle nuove dimensioni del canvas
        center_window(self.master)

    # disegna la griglia e contenuto delle celle
    def draw_grid(self):
        # cancella ogni contenuto già presente, per esempio quando riavviamo la partita e dobbiamo
        # sostituire la griglia precedente 
        self.canvas.delete("all")
        
        # distanza in pixel tra un numero e l'altro
        text_step = 15
        font_conf = ("Arial", 10)

        # disegno gli indizi sopra le colonne
        for c in range(self.model.cols):
            # prendo l'indizio corrispondente alla colonna in cui mi trovo
            hint = self.model.col_hints[c]
            # se è un numero singolo, lo trasformo in lista per trattarlo uguale
            if isinstance(hint, int): 
                hint = [hint]
            
            # coordinata orizzontale in cui scrivere gli indizi, per ogni colonna
            x = (c * CELL_SIZE) + self.margin + (CELL_SIZE / 2)
            
            # ciclo al contrario, perché gli indizi vengono scritti dal basso all'alto, quindi devono essere letti dalla fine
            for i, num in enumerate(hint[::-1]):
                #calcolo della posizione verticale di ciascun indizio di ciascuna colonna
                y = self.margin - 4 - (i * text_step)
                
                # scrittura vera e propria dell'indizio
                self.canvas.create_text(
                    x, y,
                    text=str(num),
                    fill="black",
                    font=font_conf,
                    anchor="s"
                )
            
        # disegno gli indizi a sinistra delle righe
        for r in range(self.model.rows):
            # vado a prendere l'indizio corrispondente alla riga che sto trattando
            hint = self.model.row_hints[r]
            # se è un numero singolo lo trasformo in lista per lavorarci correttamente
            if isinstance(hint, int): 
                hint = [hint]

            # calcola la posizione verticale in base alla riga in cui mi trovo, sarà uguale per ogni elemento della riga
            y = (r * CELL_SIZE) + self.margin + (CELL_SIZE / 2)

            # scorro dal fondo e calcolo la posizione orizzontale dell'indizio
            for i, num in enumerate(hint[::-1]):
                x = self.margin - 8 - (i * text_step)
                
                # scrivo l'indizio
                self.canvas.create_text(
                    x, y,
                    text=str(num),
                    fill="black",
                    font=font_conf,
                    anchor="e"
                )

        # disegno le celle
        for r in range(self.model.rows):    # ciclo sulle righe
            for c in range(self.model.cols):    # ciclo sulle colonne
                # x1, y1 sono le coordinate dell'angolo in alto a sx della cella
                x1 = (c * CELL_SIZE) + self.margin
                y1 = (r * CELL_SIZE) + self.margin
                # x2, y2 sono le coordinate dell'angolo in basso a dx della cella
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                # legge il valore attuale della cella dal modello (piena, vuota, X)
                value = self.model.get_cell(r, c)

                text = ""
                text_color = ""
                
                # piena
                if value == 1:
                    fill_color = "black"
                # X
                elif value == -1:
                    fill_color = "white"
                    text = "X"
                    text_color = "red"
                # vuota
                else:
                    fill_color = "white"
                
                # disegna effettivamente la cella nella posizione calcolata e col contenuto corretto
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill = fill_color,
                    outline = "gray"
                )

                # nel caso della X, la scrivo
                if text:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=text,
                        fill=text_color,
                        font=("Arial", 20, "bold")
                    )


    # gestione click del mouse
    def on_click(self, event):  # event passa anche le coordinate del click
        
        # dalle coordinate in pixel ci calcoliamo le coordinate della cella in cui è stato fatto il click
        c = (event.x - self.margin) // CELL_SIZE
        r = (event.y - self.margin) // CELL_SIZE

        # controllo dove è stato fatto il click, se è fuori dalla griglia non faccio nulla
        if r < 0 or c < 0 or r >= self.model.rows or c >= self.model.cols:
            return
        
        # legge il valore della cella cliccata
        current = self.model.get_cell(r, c)

        # imposta il ciclo di click tale che: 0 -> 1 -> -1 -> 0
        if current == 0:
            new = 1
        elif current == 1:
            new = -1
        else:
            new = 0
        
        # aggiorna il modello con il nuovo valore
        self.model.set_cell(r, c, new)

        # ridisegna la griglia per applicare la modifica fatta
        self.draw_grid()

        # questo comando serve per colorare l'ultima cella prima del messaggio di vittoria
        # non veniva fatto sempre perché l'operazione veniva messa in una coda, cosi forziamo l'esecuzione
        self.master.update_idletasks()

        # controlliamo se il problema è risolto
        if self.model.is_solved():
            messagebox.showinfo("Complimenti!", "Puzzle risolto correttamente!")
            # Quando clicchi OK, ne genera uno nuovo
            self.start_new_level()

    # funzioni pulsanti
    def reset_game(self):
        # chiama il metodo reset in rules.py
        self.model.reset()
        # disegna la griglia vuota
        self.draw_grid()

    # collegato al pulsante "Risolvi", questo entra in gioco la parte di Z3
    def solve_game(self):
        # per far capire che sta elaborando cambiamo il cursore
        self.master.config(cursor="watch")
        # processa gli eventi in coda per evitare stati aggiornati ma con modifiche non applicate
        self.master.update()

        # passiamo i dati del modello attuale al solver
        solution = solve_nonogram(
            self.model.rows,
            self.model.cols,
            self.model.row_hints,
            self.model.col_hints
        )

        # il sat solver torna 1 se esiste soluzione, per come l'abbiamo creato esiste sempre una soluzione
        if solution:
            # avvia animazione partendo dalla cella (0,0)
            self.animate_solution(solution, 0, 0)
        else:
            # in caso non trovi la soluzione, anche se impossibile dato che generiamo i livelli su problemi risolti
            messagebox.showerror("Errore", "Z3 non ha trovato soluzioni.")

    # metodo ricorsivo
    def animate_solution(self, solution, r, c):
        # imposta nel modello il valore della cella dalla matrice solution calcolata da z3
        self.model.set_cell(r, c, solution[r][c])

        # ridisegna tutta la griglia, nonostante abbiamo cambiato una sola cella, per fare un'animazione
        # e non dare il risultato immediato
        self.draw_grid()

        # calcola prossima cella
        next_c = c + 1
        next_r = r
        if next_c >= self.model.cols:
            next_c = 0
            next_r += 1
        
        # se ci sono altre celle richiama la funzione 0.001 sec dopo
        if next_r < self.model.rows:
            self.master.after(10, lambda: self.animate_solution(solution, next_r, next_c))
        else:
            # finite le celle
            self.master.config(cursor="")
            messagebox.showinfo("Z3 Solver", "Soluzione trovata!")