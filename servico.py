class Servico:
    def __init__(self, nome, valor, custo, tempoExe):
        self.nome = nome
        self.valor = valor
        self.custo = custo
        self.tempoExe = tempoExe
        
    @classmethod
    def criar_por_input(cls):
        nome = input("Nome: ")
        valor = input("Valor: ")
        custo = input("Custo: ")
        tempoExe = input("Tempo de Execucação: ")
        
        return cls(nome, valor, custo, tempoExe)

    def atualizar_dados(self):
        
        print("Digite os novos dados (ou pressione Enter para manter o valor atual):")
        novo_nome = input(f"Nome atual: {self.nome}\nNovo nome: ") or self.nome
        novo_valor = input(f"Valor atual: R${self.valor}\nNovo valor: ") or self.valor
        novo_custo = input(f"Custo atual: R${self.custo}\nNovo custo: ") or self.custo
        novo_tempoExe = input(f"Tempo de Execução atual: {self.tempoExe}\nNovo tempo de execução: ") or self.tempoExe

        self.nome = novo_nome
        self.valor = novo_valor
        self.custo = novo_custo
        self.tempoExe = novo_tempoExe

        print("Serviço atualizado com sucesso!")

    def exibir(self):
        print("-" * 30)
        print(f"Nome: {self.nome} | Valor: R${self.valor} | Custo: R${self.custo} | Tempo de Execução: {self.tempoExe}")

        

  