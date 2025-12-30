import tkinter as tk
import generator
from rules import Nonogram
from tkinter import messagebox
from sat_solver import solve_nonogram

# dimensione in pixel di ogni cella
CELL_SIZE = 40

# centra la finestra e aggiungici dello spazio tra i bordi della finestra e la griglia
def center_window(win):
    win.geometry("")

    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

class NonogramGUI:
    def __init__(self, master, size=8):
        self.master = master
        self.size = size

        # titolo finestra
        master.title(f"Nonogramma {size}x{size}")

        self.margin = 80

        # canvas dove si disegna la griglia
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=20)

        # pulsanti
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

        # genera il primo livello all'apertura del programma
        self.start_new_level()

    def start_new_level(self):
        self.model = generator.crea_livello_casuale(rows=self.size, cols=self.size, density=0.5)
        
        w = self.model.cols * CELL_SIZE + self.margin * 2
        h = self.model.rows * CELL_SIZE + self.margin * 2

        self.canvas.config(width=w, height=h)
        
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        
        center_window(self.master)

    # disegna la griglia e contenuto delle celle
    def draw_grid(self):
        self.canvas.delete("all")
        
        # distanza in pixel tra un numero e l'altro
        text_step = 15
        font_conf = ("Arial", 10)

        # disegno gli indizi sopra le colonne
        for c in range(self.model.cols):
            hint = self.model.col_hints[c]
            # se è un numero singolo, lo trasformo in lista per trattarlo uguale
            if isinstance(hint, int): 
                hint = [hint]
            
            x = (c * CELL_SIZE) + self.margin + (CELL_SIZE / 2)
            
            # ciclo al contrario 
            for i, num in enumerate(hint[::-1]):
                y = self.margin - 4 - (i * text_step)
                
                self.canvas.create_text(
                    x, y,
                    text=str(num),
                    fill="black",
                    font=font_conf,
                    anchor="s"
                )
            
        # disegno gli indizi a sinistra delle righe
        for r in range(self.model.rows):
            hint = self.model.row_hints[r]
            if isinstance(hint, int): 
                hint = [hint]

            y = (r * CELL_SIZE) + self.margin + (CELL_SIZE / 2)

            for i, num in enumerate(hint[::-1]):
                x = self.margin - 8 - (i * text_step)
                
                self.canvas.create_text(
                    x, y,
                    text=str(num),
                    fill="black",
                    font=font_conf,
                    anchor="e"
                )

        # disegno la griglia
        for r in range(self.model.rows):
            for c in range(self.model.cols):
                x1 = (c * CELL_SIZE) + self.margin
                y1 = (r * CELL_SIZE) + self.margin
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                value = self.model.get_cell(r, c)

                text = ""
                text_color = ""

                if value == 1:
                    fill_color = "black"
                elif value == -1:
                    fill_color = "white"
                    text = "X"
                    text_color = "red"
                else:
                    fill_color = "white"
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill = fill_color,
                    outline = "gray"
                )

                if text:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=text,
                        fill=text_color,
                        font=("Arial", 20, "bold")
                    )


    # gestione click del mouse
    def on_click(self, event):
        c = (event.x - self.margin) // CELL_SIZE
        r = (event.y - self.margin) // CELL_SIZE

        if r < 0 or c < 0 or r >= self.model.rows or c >= self.model.cols:
            return
        
        current = self.model.get_cell(r, c)

        # imposta il ciclo di click tale che: 0 -> 1 -> -1 -> 0
        if current == 0:
            new = 1
        elif current == 1:
            new = -1
        else:
            new = 0
        
        self.model.set_cell(r, c, new)

        # ridisegna la cella
        self.draw_grid()

        # questo comando serve per colorare l'ultima cella prima del messaggio di vittoria
        self.master.update_idletasks()

        if self.model.is_solved():
            messagebox.showinfo("Complimenti!", "Puzzle risolto correttamente!")
            # Quando clicchi OK, ne genera uno nuovo
            self.start_new_level()

    # funzioni pulsanti
    def reset_game(self):
        self.model.reset()
        self.draw_grid()

    def solve_game(self):
        # per far capire che sta elaborando cambiamo il cursore
        self.master.config(cursor="watch")
        self.master.update()

        # passiamo i dati del modello attuale al solver
        solution = solve_nonogram(
            self.model.rows,
            self.model.cols,
            self.model.row_hints,
            self.model.col_hints
        )

        # ripristiniamo ora il cursore normale
        self.master.config(cursor="")

        if solution:
            # se c'è una soluzione mettiamo i valori nella griglia
            for r in range(self.model.rows):
                for c in range(self.model.cols):
                    self.model.set_cell(r, c, solution[r][c])
            
            # ridisegniamo
            self.draw_grid()
            messagebox.showinfo("Z3 Solver", "Soluzione trovata!")
        else:
            # in caso non trovi la soluzione, anche se impossibile dato che generiamo i livelli
            messagebox.showerror("Errore", "Z3 non ha trovato soluzioni.")