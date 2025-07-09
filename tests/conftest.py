# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, agenda_maquinas_tabela, agenda_itens_tabela, agenda_suprimentos_tabela, venda_itens_tabela
import cliente as crud_cliente
import funcionario as crud_funcionario
import produto as crud_produto
import servico as crud_servico
import fornecedor as crud_fornecedor
import suprimento as crud_suprimento
import maquina as crud_maquina
import agenda as crud_agenda
import despesa as crud_despesa
import venda as crud_venda
import info as mod_info
from datetime import date, datetime, timedelta
from maquina import StatusMaquina
from agenda import AgendaStatus, ItemAgendado, SuprimentoAgendado

@pytest.fixture(scope="session")
def engine():
    """Cria um engine de banco de dados SQLite em memória para testes."""
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    """Cria todas as tabelas no banco de dados de teste."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine) # Limpa as tabelas após todos os testes da sessão

@pytest.fixture(scope="function")
def db_session(engine, tables):
    """
    Fornece uma sessão de banco de dados para cada teste.
    Cada teste roda em sua própria transação e é revertido ao final.
    """
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Limpa os dados de tabelas específicas antes de cada teste para garantir isolamento
    for table in reversed(Base.metadata.sorted_tables):
        if table.name not in ['agenda_maquinas', 'agenda_itens', 'agenda_suprimentos', 'venda_itens']:
            session.execute(table.delete())
    session.commit() # Commit para limpar antes de iniciar a nova transação para o teste

    # Inicia uma nova transação para o teste
    session.begin_nested() # Usa begin_nested para permitir rollback sem fechar a conexão

    yield session

    session.rollback() # Reverte a transação do teste
    transaction.rollback() # Reverte a transação da conexão
    connection.close()

# Fixtures de dados para facilitar a criação de objetos de teste
@pytest.fixture
def sample_info_contato():
    return mod_info.Informacao(
        telefone="(11) 98765-4321",
        email="teste@example.com",
        endereco="Rua Teste, 123, Centro, Cidade, SP",
        redes_sociais="instagram.com/teste"
    )

@pytest.fixture
def sample_cliente(db_session, sample_info_contato):
    return crud_cliente.criar_cliente(
        db_session,
        nome="Cliente Teste",
        nascimento_obj=date(1990, 5, 15),
        cpf="123.456.789-00",
        info_contato=sample_info_contato
    )

@pytest.fixture
def sample_funcionario(db_session, sample_info_contato):
    return crud_funcionario.criar_funcionario(
        db_session,
        nome="Funcionario Teste",
        nascimento_obj=date(1985, 1, 1),
        cpf="78961683080",
        ctps="12345678",
        informacao_contato=sample_info_contato,
        salario=3000.00,
        data_admissao_obj=date(2020, 1, 1)
    )

@pytest.fixture
def sample_produto(db_session):
    return crud_produto.criar_produto(
        db_session,
        nome="Produto Teste",
        preco=50.00,
        estoque=100.00
    )

@pytest.fixture
def sample_servico(db_session):
    return crud_servico.criar_servico(
        db_session,
        nome="Servico Teste",
        valor_venda=150.00,
        custo=50.00
    )

@pytest.fixture
def sample_fornecedor(db_session, sample_info_contato):
    return crud_fornecedor.criar_fornecedor(
        db_session,
        nome="Fornecedor Teste LTDA",
        cnpj="86460889000105",
        info_contato=sample_info_contato
    )

@pytest.fixture
def sample_suprimento(db_session):
    return crud_suprimento.criar_suprimento(
        db_session,
        nome="Algodão",
        unidade_medida="kg",
        custo_unitario=10.00,
        estoque=50.00
    )

@pytest.fixture
def sample_maquina(db_session):
    return crud_maquina.criar_maquina(
        db_session,
        nome="Máquina Laser",
        numero_serie="ML-001-XYZ",
        custo_aquisicao=15000.00,
        status=StatusMaquina.OPERANDO
    )

@pytest.fixture
def sample_agenda(db_session, sample_funcionario, sample_cliente, sample_servico):
    data_inicio = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    data_fim = data_inicio + timedelta(hours=1)
    itens = [ItemAgendado(sample_servico, 1, sample_servico.valor_venda)]
    return crud_agenda.criar_agenda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_hora_inicio_obj=data_inicio,
        data_hora_fim_obj=data_fim,
        itens_agendados=itens
    )

@pytest.fixture
def sample_venda(db_session, sample_funcionario, sample_cliente, sample_produto):
    itens = [crud_venda.ItemVenda(sample_produto, 2, sample_produto.preco)]
    return crud_venda.criar_venda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_venda_obj=date.today(),
        itens_venda=itens
    )

