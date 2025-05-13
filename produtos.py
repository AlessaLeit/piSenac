class Produtos:
    def __init__(self, nome, valorVenda, valorCompra, fornecedor, estoque, validade):
        self.nome = nome
        self.valorVenda = valorVenda
        self.valorCompra = valorCompra
        self.fornecedor = fornecedor
        self.estoque = estoque
        self.validade = validade
        
    def exibir(self):
        print("-" * 30)
        print(f"Nome: {self.nome}")
        print(f"Valor: R${self.valorVenda:.2f}")
        print(f"Valor Compra: R${self.valorCompra:.2f}")
        print(f"Fornecedor: {self.fornecedor}")
        print(f"Estoque: {self.estoque}")
        print(f"Validade: {self.validade}")
        print("-" * 30)
        

