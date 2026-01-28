import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from core.parsers.bbva import bbvaParser

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Financiero Personal 💰")
        self.root.geometry("400x400")
        
        # Contenedor principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Diccionario de Parsers (Nuestro "traductor")
        # Aquí mapeamos el nombre del desplegable con la clase real
        self.parsers_disponibles = {
            "BBVA": bbvaParser,
            "CaixaBank": None  # Pendiente de implementar
        }

        # 2. Interfaz: Selección de Banco
        ttk.Label(self.main_frame, text="1. Selecciona tu banco:", font=("Arial", 10)).pack(pady=5)
        
        self.combo_bancos = ttk.Combobox(
            self.main_frame, 
            values=list(self.parsers_disponibles.keys()), 
            state="readonly"
        )
        self.combo_bancos.pack(pady=10)
        self.combo_bancos.set("Seleccionar...")

        # 3. Interfaz: Botón de Carga
        self.btn_cargar = ttk.Button(
            self.main_frame, 
            text="Cargar Extracto 📂", 
            command=self.procesar_seleccion
        )
        self.btn_cargar.pack(pady=20)

    def procesar_seleccion(self):
        """Maneja la lógica de elegir banco y buscar archivo"""
        nombre_banco = self.combo_bancos.get()
        
        # Validación: ¿Ha elegido banco?
        if nombre_banco == "Seleccionar...":
            print("⚠️ Error: Elige un banco primero")
            return

        # A. Abrimos el explorador de archivos (filedialog)
        ruta = filedialog.askopenfilename(
            title=f"Seleccionar archivo de {nombre_banco}",
            filetypes=[("Archivos CSV", "*.csv")]
        )

        if not ruta:
            print("❌ Operación cancelada")
            return

        # B. Buscamos el Parser correspondiente en nuestro diccionario
        clase_parser = self.parsers_disponibles.get(nombre_banco)

        if clase_parser is None:
            print(f"🚫 El parser para {nombre_banco} aún no está implementado.")
        else:
            instancia_parser = clase_parser()
            transacciones = instancia_parser.parse(ruta)
            # 🚀 ¡Aquí abrimos la nueva ventana!
            ResultsWindow(self.root, transacciones)

class ResultsWindow:
    def __init__(self, parent, transactions):
        self.window = tk.Toplevel(parent)
        self.window.title("Análisis de Movimientos")
        self.window.geometry("1000x600")
        
        # 1. Contenedor principal dividido en dos columnas
        self.main_pane = ttk.PanedWindow(self.window, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- PARTE IZQUIERDA: TABLA ---
        self.left_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.left_frame, weight=2)
        
        self.tree = ttk.Treeview(self.left_frame, columns=("Fecha", "Concepto", "Importe"), show='headings')
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Concepto", text="Concepto")
        self.tree.heading("Importe", text="Importe")
        
        for t in transactions:
            self.tree.insert("", tk.END, values=(t.date, t.description, f"{t.amount}€"))
        self.tree.pack(fill=tk.BOTH, expand=True)

        # --- PARTE DERECHA: GRÁFICA ---
        self.right_frame = ttk.Frame(self.main_pane)
        self.main_pane.add(self.right_frame, weight=1)
        
        self.mostrar_grafica(transactions)

        # --- PARTE INFERIOR: MENSAJE ---
        self.mostrar_resumen(transactions)

    def mostrar_grafica(self, transactions):
        gastos = abs(sum(t.amount for t in transactions if t.amount < 0))
        ingresos = sum(t.amount for t in transactions if t.amount > 0)

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie([gastos, ingresos], labels=["Gastos", "Ingresos"], 
               colors=["#ff9999", "#99ff99"], autopct='%1.1f%%')
        ax.set_title("Balance Mensual")

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def mostrar_resumen(self, transactions):
        balance_total = sum(t.amount for t in transactions)
        mensaje = "Tu situación financiera es buena ✅" if balance_total >= 0 else "Tu situación financiera es mala ⚠️"
        color = "green" if balance_total >= 0 else "red"
        
        lbl = tk.Label(self.window, text=mensaje, font=("Arial", 14, "bold"), fg=color)
        lbl.pack(side=tk.BOTTOM, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()