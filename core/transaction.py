from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction: 
    "Esta clase representa un único movimiento bancario"
    date: date  #Fecha de la operación 
    description: str # Concepto o descripción del banco
    amount : float # Cantidad(Positivo: Ingreso, Negativo: Gasto)
    category: str = "Sin categoria" #Valor por defecto

def is_expensive(self) -> bool:
    return self.amount<0
