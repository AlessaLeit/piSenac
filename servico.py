class Servicos:
    def __init__(self, nome, valor, custo, tempoExecucao):
        self.nome = nome
        self.valor = valor
        self.custo = custo
        self.tempoExecucao = tempoExecucao
        
    def exibir(self):
        print("-" * 30)
        print(f"Nome: {self.nome}")
        print(f"Valor: R${self.valor:.2f}")
        print(f"Custo: {self.custo}")
        print(f"Tempo Execução: {self.tempoExecucao}")
        print("-" * 30)
        

            