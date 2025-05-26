class Financeiro:
    def __init__(self):
        self.entradas = []  # Armazenará as entradas (pagamentos de clientes)
        self.saidas = []  # Armazenará as saídas (despesas)
        self.comissoes = []  # Comissões dos funcionários

    def registrar_entrada(self, cliente, valor, descricao, agenda):
        self.entradas.append({
            'cliente': cliente.nome,
            'valor': valor,
            'descricao': descricao,
            'data': agenda.data
        })

    def registrar_saida(self, valor, descricao, agenda):
        self.saidas.append({
            'valor': valor,
            'descricao': descricao,
            'data': agenda.data 
        })

    # Calcula a comissão de um funcionário com base nas entradas
    def calcular_comissao(self, funcionario, percentual_comissao):
        total_entradas = sum([entrada['valor'] for entrada in self.entradas])
        comissao = total_entradas * percentual_comissao / 100
        self.comissoes.append({
            'funcionario': funcionario.nome,
            'comissao': comissao
        })

    def exibir_financeiro(self):
        print("Entradas:")
        for entrada in self.entradas:
            print(f"{entrada['data']} - {entrada['descricao']}: R${entrada['valor']:.2f}")
        print("Saídas:")
        for saida in self.saidas:
            print(f"{saida['data']} - {saida['descricao']}: R${saida['valor']:.2f}")
        print("Comissões dos Funcionários:")
        for comissao in self.comissoes:
            print(f"{comissao['funcionario']} - Comissão: R${comissao['comissao']:.2f}")
        print("-" * 30)