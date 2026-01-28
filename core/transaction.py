from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    date: date
    description: str
    amount: float
    category: str = "Sin categoría"

    # ¿Está este método escrito exactamente así? 👇
    def is_expense(self) -> bool:
        return self.amount < 0
