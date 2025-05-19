class Produto:      
    def __init__(self, nome, valorVenda, valorCompra, fornecedor, estoque, validade, id):
        self.nome = nome
        self.valorVenda = valorVenda
        self.valorCompra = valorCompra
        self.fornecedor = fornecedor
        self.estoque = estoque
        self.validade = validade
        self.id = id

    def criar_por_input():
        nome = input("Nome: ")
        valorVenda = float(input("Valor de Venda: "))
        valorCompra = float(input("Valor de Compra: "))
        fornecedor = input("CNPJ Fornecedor:" )
        estoque = input("Quantidade em estoque: ")
        validade = input("Data de Validade: ")
        id = input("Id do Produto: ")
          
        print("Produto Cadastado com sucesso!")
        return Produto(nome, valorVenda, valorCompra, fornecedor, estoque, validade, id)
           
    def atualizar_dados(self):
        
        print("Digite os novos dados (ou pressione Enter para manter o valor atual):")
        novo_nome = input(f"Nome atual: {self.nome}\nNovo nome: ") or self.nome
        novo_valorVenda = input(f"Valor de Venda atual: R${self.valorVenda}\nNovo valor de Venda: ") or self.valorVenda
        novo_valorCompra = input(f"Valor de Compra atual: {self.valorCompra}\nNovo valor de Compra: ") or self.valorCompra
        novo_fornecedor = input(f"Fornecedor atual: {self.fornecedor}\nNovo fornecedor: ") or self.fornecedor
        novo_validade = input(f"Validade atual: {self.validade}\nNova validade: ") or self.validade
        novo_id = input(f"Id Atual: {self.id}\nNovo Id: ") or self.id

        self.nome = novo_nome
        self.valorVenda = novo_valorVenda
        self.valorCompra = novo_valorCompra
        self.fornecedor = novo_fornecedor
        self.validade = novo_validade
        self.id = novo_id

        print("Produto atualizado com sucesso!")

    def exibir(self):
        print(f"Nome: {self.nome} | Valor: R${self.valorVenda}| Valor Compra: R${self.valorCompra} | Fornecedor: {self.fornecedor} | Estoque: {self.estoque} | Validade: {self.validade} | Id: {self.id}")

        

