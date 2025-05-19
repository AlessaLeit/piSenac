class Fornecedor:
    def __init__(self, nome, cnpj, produtos):
        self.nome = nome
        self.cnpj = cnpj
        self.produtos = produtos

    @staticmethod
    def criar_por_input():
        nome = input("Nome do Fornecedor: ")
        cnpj = input("Digite o CNPJ: ")
        produtos_input = input("Digite os IDs dos produtos separados por vírgula: ")
        produtos = [int(id.strip()) for id in produtos_input.split(',')]
        return Fornecedor(nome, cnpj, produtos)

    def atualizar_dados(self):
        
        print("Digite os novos dados (ou pressione Enter para manter o valor atual):")
        novo_nome = input(f"Nome atual: {self.nome}\nNovo nome: ") or self.nome
        novo_cnpj = input(f"CNPJ atual: {self.cnpj}\nNovo CNPJ (14 dígitos): ") or self.cnpj
        if not novo_cnpj.isdigit() or len(novo_cnpj) != 14:
            print("CNPJ inválido. Atualização cancelada.")
            return

        novo_produtos_input = input(f"Produtos atuais: {self.produtos}\nNovos produtos: ") or self.produtos
        novo_produtos = [int(id.strip()) for id in novo_produtos_input.split(',')]

        self.nome = novo_nome
        self.cnpj = novo_cnpj
        self.produtos = novo_produtos

        print("Fornecedor atualizado com sucesso!")
        
    def exibir(self):
        print(f"Nome: {self.nome} | CNPJ: {self.cnpj} | Produtos: {self.produtos}")



 