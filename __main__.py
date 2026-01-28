from core.parsers.bbva import bbvaParser



def test_run():
    parser = bbvaParser()
    file_path = "data/extracto_bancario_bbva.csv"

    try:
            # 3. Procesamos los datos
            transactions = parser.parse(file_path)
            
            # 4. Mostramos resultados
            print(f"✅ Se han procesado {len(transactions)} transacciones.\n")
            for t in transactions:
                tipo = "Gasto 🔻" if t.is_expense() else "Ingreso 🔹"
                print(f"{t.date} | {tipo} | {t.amount}€ | {t.description}")
                
    except Exception as e:
            print(f"❌ Error al procesar el archivo: {e}")

if __name__ == "__main__":
        test_run()
