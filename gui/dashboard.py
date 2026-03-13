# gui/dashboard.py
import tkinter as tk
from tkinter import ttk
from core import datos


class Dashboard:
    def __init__(self, root, usuario, rol):
        self.root = root
        self.usuario = usuario
        self.rol = rol
        self.root.title(
            f"📦 HADES WMS - Panel Principal | Usuario: {usuario} | Rol: {rol}"
        )
        self.root.geometry("1000x600")
        self.root.eval("tk::PlaceWindow . center")

        self.construir_interfaz()

    def construir_interfaz(self):
        # --- PANEL LATERAL (MENÚ) ---
        panel_menu = tk.Frame(self.root, bg="#2C3E50", width=200)
        panel_menu.pack(side="left", fill="y")

        tk.Label(
            panel_menu,
            text="MENÚ PRINCIPAL",
            bg="#2C3E50",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(pady=20)

        btn_style = {
            "font": ("Arial", 10),
            "bg": "#34495E",
            "fg": "white",
            "width": 20,
            "pady": 8,
            "cursor": "hand2",
        }

        # AQUÍ ESTÁ EL BOTÓN CONECTADO A LA FUNCIÓN
        tk.Button(
            panel_menu,
            text="🔍 Inventario",
            **btn_style,
            command=self.mostrar_inventario,
        ).pack(pady=5)
        tk.Button(
            panel_menu,
            text="📦 Mantenimiento",
            **btn_style,
            command=self.mostrar_mantenimiento,
        ).pack(pady=5)
        tk.Button(
            panel_menu,
            text="🔄 Movimientos",
            **btn_style,
            command=self.mostrar_movimientos,
        ).pack(pady=5)
        tk.Button(
            panel_menu, text="📷 Escáner QR", **btn_style, command=self.abrir_escaner_qr
        ).pack(pady=5)
        tk.Button(
            panel_menu, text="📊 Reportes", **btn_style, command=self.mostrar_reportes
        ).pack(pady=5)

        # Botón Cerrar Sesión
        tk.Button(
            panel_menu,
            text="🚪 Cerrar Sesión",
            bg="#E74C3C",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            pady=8,
            cursor="hand2",
            command=self.cerrar_sesion,
        ).pack(side="bottom", pady=20)

        # --- ÁREA DE TRABAJO (DERECHA) ---
        self.area_trabajo = tk.Frame(self.root, bg="#ECF0F1")
        self.area_trabajo.pack(side="right", expand=True, fill="both")

        tk.Label(
            self.area_trabajo,
            text=f"¡Bienvenido a Hades WMS, {self.usuario}!",
            font=("Arial", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
        ).pack(expand=True)

    def limpiar_area_trabajo(self):
        """Destruye todo lo que haya en el panel derecho para cargar algo nuevo."""
        for widget in self.area_trabajo.winfo_children():
            widget.destroy()

    def mostrar_inventario(self):
        """Muestra la tabla con los productos de la base de datos."""
        self.limpiar_area_trabajo()

        tk.Label(
            self.area_trabajo,
            text="📦 CONSULTA DE INVENTARIO",
            font=("Arial", 18, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
        ).pack(pady=20)

        frame_tabla = tk.Frame(self.area_trabajo, bg="#ECF0F1")
        frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        columnas = ("Codigo", "Nombre", "Marca", "Categoria", "Stock")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

        tabla.heading("Codigo", text="CÓDIGO")
        tabla.heading("Nombre", text="NOMBRE DEL PRODUCTO")
        tabla.heading("Marca", text="MARCA")
        tabla.heading("Categoria", text="CATEGORÍA")
        tabla.heading("Stock", text="STOCK")

        tabla.column("Codigo", width=100, anchor="center")
        tabla.column("Nombre", width=250, anchor="w")
        tabla.column("Marca", width=120, anchor="center")
        tabla.column("Categoria", width=120, anchor="center")
        tabla.column("Stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        tabla.pack(side="left", fill="both", expand=True)

        # Cargar los datos a la tabla
        for codigo, prod in datos.inventario_db.items():
            alerta = " ⚠️" if prod["stock"] <= prod.get("stock_minimo", 5) else ""
            tabla.insert(
                "",
                "end",
                values=(
                    codigo,
                    prod["nombre"],
                    prod.get("marca", "N/A"),
                    prod.get("categoria", "N/A"),
                    f"{prod['stock']}{alerta}",
                ),
            )

    def mostrar_mantenimiento(self):
        """Muestra el formulario para registrar un nuevo producto."""
        self.limpiar_area_trabajo()

        tk.Label(
            self.area_trabajo,
            text="📦 REGISTRO DE PRODUCTOS",
            font=("Arial", 18, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
        ).pack(pady=20)

        # Contenedor del formulario
        marco_form = tk.Frame(self.area_trabajo, bg="#ECF0F1")
        marco_form.pack(pady=10)

        # Diccionario para guardar las referencias a las cajas de texto
        self.entradas_mantenimiento = {}
        campos = [
            "Código (ej. PAP-022):",
            "Nombre:",
            "Marca:",
            "Categoría:",
            "Stock Inicial:",
            "Stock Mínimo:",
        ]

        # Crear las etiquetas y cajas de texto dinámicamente
        for i, campo in enumerate(campos):
            tk.Label(
                marco_form,
                text=campo,
                font=("Arial", 12, "bold"),
                bg="#ECF0F1",
                fg="#34495E",
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entrada = ttk.Entry(marco_form, font=("Arial", 12), width=35)
            entrada.grid(row=i, column=1, padx=10, pady=10)
            self.entradas_mantenimiento[campo] = entrada

        # Botón para guardar
        btn_guardar = tk.Button(
            self.area_trabajo,
            text="💾 Guardar Producto",
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            cursor="hand2",
            width=20,
            command=self.guardar_nuevo_producto,
        )
        btn_guardar.pack(pady=30)

    def guardar_nuevo_producto(self):
        """Valida y guarda los datos ingresados en el formulario."""
        from tkinter import messagebox
        from core import datos

        # Extraer los textos de las cajas
        codigo = (
            self.entradas_mantenimiento["Código (ej. PAP-022):"].get().strip().upper()
        )
        nombre = self.entradas_mantenimiento["Nombre:"].get().strip()
        marca = self.entradas_mantenimiento["Marca:"].get().strip()
        categoria = self.entradas_mantenimiento["Categoría:"].get().strip()
        stock_str = self.entradas_mantenimiento["Stock Inicial:"].get().strip()
        stock_min_str = self.entradas_mantenimiento["Stock Mínimo:"].get().strip()

        # Validaciones de seguridad
        if not codigo or not nombre or not stock_str or not stock_min_str:
            messagebox.showwarning(
                "Campos incompletos",
                "⚠️ Por favor, llene los campos obligatorios (Código, Nombre, Stock).",
            )
            return

        if codigo in datos.inventario_db:
            messagebox.showerror(
                "Error", f"❌ El código '{codigo}' ya existe en el inventario."
            )
            return

        try:
            stock = int(stock_str)
            stock_min = int(stock_min_str)
            if stock < 0 or stock_min < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error",
                "❌ El stock y stock mínimo deben ser números enteros positivos.",
            )
            return

        # Guardar en la "memoria" y en el archivo JSON
        datos.inventario_db[codigo] = {
            "nombre": nombre,
            "categoria": categoria,
            "marca": marca,
            "stock": stock,
            "stock_minimo": stock_min,
        }
        datos.guardar_inventario()

        # Generar QR automáticamente (reutilizando la función del domingo)
        try:
            from core.utils import generar_qr_producto

            info = f"ID: {codigo}\nNombre: {nombre}\nMarca: {marca}\nCat: {categoria}"
            generar_qr_producto(codigo, info)
        except ImportError:
            pass  # Si falla la importación del QR, al menos guarda el producto

        messagebox.showinfo("Éxito", f"✅ Producto '{nombre}' guardado correctamente.")

        # Limpiar las cajas de texto después de guardar
        for entrada in self.entradas_mantenimiento.values():
            entrada.delete(0, tk.END)

    def mostrar_movimientos(self):
        """Muestra la interfaz para registrar Entradas y Salidas."""
        self.limpiar_area_trabajo()

        tk.Label(
            self.area_trabajo,
            text="🔄 REGISTRO DE MOVIMIENTOS",
            font=("Arial", 18, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
        ).pack(pady=20)

        marco_mov = tk.Frame(self.area_trabajo, bg="#ECF0F1")
        marco_mov.pack(pady=10)

        # Diccionario para capturar los datos
        self.entradas_mov = {}

        # Código del Producto
        tk.Label(
            marco_mov,
            text="Código del Producto:",
            font=("Arial", 12, "bold"),
            bg="#ECF0F1",
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entradas_mov["codigo"] = ttk.Entry(marco_mov, font=("Arial", 12), width=20)
        self.entradas_mov["codigo"].grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Tipo de Movimiento (Desplegable)
        tk.Label(
            marco_mov,
            text="Tipo de Movimiento:",
            font=("Arial", 12, "bold"),
            bg="#ECF0F1",
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entradas_mov["tipo"] = ttk.Combobox(
            marco_mov,
            values=["ENTRADA", "SALIDA"],
            font=("Arial", 12),
            state="readonly",
            width=18,
        )
        self.entradas_mov["tipo"].current(0)  # Selecciona "ENTRADA" por defecto
        self.entradas_mov["tipo"].grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Cantidad
        tk.Label(
            marco_mov, text="Cantidad:", font=("Arial", 12, "bold"), bg="#ECF0F1"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entradas_mov["cantidad"] = ttk.Entry(
            marco_mov, font=("Arial", 12), width=20
        )
        self.entradas_mov["cantidad"].grid(
            row=2, column=1, padx=10, pady=10, sticky="w"
        )

        # Motivo
        tk.Label(
            marco_mov, text="Motivo/Detalle:", font=("Arial", 12, "bold"), bg="#ECF0F1"
        ).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entradas_mov["motivo"] = ttk.Entry(marco_mov, font=("Arial", 12), width=35)
        self.entradas_mov["motivo"].grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Botón de Procesar
        btn_procesar = tk.Button(
            self.area_trabajo,
            text="⚡ Procesar Movimiento",
            font=("Arial", 12, "bold"),
            bg="#E67E22",
            fg="white",
            cursor="hand2",
            width=25,
            command=self.procesar_movimiento,
        )
        btn_procesar.pack(pady=30)

    def abrir_escaner_qr(self):
        """Abre la cámara, lee el QR y pre-llena el formulario de movimientos."""
        self.limpiar_area_trabajo()

        tk.Label(
            self.area_trabajo,
            text="📷 ESCÁNER DE CÓDIGOS QR",
            font=("Arial", 18, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
        ).pack(pady=20)
        tk.Label(
            self.area_trabajo,
            text="Abriendo cámara... Por favor enfoque el código QR.",
            font=("Arial", 12),
            bg="#ECF0F1",
        ).pack(pady=10)
        tk.Label(
            self.area_trabajo,
            text="(Presione la tecla 'Q' en la ventana de la cámara para cancelar)",
            font=("Arial", 10, "italic"),
            bg="#ECF0F1",
        ).pack()

        # Actualizamos la interfaz antes de que la cámara pause el programa
        self.root.update()

        import cv2
        from pyzbar.pyzbar import decode
        from tkinter import messagebox
        from core import datos

        cap = cv2.VideoCapture(0)
        codigo_detectado = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Buscar códigos en la imagen de la cámara
            for code in decode(frame):
                contenido = code.data.decode("utf-8")
                if "ID: " in contenido:
                    codigo_detectado = (
                        contenido.split("\n")[0].replace("ID: ", "").strip()
                    )
                    break

            cv2.imshow("HADES WMS - Escáner Gráfico", frame)

            # Se cierra si detecta el código o si presionas 'q'
            if codigo_detectado or cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        # ¿Qué hacemos si encontramos un código?
        if codigo_detectado:
            if codigo_detectado in datos.inventario_db:
                prod = datos.inventario_db[codigo_detectado]
                messagebox.showinfo(
                    "QR Detectado",
                    f"✅ Producto encontrado:\n{prod['nombre']}\nStock actual: {prod['stock']}\n\nSe abrirá el panel de Movimientos.",
                )

                # Magia: Te mandamos a la pantalla de movimientos y escribimos el código por ti
                self.mostrar_movimientos()
                self.entradas_mov["codigo"].insert(0, codigo_detectado)
            else:
                messagebox.showerror(
                    "Error",
                    f"❌ El código '{codigo_detectado}' leído en el QR no existe en el sistema.",
                )
                self.mostrar_inventario()
        else:
            messagebox.showinfo("Cancelado", "⚠️ Escaneo cancelado por el usuario.")
            self.mostrar_inventario()

    def procesar_movimiento(self):
        """Valida matemáticamente y guarda el movimiento de stock."""
        from tkinter import messagebox
        from core import datos
        from datetime import datetime

        codigo = self.entradas_mov["codigo"].get().strip().upper()
        tipo = self.entradas_mov["tipo"].get()
        cant_str = self.entradas_mov["cantidad"].get().strip()
        motivo = self.entradas_mov["motivo"].get().strip() or "No especificado"

        if not codigo or not cant_str:
            messagebox.showwarning("Faltan Datos", "⚠️ Ingrese el código y la cantidad.")
            return

        if codigo not in datos.inventario_db:
            messagebox.showerror("Error", f"❌ El producto '{codigo}' no existe.")
            return

        try:
            cant = int(cant_str)
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "❌ La cantidad debe ser un número entero mayor a cero."
            )
            return

        prod = datos.inventario_db[codigo]

        # Validar lógica de Salidas (No stock negativo)
        if tipo == "SALIDA" and cant > prod["stock"]:
            messagebox.showerror(
                "Stock Insuficiente",
                f"❌ No puede retirar {cant} unidades.\nSolo hay {prod['stock']} disponibles de {prod['nombre']}.",
            )
            return

        # Aplicar la matemática
        if tipo == "ENTRADA":
            prod["stock"] += cant
        else:
            prod["stock"] -= cant

        # Guardar en JSON de Inventario
        datos.guardar_inventario()

        # Registrar en el Historial (Kardex)
        nuevo_movimiento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "codigo_prod": codigo,
            "cantidad": cant,
            "usuario": self.usuario,
            "motivo": motivo,
        }
        datos.movimientos_db.append(nuevo_movimiento)
        datos.guardar_movimientos()

        messagebox.showinfo(
            "Éxito",
            f"✅ Movimiento registrado.\nNuevo stock de '{prod['nombre']}': {prod['stock']}",
        )

        # Limpiar campos
        self.entradas_mov["codigo"].delete(0, tk.END)
        self.entradas_mov["cantidad"].delete(0, tk.END)
        self.entradas_mov["motivo"].delete(0, tk.END)

    def mostrar_reportes(self):
        """Muestra la tabla del historial de movimientos (Kardex)."""
        self.limpiar_area_trabajo()

        tk.Label(
            self.area_trabajo,
            text="📊 HISTORIAL DE MOVIMIENTOS",
            font=("Arial", 18, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
        ).pack(pady=20)

        # Contenedor de la tabla
        frame_tabla = tk.Frame(self.area_trabajo, bg="#ECF0F1")
        frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear la tabla
        columnas = ("Fecha", "Tipo", "Codigo", "Cantidad", "Usuario")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

        # Encabezados
        tabla.heading("Fecha", text="FECHA Y HORA")
        tabla.heading("Tipo", text="TIPO")
        tabla.heading("Codigo", text="PRODUCTO")
        tabla.heading("Cantidad", text="CANTIDAD")
        tabla.heading("Usuario", text="USUARIO")

        # Tamaños
        tabla.column("Fecha", width=160, anchor="center")
        tabla.column("Tipo", width=100, anchor="center")
        tabla.column("Codigo", width=120, anchor="center")
        tabla.column("Cantidad", width=80, anchor="center")
        tabla.column("Usuario", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        tabla.pack(side="left", fill="both", expand=True)

        # Cargar los datos desde el historial (Cerebro)
        from core import datos

        # Usamos reversed() para que los movimientos más nuevos salgan arriba
        for mov in reversed(datos.movimientos_db):
            tabla.insert(
                "",
                "end",
                values=(
                    mov.get("fecha", "N/A"),
                    mov.get("tipo", "N/A"),
                    mov.get("codigo_prod", "N/A"),
                    mov.get("cantidad", 0),
                    mov.get("usuario", "N/A"),
                ),
            )

    def cerrar_sesion(self):
        self.root.destroy()
        from gui.login import LoginWindow

        ventana_login = tk.Tk()
        app = LoginWindow(ventana_login)
        ventana_login.mainloop()
