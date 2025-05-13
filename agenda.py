class Agenda:
    def __init__(self, data, hora, cliente, servicos, suprimentos):
        self.data = data
        self.hora = hora
        self.cliente = cliente
        self.servicos = servicos  
        self.suprimentos = suprimentos  
        self.valorTotal = self.calcular_valor_total()

    # Calcula o valor total com base nos serviços e produtos
    def calcular_valor_total(self):
        total_servicos = sum([servico.valor for servico in self.servicos])
        total_suprimentos = sum([suprimentos.valor for suprimentos in self.suprimentos])
        return total_servicos + total_suprimentos

    def exibir_agendamento(self):
        print(f"Data: {self.data}, Hora: {self.hora}")
        print(f"Cliente: {self.cliente.nome}")
        print("Serviços:")
        for servico in self.servicos:
            print(f"- {servico.nome}: R${servico.valor:.2f}")
        print("Produtos:")
        for suprimentos in self.suprimentos:
            print(f"- {suprimentos.nome}: R${suprimentos.valor:.2f}")
        print(f"Valor Total: R${self.valorTotal:.2f}")
        print("-" * 30)