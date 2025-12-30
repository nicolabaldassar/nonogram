import tkinter as tk
from gui import NonogramGUI, center_window

def avvia_gioco(dimensione):
    for widget in root.winfo_children():
        widget.destroy()
    
    gioco = NonogramGUI(root, size=dimensione)
    center_window(root)

def main():
    global root
    root = tk.Tk()
    root.title("Menu Nonogramma")

    width=300
    height=400

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)

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
            command=lambda d=i: avvia_gioco(d)
        )
        btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()