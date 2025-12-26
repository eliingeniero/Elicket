import tkinter as tk
import os
import inicio

def main():
    root = tk.Tk()
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "eliicoptero.ico"))
    root.title("Élicket")
    root.geometry("800x600")

    inicio.abrir_inicio(root)

    root.mainloop()

if __name__ == "__main__":
    main()
