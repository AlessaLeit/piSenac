from entidade import Entidade

class Pessoa(Entidade):
    def __init__(self, nome, cpf, telefone, email, endereco):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        
    def atualizar_por_input(self):
        self.nome = input(f"Nome [{self.nome}]: ") or self.nome
        self.telefone = input(f"Telefone [{self.telefone}]: ") or self.telefone
        self.email = input(f"Email [{self.email}]: ") or self.email
        self.endereco = input(f"Endereço [{self.endereco}]: ") or self.endereco
