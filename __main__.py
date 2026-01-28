import tkinter as tk
from ui.main_window import MainWindow
from core.parsers.bbva import bbvaParser



# def test_run():
#     parser = bbvaParser()
#     file_path = "data/extracto_bancario_bbva.csv"

#     try:
#             # 3. Procesamos los datos
#             transactions = parser.parse(file_path)
            
#             # 4. Mostramos resultados
#             print(f"✅ Se han procesado {len(transactions)} transacciones.\n")
#             for t in transactions:
#                 tipo = "Gasto 🔻" if t.is_expense() else "Ingreso 🔹"
#                 print(f"{t.date} | {tipo} | {t.amount}€ | {t.description}")
                
#     except Exception as e:
#             print(f"❌ Error al procesar el archivo: {e}")

def main():
    # 1. Creamos la base de la interfaz gráfica 🖼️
    root = tk.Tk()
    
    # 2. Inicializamos nuestra ventana principal 🏗️
    # Al pasarle 'root', le decimos a MainWindow dónde debe dibujarse
    app = MainWindow(root)
    
    # 3. Mantenemos la aplicación abierta 🔄
    # Sin esto, la ventana se abriría y cerraría en un milisegundo
    root.mainloop()

if __name__ == "__main__":
        main()
