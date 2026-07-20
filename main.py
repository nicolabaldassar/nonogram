import tkinter as tk
from gui import NonogramGUI, center_window

def avvia_gioco(dimensione):
    # scorre la lista di tutti i figli di root e li distrugge, perché ora il contenuto della finestra deve cambiare
    for widget in root.winfo_children():
        widget.destroy()
    
    # creo un istanza di NonogramGUI dentro root
    gioco = NonogramGUI(root, size=dimensione)
    # ricentriamo la finestra date le dimensioni cambiate
    center_window(root)

def main():
    # definisco root globale eprché poi la userò anche fuori dal main, in avvia_gioco
    global root
    # ci assegno la finestra dell'applicazione
    root = tk.Tk()
    root.title("Menu Nonogramma")

    width=300
    height=400

    # calcolo la posizione in alto a sx della finestra dalle dimensioni dello schermo
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)

    # imposto posizione e dimensione
    root.geometry(f"{width}x{height}+{x}+{y}")

    tk.Label(root, text="Scegli la dimensione", font=("Arial", 14, "bold")).pack(pady=20)

    for i in range(6, 13):
        if i == 8:
            testo_bottone = f"{i}x{i} (consigliato)"
        else:
            testo_bottone = f"{i}x{i}"

        btn = tk.Button(
            root,
            text=testo_bottone,
            font=("Arial", 11),
            width=20,
            # funzione da eseguire al click, salvo il valore della i in d e poi chiamo quel valore altrimenti
            # la funzione avvia_gioco sarebbe chiamata con i = 12 per via del ciclo già finito
            command=lambda d=i: avvia_gioco(d)
        )
        # distanzia i pulsanti
        btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()