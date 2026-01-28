import csv
from datetime import datetime
from typing import List
from core.transaction import Transaction
from core.parsers.base_parser import BaseParser

class bbvaParser(BaseParser):
    def parse(self, file_path: str) -> List[Transaction]:
        transactions = []
        
        with open(file_path, mode='r', encoding='utf-8') as file:
            # 1. Buscamos la línea donde empiezan los datos reales
            # Consumimos el archivo línea a línea hasta encontrar la cabecera
            header_found = False
            for line in file:
                if "Fecha;Tarjeta;Concepto" in line:
                    header_found = True
                    break
            
            if not header_found:
                # Si recorremos todo y no hay cabecera, el archivo no es válido
                return []

            # 2. Ahora que el puntero del archivo está justo después de la cabecera,
            # leemos el resto como un CSV normal.
            # Nota: Como ya saltamos la cabecera original, definimos los nombres a mano.
            reader = csv.DictReader(
                file, 
                fieldnames=["Fecha", "Tarjeta", "Concepto", "Importe", "Divisa"], 
                delimiter=';'
            )
            
            for row in reader:
                # Ignoramos filas vacías o incompletas
                if not row["Fecha"] or not row["Importe"]:
                    continue
                
                # 3. Limpieza de datos (Tratamiento de moneda europea)
                # Cambiamos la coma decimal por un punto para que Python lo entienda
                clean_amount = row['Importe'].replace(',', '.')
                
                # 4. Creación del objeto Transaction
                t = Transaction(
                    date=datetime.strptime(row['Fecha'], '%d/%m/%Y').date(),
                    description=row['Concepto'],
                    amount=float(clean_amount)
                )
                transactions.append(t)
                
        return transactions