from datetime import datetime
from queue import Full
import re

from cliente import Cliente
from fornecedor import Fornecedor
from servico import Servico
from produto import Produto

loop = 1 
clientes_cadastrados = []
produtos_cadastrados = []
fornecedor_cadastrados = []
servico_cadastrados = []
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
    
    #Funcionários