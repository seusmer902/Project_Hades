# gui/login.py
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from core import datos
from gui.dashboard import Dashboard


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 HADES WMS - Login")
        self.root.geometry("350x400")
        self.root.resizable(False, False)
        self.root.eval("tk::PlaceWindow . center")

        datos.cargar_datos_sistema()
        self.construir_interfaz()

    def construir_interfaz(self):
        marco = ttk.Frame(self.root, padding="30")
        marco.pack(expand=True, fill="both")

        ttk.Label(marco, text="🔐 INICIO DE SESIÓN", font=("Arial", 16, "bold")).pack(
            pady=(10, 30)
        )

        ttk.Label(marco, text="Usuario:").pack(anchor="w")
        self.entry_usuario = ttk.Entry(marco, font=("Arial", 12))
        self.entry_usuario.pack(fill="x", pady=(0, 20))

        ttk.Label(marco, text="Contraseña:").pack(anchor="w")
        self.entry_password = ttk.Entry(marco, font=("Arial", 12), show="*")
        self.entry_password.pack(fill="x", pady=(0, 30))

        btn_login = ttk.Button(
            marco, text="Ingresar al Sistema", command=self.validar_login
        )
        btn_login.pack(fill="x", pady=(0, 10))

        self.root.bind("<Return>", lambda event: self.validar_login())

    def validar_login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        if not usuario or not password:
            messagebox.showwarning(
                "Campos vacíos", "⚠️ Por favor, complete todos los campos."
            )
            return

        if usuario in datos.usuarios_db:
            if datos.usuarios_db[usuario].get("bloqueado"):
                messagebox.showerror("Acceso Denegado", "🚫 Su cuenta está bloqueada.")
                return

            hash_ingresado = hashlib.sha256(password.encode()).hexdigest()
            if datos.usuarios_db[usuario]["pass_hash"] == hash_ingresado:
                rol = datos.usuarios_db[usuario].get("rol", "Desconocido")

                # Cierra el login y abre el dashboard
                self.root.destroy()
                ventana_dashboard = tk.Tk()
                app_dash = Dashboard(ventana_dashboard, usuario, rol)
                ventana_dashboard.mainloop()
            else:
                messagebox.showerror("Error", "❌ Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "❌ El usuario no existe.")
