import re
from pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, telefone, email, endereco, ctps, nis):
        super().__init__(nome, cpf, telefone, email, endereco)
        self.ctps = ctps
        self.nis = nis

    def atualziar_dados(self):
        super().atualizar_por_input()
        ctps = input(f"CTPS atual: {self.ctps}\nNovo CTPS (7 dígitos): ") or self.ctps
        while not ctps.isdigit() or len(ctps) != 7:
            print("CPF inválido. Atualização cancelada.")
            return
        nis = input(f"NIS atual:{self.nis}\nNovo NIS (11 dígitos): ") or self.nis
        while not nis.isdigit() or len(nis) != 11:
            print("NIS inválido. Atualização cancelada.")
            return
        
    @classmethod
    def criar_por_input(cls):
        nome = input("Nome: ")
        cpf = input("CPF (11 dígitos): ")
        while not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido! Deve conter exatamente 11 dígitos numéricos.")
            cpf = input("CPF (11 dígitos): ")
            
        telefone = input("Telefone: ")
        email = input("Email: ")
        while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Email inválido!")
            email = input("Email: ")
        
        endereco = input("Endereço: ")
        ctps = input("CTPS (7 dígitos): ")
        while not ctps.isdigit() or len(ctps) != 7:
            print("CTPS inválido! Deve conter exatamente 7 dígitos numéricos.")
            ctps = input("CTPS (7 dígitos): ")
            
        nis = input("NIS (11 dígitos): ")
        while not nis.isdigit() or len(nis) != 11:
            print("NIS inválido! Deve conter exatamente 11 dígitos numéricos.")
            nis = input("NIS (11 dígitos): ")
            
        return cls(nome, cpf, telefone, email, endereco, ctps, nis)

    def exibir(self):
        super().exibir() + print(f"| CTPS: {self.ctps} | NIS: {self.nis}")

