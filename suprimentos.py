class Suprimentos:
    def __init__ (self, nome, valor, fornecedor, estoque, validade):
        self.nome = nome
        self.valor = valor
        self.fornecedor = fornecedor
        self.estoque = estoque
        self.validade = validade 
        
    def exibir(self):
        print("-" * 30)
        print(f"Nome: {self.nome}")
        print(f"Valor: R${self.valor:.2f}")
        print(f"Fornecedor: {self.fornecedor}")
        print(f"Estoque: {self.estoque}")
        print(f"Validade: {self.validade}")
        print("-" * 30)
            