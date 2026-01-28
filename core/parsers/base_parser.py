from abc import ABC, abstractmethod
from typing import List 
from core.transaction import Transaction

class BaseParser(ABC):
    """ 
        Esta es la clase abstracta que define los métodos van a implementar 
        las futuras clases. Las cuales heredaran de base_parser
    """

    @abstractmethod
    def parse(self,file_path: str)-> List[Transaction]:
        """
        Esta función lee un extracto bancario y lo convierte en una lista
        de objetos Transaction
        """
        pass