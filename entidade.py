from abc import ABC, abstractmethod

class Entidade(ABC):
    @classmethod
    @abstractmethod
    def criar_por_input(cls):
        pass

    @abstractmethod
    def exibir(self):
        pass

    @abstractmethod
    def atualizar_por_input(self):
        pass
