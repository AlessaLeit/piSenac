class Fornecedores:
    def __init__(self, nome, cnpj, produtos):
        self.nome = nome
        self.cnpj = cnpj
        self.produtos = produtos 
           
    def exibir(self):
        print("-" * 30)
        print(f"Nome: {self.nome}")
        print(f"CNPJ: {self.cnpj}")
        print(f"Produtos: {self.produtos}")
        print("-" * 30)

