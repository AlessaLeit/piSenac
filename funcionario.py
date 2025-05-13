from pi.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, telefone, email, endereco, ctps, nis):
        super().__init__(nome, cpf, telefone, email, endereco)
        self.ctps = ctps
        self.nis = nis

    def exibir(self):
        super().exibir()
        print(f"CTPS: {self.ctps}")
        print(f"NIS: {self.nis}")
        print("-" * 30)

    def atualizar_por_input(self):
        super().atualizar_por_input()
        self.ctps = input(f"CTPS [{self.ctps}]: ") or self.ctps
        self.nis = input(f"NIS [{self.nis}]: ") or self.nis

    @classmethod
    def criar_por_input(cls):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        telefone = input("Telefone: ")
        email = input("Email: ")
        endereco = input("Endereço: ")
        ctps = input("CTPS: ")
        nis = input("NIS: ")
        return cls(nome, cpf, telefone, email, endereco, ctps, nis)

