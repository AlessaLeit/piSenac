from datetime import datetime
from queue import Full
import re

from cliente import Cliente

loop = 1 
clientes_cadastrados = []
while loop == 1:
    print("-" * 10 + "  SOFTWARE  " + "-" * 10)
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
    
    if menu == "1":
        print("-" * 11 + "  CLIENTE  " + "-" * 11)
        print("Escolha uma opção:")
        print("[1] Adicionar Cliente")
        print("[2] Listar Cliente")
        print("[3] Remover Cliente")
        print("[4] Atualziar Cliente")
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
                print("Nenhum cliente cadastrado.")
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
                print("Nenhum cliente para remover.")
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
                print("Nenhum cliente para atualizar.")
            else:
                for i, cliente in enumerate(clientes_cadastrados, start=1):
                    print(f"[{i}] {cliente.nome} - CPF: {cliente.cpf}")
                indice = int(input("Digite o número do cliente que deseja atualizar: ")) - 1
                if 0 <= indice < len(clientes_cadastrados):
                    cliente_atualizar = clientes_cadastrados[indice]
                    cliente_atualizar.atualizar_dados()
                else:
                    print("Índice inválido.")


                




