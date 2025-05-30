class Fornecedor:
    def __init__(self, nome, cnpj, produtos):
        self.nome = nome
        self.cnpj = cnpj
        self.produtos = produtos

    @staticmethod
    def criar_por_input():
        nome = input("Nome do Fornecedor: ")
        cnpj = input("Digite o CNPJ: ")
        while not cnpj.isdigit() or len(cnpj) != 14:
            print("CNPJ inválido! Deve conter exatamente 14 dígitos numéricos.")
            cnpj = input("CNPJ (14 dígitos): ")
            
        produtos_input = input("Digite os IDs dos produtos separados por vírgula: ")
        produtos = [int(id.strip()) for id in produtos_input.split(',')]
        return Fornecedor(nome, cnpj, produtos)

    def atualizar_dados(self):
        
        print("Digite os novos dados (ou pressione Enter para manter o valor atual):")
        novo_nome = input(f"Nome atual: {self.nome}\nNovo nome: ") or self.nome
        novo_cnpj = input(f"CNPJ atual: {self.cnpj}\nNovo CNPJ (14 dígitos): ") or self.cnpj
        if not novo_cnpj.isdigit() or len(novo_cnpj) != 14:
            print("CNPJ inválido. CNPJ antigo mantido.")
            novo_cnpj = self.cnpj
        elif novo_cnpj is None:
            print("Nenhum CNPJ fornecido. CNPJ antigo mantido.")
            novo_cnpj = self.cnpj
        else:
            print("CNPJ atualizado com sucesso.")

        novo_produtos_input = input(f"Produtos atuais: {self.produtos}\nNovos produtos: ") or self.produtos
        novo_produtos_input = ','.join(map(str, novo_produtos_input))
        novo_produtos = [int(id.strip()) for id in novo_produtos_input.split(',')]

        self.nome = novo_nome
        self.cnpj = novo_cnpj
        self.produtos = novo_produtos

        print("\nFornecedor atualizado com sucesso!")
        
    def exibir(self):
        print(f"Nome: {self.nome} | CNPJ: {self.cnpj} | Produtos: {self.produtos}")



 