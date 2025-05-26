import re
from models.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, telefone, email, endereco, ctps, nis):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.ctps = ctps
        self.nis = nis

    def atualizar_dados(self):
        print("Digite os novos dados (ou pressione Enter para manter o valor atual):")
        novo_nome = input(f"Nome atual: {self.nome}\nNovo nome: ") or self.nome
        novo_cpf = input(f"CPF atual: {self.cpf}\nNovo CPF (11 dígitos): ") or self.cpf
        if not novo_cpf.isdigit() or len(novo_cpf) != 11:
            print("CPF inválido. Atualização cancelada.")
            return

        novo_telefone = input(f"Telefone atual: {self.telefone}\nNovo telefone: ") or self.telefone
        novo_email = input(f"Email atual: {self.email}\nNovo email: ") or self.email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
            print("Email inválido. Atualização cancelada.")
            return

        novo_endereco = input(f"Endereço atual: {self.endereco}\nNovo endereço: ") or self.endereco
        novo_ctps = input(f"CTPS atual: {self.ctps}\nNovo CTPS (7 dígitos): ") or self.ctps
        while not novo_ctps.isdigit() or len(novo_ctps) != 7:
            print("CPF inválido. Atualização cancelada.")
            return
        novo_nis = input(f"NIS atual:{self.nis}\nNovo NIS (11 dígitos): ") or self.nis
        while not novo_nis.isdigit() or len(novo_nis) != 11:
            print("NIS inválido. Atualização cancelada.")
            return
        
        self.nome = novo_nome
        self.cpf = novo_cpf
        self.telefone = novo_telefone
        self.email = novo_email
        self.endereco = novo_endereco
        
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
        print("-" * 30)
        print(f"Nome: {self.nome} | CPF: {self.cpf} | Telefone: {self.telefone} | Email: {self.email} | Endereço: {self.endereco} | CTPS: {self.ctps} | NIS: {self.nis}")

