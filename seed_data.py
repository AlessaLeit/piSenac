import datetime
from random import randint, choice
import database
import cliente as crud_cliente
import funcionario as crud_funcionario
import produto as crud_produto
import servico as crud_servico
import fornecedor as crud_fornecedor
import suprimento as crud_suprimento
import maquina as crud_maquina
import despesa as crud_despesa
import venda as crud_venda
import agenda as crud_agenda
import info as mod_info

def create_sample_clientes(session):
    for i in range(10):
        nome = f"Cliente {i+1}"
        # Valid CPFs for testing (example valid CPFs)
        valid_cpfs = [
            "123.456.789-09",
            "987.654.321-00",
            "111.222.333-44",
            "555.666.777-88",
            "999.888.777-66",
            "123.123.123-12",
            "321.321.321-32",
            "456.456.456-45",
            "654.654.654-65",
            "789.789.789-78"
        ]
        cpf = valid_cpfs[i]
        nascimento = datetime.date(1990, 1, 1)
        info_contato = mod_info.Informacao(f"+55119999900{i:02d}", f"cliente{i+1}@email.com", f"Rua {i+1}, 123", redes_sociais="")
        crud_cliente.criar_cliente(session, nome=nome, nascimento_obj=nascimento, cpf=cpf, info_contato=info_contato)

def create_sample_funcionarios(session):
    for i in range(10):
        nome = f"Funcionario {i+1}"
        # Valid CPFs for testing (example valid CPFs)
        valid_cpfs = [
            "234.567.890-12",
            "876.543.210-98",
            "222.333.444-55",
            "666.777.888-99",
            "888.777.666-55",
            "234.234.234-23",
            "432.432.432-43",
            "567.567.567-56",
            "765.765.765-76",
            "890.890.890-89"
        ]
        cpf = valid_cpfs[i]
        nascimento = datetime.date(1985, 1, 1)
        ctps = f"CTPS{i+1}"
        salario = 2000 + i * 100
        data_admissao = datetime.date(2020, 1, 1)
        info_contato = mod_info.Informacao(f"+55119888800{i:02d}", f"funcionario{i+1}@email.com", f"Av {i+1}, 456", redes_sociais="")
        crud_funcionario.criar_funcionario(session, nome=nome, cpf=cpf, nascimento=nascimento, ctps=ctps, salario=salario, data_admissao=data_admissao, informacao_contato=info_contato)

def create_sample_produtos(session):
    for i in range(10):
        nome = f"Produto {i+1} (Val: 2025-12-{10+i})"
        preco = 10 + i * 2
        estoque = 100 + i * 10
        crud_produto.criar_produto(session, nome=nome, preco=preco, estoque=estoque)

def create_sample_servicos(session):
    for i in range(10):
        nome = f"Servico {i+1}"
        valor_venda = 50 + i * 5
        custo = 20 + i * 2
        crud_servico.criar_servico(session, nome=nome, valor_venda=valor_venda, custo=custo)

def create_sample_fornecedores(session):
    for i in range(10):
        nome = f"Fornecedor {i+1}"
        cnpj = f"00.000.000/0000-{i:02d}"
        telefone = f"+551197777000{i:02d}"
        email = f"fornecedor{i+1}@email.com"
        endereco = f"Rua Fornecedor {i+1}, 789"
        info_contato = mod_info.Informacao(telefone, email, endereco, redes_sociais="")
        crud_fornecedor.criar_fornecedor(session, nome=nome, cnpj=cnpj, info_contato=info_contato)

def create_sample_suprimentos(session):
    for i in range(10):
        nome = f"Suprimento {i+1}"
        unidade_medida = "un"
        custo_unitario = 5 + i
        estoque = 50 + i * 5
        crud_suprimento.criar_suprimento(session, nome=nome, unidade_medida=unidade_medida, custo_unitario=custo_unitario, estoque=estoque)

def create_sample_maquinas(session):
    from maquina import StatusMaquina
    for i in range(10):
        nome = f"Maquina {i+1}"
        numero_serie = f"SN{i+1000}"
        status = StatusMaquina.OPERANDO
        custo_aquisicao = 1000 + i * 100
        crud_maquina.criar_maquina(session, nome=nome, numero_serie=numero_serie, status=status, custo_aquisicao=custo_aquisicao)

def create_sample_despesas(session, funcionarios):
    # Create salary expenses for funcionarios
    for i, func in enumerate(funcionarios):
        valor = func.salario
        descontos = 0
        data_despesa = datetime.date.today()
        crud_despesa.criar_salario(session, func, valor, descontos, data_despesa)
    # Create other expenses
    for i in range(5):
        tipo = choice(["FixoTerceiro", "Outros"])
        valor = 100 + i * 10
        data_despesa = datetime.date.today()
        if tipo == "FixoTerceiro":
            crud_despesa.criar_fixo_terceiro(session, valor, f"Despesa Fixa {i+1}", data_despesa)
        else:
            crud_despesa.criar_outros(session, valor, f"Despesa Outros {i+1}", data_despesa)

def create_sample_agendas(session, funcionarios, clientes):
    for i in range(10):
        func = funcionarios[i % len(funcionarios)]
        cli = clientes[i % len(clientes)]
        data_hora_inicio = datetime.datetime.now() + datetime.timedelta(days=i)
        data_hora_fim = data_hora_inicio + datetime.timedelta(hours=1)
        itens_agendados = []
        crud_agenda.criar_agenda(session, func, cli, data_hora_inicio, data_hora_fim, itens_agendados=itens_agendados, maquinas_agendadas=[])

def create_sample_vendas(session, funcionarios, clientes, produtos):
    for i in range(10):
        func = funcionarios[i % len(funcionarios)]
        cli = clientes[i % len(clientes)]
        prod = produtos[i % len(produtos)]
        data_venda = datetime.date.today()
        from venda import ItemVenda
        itens_venda = [ItemVenda(prod, randint(1, 5))]
        crud_venda.criar_venda(session, func, cli, data_venda, itens_venda=itens_venda, agenda_obj=None)

def main():
    session = database.SessionLocal()
    try:
        create_sample_clientes(session)
        create_sample_funcionarios(session)
        create_sample_produtos(session)
        create_sample_servicos(session)
        create_sample_fornecedores(session)
        create_sample_suprimentos(session)
        create_sample_maquinas(session)

        funcionarios = session.query(crud_funcionario.Funcionario).all()
        clientes = session.query(crud_cliente.Cliente).all()
        produtos = session.query(crud_produto.Produto).all()

        create_sample_despesas(session, funcionarios)
        create_sample_agendas(session, funcionarios, clientes)
        create_sample_vendas(session, funcionarios, clientes, produtos)

        session.commit()
        print("Sample data added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error adding sample data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
