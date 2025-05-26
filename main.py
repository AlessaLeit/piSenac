from datetime import datetime
from queue import Full
import re

from models.cliente import Cliente
from models.fornecedor import Fornecedor
from models.funcionario import Funcionario
from models.servico import Servico
from models.produto import Produto
from models.financeiro import Financeiro
from models.suprimento import Suprimento

loop = 1 
financeiro = Financeiro()

clientes_cadastrados = []
produtos_cadastrados = []
fornecedor_cadastrados = []
servico_cadastrados = []
funcionario_cadastrados = []
suprimentos_cadastrados = []
agenda_cadastrada = []
lancamentos_financeiros = []

while loop == 1:
    print("\n" + "-" * 10 + "  SOFTWARE  " + "-" * 10)
    print("Escolha uma opção:")
    print("[1] Cliente")
    print("[2] Produtos")
    print("[3] Fornecedores")
    print("[4] Serviços")
    print("[5] Funcionários")
    print("[6] Suprimentos")
    print("[7] Agenda")
    print("[8] Financeiro")
    menu = input("Digite o número correspondente: ")
    
    # Cliente
    if menu == "1":
        print("-" * 11 + "  CLIENTE  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Cliente")
        print("[2] Listar Cliente")
        print("[3] Remover Cliente")
        print("[4] Atualizar Cliente")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")
        
        # Adicionar
        if submenu == "1":
            cliente = Cliente.criar_por_input()
            if cliente: 
                clientes_cadastrados.append(cliente)
            else:
                print("Cliente não foi cadastrado devido a dados inválidos.")

        # Listar
        elif submenu == "2":
            if not clientes_cadastrados:
                print("\nNenhum cliente cadastrado.")
            else:
                print("\n--- Lista de Clientes Cadastrados ---")
                for i, cliente in enumerate(clientes_cadastrados, start=1):
                    if cliente is not None:
                        print(f"\nCliente {i}:")
                        cliente.exibir()
                    else:
                        print(f"\nCliente {i} inválido (None).")
        
        # Remover  
        elif submenu == "3":
            if not clientes_cadastrados:
                print("\nNenhum cliente para remover.")
            else:
                for i, cliente in enumerate(clientes_cadastrados, start=1):
                    print(f"[{i}] {cliente.nome} - CPF: {cliente.cpf}")
                indice = int(input("Digite o número do cliente que deseja remover: ")) - 1
                if 0 <= indice < len(clientes_cadastrados):
                    removido = clientes_cadastrados.pop(indice)
                    print(f"Cliente '{removido.nome}' removido com sucesso.")
                else:
                    print("Índice inválido.")
        
        # Atualizar  
        elif submenu == "4":
            if not clientes_cadastrados:
                print("\nNenhum cliente para atualizar.")
            else:
                for i, cliente in enumerate(clientes_cadastrados, start=1):
                    print(f"[{i}] {cliente.nome} - CPF: {cliente.cpf}")
                indice = int(input("Digite o número do cliente que deseja atualizar: ")) - 1
                if 0 <= indice < len(clientes_cadastrados):
                    cliente_atualizar = clientes_cadastrados[indice]
                    cliente_atualizar.atualizar_dados()
                else:
                    print("Índice inválido.")
    
        # Voltar
        elif submenu == "5":
            exit
    
    # Produto
    if menu == "2":
        print("-" * 11 + "  Produtos  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Produto")
        print("[2] Listar Produtos")
        print("[3] Remover Produto")
        print("[4] Atualizar Produto")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")
   
         # Adicionar
        if submenu == "1":
            produto = Produto.criar_por_input()
            if produto: 
                produtos_cadastrados.append(produto)
            else:
                print("Produto não foi cadastrado devido a dados inválidos.")

        # Listar
        elif submenu == "2":
            if not produtos_cadastrados:
                print("\nNenhum produto cadastrado.")
            else:
                print("\n--- Lista de Produtos Cadastrados ---")
                for i, produto in enumerate(produtos_cadastrados, start=1):
                    if produto is not None:
                        print(f"\nProduto {i}:")
                        produto.exibir()
                    else:
                        print(f"\nProduto {i} inválido (None).")
        
        # Remover  
        elif submenu == "3":
            if not produtos_cadastrados:
                print("\nNenhum produto para remover.")
            else:
                for i, produto in enumerate(produtos_cadastrados, start=1):
                    print(f"[{i}] {produto.nome} - ID: {produto.id}")
                indice = int(input("Digite o número do produto que deseja remover: ")) - 1
                if 0 <= indice < len(produtos_cadastrados):
                    removido = produtos_cadastrados.pop(indice)
                    print(f"Produto '{removido.nome}' removido com sucesso.")
                else:
                    print("Índice inválido.")
        
        # Atualizar  
        elif submenu == "4":
            if not produtos_cadastrados:
                print("\nNenhum produto para atualizar.")
            else:
                for i, produto in enumerate(produtos_cadastrados, start=1):
                    print(f"[{i}] {produto.nome} - ID: {produto.id}")
                indice = int(input("Digite o número do produto que deseja atualizar: ")) - 1
                if 0 <= indice < len(produtos_cadastrados):
                    produto_atualizar = produtos_cadastrados[indice]
                    produto_atualizar.atualizar_dados()
                else:
                    print("Índice inválido.")
       
        # Voltar
        elif submenu == "5":
            exit
    
    # Fornecedor
    if menu == "3":
        print("-" * 11 + "  Fornecedor  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Fornecedor")
        print("[2] Listar Fornecedor")
        print("[3] Remover Fornecedor")
        print("[4] Atualizar Fornecedor")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")
   
         # Adicionar
        if submenu == "1":
            fornecedor = Fornecedor.criar_por_input()
            if fornecedor: 
                fornecedor_cadastrados.append(fornecedor)
            else:
                print("\nFornecedor não foi cadastrado devido a dados inválidos.")

        # Listar
        elif submenu == "2":
            if not fornecedor_cadastrados:
                print("\nNenhum fornecedor cadastrado.")
            else:
                print("\n--- Lista de Fornecedor Cadastrados ---")
                for i, fornecedor in enumerate(fornecedor_cadastrados, start=1):
                    if fornecedor is not None:
                        print(f"\nFornecedor {i}:")
                        fornecedor.exibir()
                    else:
                        print(f"\nFornecedor {i} inválido (None).")
        
        # Remover  
        elif submenu == "3":
            if not fornecedor_cadastrados:
                print("\nNenhum fornecedor para remover.")
            else:
                for i, fornecedor in enumerate(fornecedor_cadastrados, start=1):
                    print(f"[{i}] {fornecedor.nome} - CNPJ: {fornecedor.cnpj}")
                indice = int(input("Digite o número do fornecedor que deseja remover: ")) - 1
                if 0 <= indice < len(fornecedor_cadastrados):
                    removido = fornecedor_cadastrados.pop(indice)
                    print(f"Fornecedor '{removido.nome}' removido com sucesso.")
                else:
                    print("Índice inválido.")
        
        # Atualizar  
        elif submenu == "4":
            if not fornecedor_cadastrados:
                print("\nNenhum produto para atualizar.")
            else:
                for i, fornecedor in enumerate(fornecedor_cadastrados, start=1):
                    print(f"[{i}] {fornecedor.nome} - CNPJ: {fornecedor.cnpj}")
                indice = int(input("Digite o número do fornecedor que deseja atualizar: ")) - 1
                if 0 <= indice < len(fornecedor_cadastrados):
                    fornecedor_atualizar = fornecedor_cadastrados[indice]
                    fornecedor_atualizar.atualizar_dados()
                else:
                    print("Índice inválido.")
       
        # Voltar
        elif submenu == "5":
            exit
                
    # Serviços
    if menu == "4":
        print("-" * 11 + "  SERVIÇOS  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Serviço")
        print("[2] Listar Serviço")
        print("[3] Remover Serviço")
        print("[4] Atualizar Serviço")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")
        
        # Adicionar
        if submenu == "1":
            servico = Servico.criar_por_input()
            if servico: 
                servico_cadastrados.append(servico)
            else:
                print("Serviço não foi cadastrado devido a dados inválidos.")

        # Listar
        elif submenu == "2":
            if not servico_cadastrados:
                print("\nNenhum serviço cadastrado.")
            else:
                print("\n--- Lista de Serviços Cadastrados ---")
                for i, servico in enumerate(servico_cadastrados, start=1):
                    if servico is not None:
                        print(f"\nServiço {i}:")
                        servico.exibir()
                    else:
                        print(f"\nServiço {i} inválido (None).")
        
        # Remover  
        elif submenu == "3":
            if not servico_cadastrados:
                print("\nNenhum serviço para remover.")
            else:
                for i, servico in enumerate(servico_cadastrados, start=1):
                    print(f"[{i}] {servico.nome} - Valor: {servico.valor} - Tempo: {servico.tempoExe}")
                indice = int(input("Digite o número do serviço que deseja remover: ")) - 1
                if 0 <= indice < len(servico_cadastrados):
                    removido = servico_cadastrados.pop(indice)
                    print(f"Serviço '{removido.nome}' removido com sucesso.")
                else:
                    print("Índice inválido.")
        
        # Atualizar  
        elif submenu == "4":
            if not servico_cadastrados:
                print("\nNenhum serviço para atualizar.")
            else:
                for i, servico in enumerate(servico_cadastrados, start=1):
                    print(f"[{i}] {servico.nome} - Valor: {servico.valor} - Tempo: {servico.tempoExe}")
                indice = int(input("Digite o número do serviço que deseja atualizar: ")) - 1
                if 0 <= indice < len(servico_cadastrados):
                    servico_atualizar = servico_cadastrados[indice]
                    servico_atualizar.atualizar_dados()
                else:
                    print("Índice inválido.")
    
        # Voltar
        elif submenu == "5":
            exit
    
    # Funcionários
    if menu == "5":
        print("-" * 11 + "  FUNCIONÁRIOS  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Funcionário")
        print("[2] Listar Funcionário")
        print("[3] Remover Funcionário")
        print("[4] Atualizar Funcionário")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")
            
        # Adicionar
        if submenu == "1":
            funcionario = Funcionario.criar_por_input()
            if funcionario: 
                funcionario_cadastrados.append(funcionario)
            else:
                    print("Funcionário não foi cadastrado devido a dados inválidos.")

        # Listar
        elif submenu == "2":
            if not funcionario_cadastrados:
                print("\nNenhum funcionário cadastrado.")
            else:
                print("\n--- Lista de Funcionários Cadastrados ---")
            for i, funcionario in enumerate(funcionario_cadastrados, start=1):
                if funcionario is not None:
                    print(f"\nFuncionário {i}:")
                    funcionario.exibir()
                else:
                    print(f"\nFuncionário {i} inválido (None).")
            
        # Remover  
        elif submenu == "3":
            if not funcionario_cadastrados:
                print("\nNenhum funcionário para remover.")
            else:
                for i, funcionario in enumerate(funcionario_cadastrados, start=1):
                    print(f"[{i}] {funcionario.nome} - CTPS: {funcionario.ctps} - NIS: {funcionario.nis}")
                indice = int(input("Digite o número do funcionário que deseja remover: ")) - 1
                if 0 <= indice < len(funcionario_cadastrados):
                    removido = funcionario_cadastrados.pop(indice)
                    print(f"Funcionário '{removido.nome}' removido com sucesso.")
                else:
                    print("Índice inválido.")
            
        # Atualizar  
        elif submenu == "4":
            if not funcionario_cadastrados:
                print("\nNenhum funcionário para atualizar.")
            else:
                for i, funcionario in enumerate(funcionario_cadastrados, start=1):
                    print(f"[{i}] {funcionario.nome} - CTPS: {funcionario.ctps} - NIS: {funcionario.nis}")
                indice = int(input("Digite o número do funcionário que deseja atualizar: ")) - 1
                if 0 <= indice < len(funcionario_cadastrados):
                    funcionario_atualizar = funcionario_cadastrados[indice]
                    funcionario_atualizar.atualizar_dados()
                else:
                    print("Índice inválido.")
        
        # Voltar
        elif submenu == "5":
            exit
    
    # Suprimentos
    if menu == "6":
        print("-" * 11 + "  SUPRIMENTOS  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Suprimento")
        print("[2] Listar Suprimentos")
        print("[3] Remover Suprimento")
        print("[4] Atualizar Suprimento")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")

        if submenu == "1":
            suprimento = Suprimento.criar_por_input()
            if suprimento:
                suprimentos_cadastrados.append(suprimento)
            else:
                print("Suprimento não foi cadastrado devido a dados inválidos.")

        elif submenu == "2":
            if not suprimentos_cadastrados:
                print("\nNenhum suprimento cadastrado.")
            else:
                print("\n--- Lista de Suprimentos Cadastrados ---")
                for i, s in enumerate(suprimentos_cadastrados, start=1):
                    print(f"\nSuprimento {i}:")
                    s.exibir()

        elif submenu == "3":
            if not suprimentos_cadastrados:
                print("\nNenhum suprimento para remover.")
            else:
                for i, s in enumerate(suprimentos_cadastrados, start=1):
                    print(f"[{i}] {s.nome}")
                indice = int(input("Digite o número do suprimento que deseja remover: ")) - 1
                if 0 <= indice < len(suprimentos_cadastrados):
                    removido = suprimentos_cadastrados.pop(indice)
                    print(f"Suprimento '{removido.nome}' removido com sucesso.")
                else:
                    print("Índice inválido.")

        elif submenu == "4":
            if not suprimentos_cadastrados:
                print("\nNenhum suprimento para atualizar.")
            else:
                for i, s in enumerate(suprimentos_cadastrados, start=1):
                    print(f"[{i}] {s.nome}")
                indice = int(input("Digite o número do suprimento que deseja atualizar: ")) - 1
                if 0 <= indice < len(suprimentos_cadastrados):
                    suprimentos_cadastrados[indice].atualizar_dados()
                else:
                    print("Índice inválido.")

        elif submenu == "5":
            exit

    # Agenda
    if menu == "7":
        print("-" * 11 + "  AGENDA  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Horário")
        print("[2] Listar Horários")
        print("[3] Remover Horário")
        print("[4] Voltar")
        submenu = input("Digite o número correspondente: ")

        # Adicionar
        if submenu == "1":
            if not clientes_cadastrados:
                print("Cadastre ao menos um cliente antes de agendar.")
            else:
                for i, cliente in enumerate(clientes_cadastrados, start=1):
                    print(f"[{i}] {cliente.nome}")
                idx_cliente = int(input("Escolha o cliente: ")) - 1
                cliente = clientes_cadastrados[idx_cliente]

                data = input("Data (DD/MM/AAAA): ")
                hora = input("Hora (HH:MM): ")

                # Selecionar serviços
                servicos_selecionados = []
                if not servico_cadastrados:
                    print("Nenhum serviço disponível.")
                else:
                    print("Selecione os serviços (0 para terminar):")
                    while True:
                        for i, s in enumerate(servico_cadastrados, start=1):
                            print(f"[{i}] {s.nome} - R${s.valor}")
                        op = int(input("Número do serviço: "))
                        if op == 0:
                            break
                        if 1 <= op <= len(servico_cadastrados):
                            servicos_selecionados.append(servico_cadastrados[op - 1])
                        else:
                            print("Opção inválida.")

                # Selecionar suprimentos
                suprimentos_selecionados = []
                if not suprimentos_cadastrados:
                    print("Nenhum suprimento disponível.")
                else:
                    print("Selecione os suprimentos (0 para terminar):")
                    while True:
                        for i, s in enumerate(suprimentos_cadastrados, start=1):
                            print(f"[{i}] {s.nome} - R${s.valor}")
                        op = int(input("Número do suprimento: "))
                        if op == 0:
                            break
                        if 1 <= op <= len(suprimentos_cadastrados):
                            suprimentos_selecionados.append(suprimentos_cadastrados[op - 1])
                        else:
                            print("Opção inválida.")

                from models.agenda import Agenda
                compromisso = Agenda(data, hora, cliente, servicos_selecionados, suprimentos_selecionados)
                agenda_cadastrada.append(compromisso)
                print("Compromisso registrado com sucesso!")

        # Listar
        elif submenu == "2":
            if not agenda_cadastrada:
                print("Nenhum compromisso registrado.")
            else:
                print("\n--- Lista de Compromissos ---")
                for i, ag in enumerate(agenda_cadastrada, start=1):
                    print(f"\nCompromisso {i}:")
                    ag.exibir_agendamento()

        # Remover
        elif submenu == "3":
            if not agenda_cadastrada:
                print("Nenhum compromisso para remover.")
            else:
                for i, ag in enumerate(agenda_cadastrada, start=1):
                    print(f"[{i}] {ag.data} - {ag.cliente.nome}")
                idx = int(input("Digite o número do compromisso a remover: ")) - 1
                if 0 <= idx < len(agenda_cadastrada):
                    removido = agenda_cadastrada.pop(idx)
                    print(f"Compromisso com {removido.cliente.nome} em {removido.data} removido.")
                else:
                    print("Índice inválido.")

        # Voltar
        elif submenu == "4":
            exit

    # Financeiro
    if menu == "8":
        print("-" * 11 + "  FINANCEIRO  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Registrar Entrada (Receita de Cliente)")
        print("[2] Registrar Saída (Despesa)")
        print("[3] Calcular Comissão de Funcionário")
        print("[4] Exibir Relatório Financeiro")
        print("[5] Voltar")
        submenu = input("Digite o número correspondente: ")

        # Registrar entrada
        if submenu == "1":
            if not clientes_cadastrados or not agenda_cadastrada:
                print("Você precisa ter pelo menos um cliente e um agendamento registrado.")
            else:
                for i, cliente in enumerate(clientes_cadastrados, start=1):
                    print(f"[{i}] {cliente.nome}")
                idx_cliente = int(input("Selecione o cliente: ")) - 1

                for i, ag in enumerate(agenda_cadastrada, start=1):
                    print(f"[{i}] {ag.titulo} - {ag.data}")
                idx_agenda = int(input("Selecione o compromisso relacionado: ")) - 1

                valor = float(input("Valor recebido: R$ "))
                descricao = input("Descrição da entrada: ")

                financeiro.registrar_entrada(
                    clientes_cadastrados[idx_cliente], valor, descricao, agenda_cadastrada[idx_agenda]
                )
                print("Entrada registrada com sucesso.")

        # Registrar saída
        elif submenu == "2":
            if not agenda_cadastrada:
                print("Você precisa ter pelo menos um compromisso registrado.")
            else:
                for i, ag in enumerate(agenda_cadastrada, start=1):
                    print(f"[{i}] {ag.titulo} - {ag.data}")
                idx_agenda = int(input("Selecione o compromisso relacionado: ")) - 1

                valor = float(input("Valor da despesa: R$ "))
                descricao = input("Descrição da saída: ")

                financeiro.registrar_saida(valor, descricao, agenda_cadastrada[idx_agenda])
                print("Saída registrada com sucesso.")

        # Calcular comissão
        elif submenu == "3":
            if not funcionario_cadastrados:
                print("Nenhum funcionário cadastrado.")
            else:
                for i, func in enumerate(funcionario_cadastrados, start=1):
                    print(f"[{i}] {func.nome}")
                idx_func = int(input("Selecione o funcionário: ")) - 1
                percentual = float(input("Percentual de comissão (%): "))
                financeiro.calcular_comissao(funcionario_cadastrados[idx_func], percentual)
                print("Comissão registrada com sucesso.")

        # Exibir relatório
        elif submenu == "4":
            financeiro.exibir_financeiro()

        # Voltar
        elif submenu == "5":
            exit
