# Nonogramma (Picross) in Python

## Descrizione del progetto

Questo progetto è stato sviluppato come lavoro per il corso di **Computabilità, Complessità e Logica** (2° anno, corso di laurea AIDA).

Si tratta di un'implementazione del gioco del **Nonogramma** (noto anche come *Picross* o *Griddler*), un puzzle logico in cui il giocatore deve colorare le celle di una griglia seguendo gli indizi numerici posti a lato di ogni riga e colonna, fino a formare un'immagine.

Il progetto integra tre componenti principali:

- **Interfaccia grafica** realizzata con `tkinter`, che permette di giocare cliccando sulle celle della griglia (click sinistro per ciclare tra cella piena, cella con "X" e cella vuota).
- **Generatore di livelli casuali**, che crea griglie di gioco casuali e ne calcola automaticamente gli indizi corrispondenti.
- **Risolutore automatico basato su Z3**, un SAT/SMT solver, che modella il puzzle come un problema di soddisfacibilità di vincoli (constraint satisfaction) e trova una soluzione valida, mostrata poi tramite un'animazione cella per cella.

## Come si usa

1. Avvia il programma eseguendo `main.py`.
2. Dal menu iniziale scegli la dimensione della griglia (da 6x6 a 12x12).
3. Gioca cliccando sulle celle:
   - primo click: cella piena (nera)
   - secondo click: cella marcata con una "X" (cella sicuramente vuota)
   - terzo click: cella vuota
4. Usa i pulsanti in basso per:
   - **Reset**: svuota la griglia corrente mantenendo gli stessi indizi
   - **Genera**: crea un nuovo livello casuale
   - **Risolvi**: richiama il solver Z3 e mostra la soluzione con un'animazione
5. Quando la griglia rispetta tutti gli indizi, viene mostrato un messaggio di vittoria e viene generato automaticamente un nuovo livello.

## Dipendenze da installare

Oltre a Python, il progetto richiede:

- **z3-solver**: libreria per la risoluzione di vincoli logici usata dal modulo `sat_solver.py`.
```bash
  pip install z3-solver
```

- **tkinter**: libreria per l'interfaccia grafica. Su Windows e macOS è generalmente già inclusa nell'installazione standard di Python. Su alcune distribuzioni Linux va installata separatamente, ad esempio su Ubuntu/Debian:
```bash
  sudo apt-get install python3-tk
```