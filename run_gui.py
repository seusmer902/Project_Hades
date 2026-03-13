# run_gui.py
import tkinter as tk
from gui.login import LoginWindow

if __name__ == "__main__":
    # Arrancar el motor gráfico
    ventana_principal = tk.Tk()
    app = LoginWindow(ventana_principal)
    ventana_principal.mainloop()
