class Suprimento:
    def __init__(self, nome, quantidade, validade):
        self.nome = nome
        self.quantidade = quantidade
        self.validade = validade

    @classmethod
    def criar_por_input(cls):
        nome = input("Nome do Suprimento: ")
        quantidade = input("Quantidade: ")
        while not quantidade.isdigit():
            print("Quantidade deve ser numérica.")
            quantidade = input("Quantidade: ")
        validade = input("Data de validade (DD/MM/AAAA): ")
        return cls(nome, int(quantidade), validade)

    def atualizar_dados(self):
        print("Atualizar dados do suprimento (pressione Enter para manter o valor atual):")
        novo_nome = input(f"Nome atual: {self.nome}\nNovo nome: ") or self.nome
        nova_quantidade = input(f"Quantidade atual: {self.quantidade}\nNova quantidade: ") or self.quantidade
        if not str(nova_quantidade).isdigit():
            print("Quantidade inválida. Atualização cancelada.")
            return
        nova_validade = input(f"Validade atual: {self.validade}\nNova validade: ") or self.validade

        self.nome = novo_nome
        self.quantidade = int(nova_quantidade)
        self.validade = nova_validade

        print("Suprimento atualizado com sucesso!")

    def exibir(self):
        print("-" * 30)
        print(f"Nome: {self.nome} | Quantidade: {self.quantidade} | Validade: {self.validade}")

            