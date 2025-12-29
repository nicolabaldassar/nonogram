import tkinter as tk
from rules import Nonogram

# dimensione in pixel di ogni cella
CELL_SIZE = 40

# centra la finestra e aggiungici dello spazio tra i bordi della finestra e la griglia
def center_window(win):
    win.update_idletasks()

    width = win.winfo_width()
    height = win.winfo_height()

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()

    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

class NonogramGUI:
    def __init__(self, master, model: Nonogram):
        self.master = master
        self.model = model

        # titolo finestra
        master.title("Nonogram")

        self.margin = 40

        # canvas dove si disegna la griglia
        self.canvas = tk.Canvas(
            master,
            width = model.cols * CELL_SIZE + self.margin * 2,
            height = model.rows * CELL_SIZE + self.margin * 2,
            bg = "white"
        )
        self.canvas.pack()

        # disegna la griglia
        self.draw_grid()

        # aggiunge l'evento click sulle celle
        self.canvas.bind("<Button-1>", self.on_click)

    # disegna la griglia e contenuto delle celle
    def draw_grid(self):
        self.canvas.delete("all")

        for r in range(self.model.rows):
            for c in range(self.model.cols):
                x1 = (c * CELL_SIZE) + self.margin
                y1 = (r * CELL_SIZE) + self.margin
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                value = self.model.get_cell(r, c)

                # imposta lo sfondo della cella in base allo stato
                if value == 1:
                    color = "black"
                else:
                    color = "white"
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill = color,
                    outline = "gray"
                )

    # gestione click del mouse
    def on_click(self, event):
        c = (event.x - self.margin) // CELL_SIZE
        r = (event.y - self.margin) // CELL_SIZE

        if r < 0 or c < 0 or r >= self.model.rows or c >= self.model.cols:
            return
        
        current = self.model.get_cell(r, c)

        # imposta il ciclo di click tale che: None -> Pieno -> Vuoto -> None
        if current == 0:
            new = 1
        else:
            new = 0
        
        self.model.set_cell(r, c, new)

        # ridisegna la cella
        self.draw_grid()




if __name__ == "__main__":
    model = Nonogram(
        8, 8,
        row_hints=[[1], 3, [1,1], [5], [2], [1], 3, [1,1]],
        col_hints=[[2], [2], [1, 1], [3], [1], [1], 3, [1,1]]
    )
    root = tk.Tk()
    gui = NonogramGUI(root, model)
    
    center_window(root)

    root.mainloop()