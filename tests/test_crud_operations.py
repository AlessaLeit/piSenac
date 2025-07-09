# tests/test_crud_operations.py
import pytest
from datetime import date, datetime, timedelta
from maquina import StatusMaquina
from agenda import AgendaStatus, ItemAgendado, SuprimentoAgendado
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
from database import agenda_itens_tabela, agenda_suprimentos_tabela, venda_itens_tabela

# --- Testes para Cliente ---
def test_criar_cliente(db_session, sample_info_contato):
    cliente = crud_cliente.criar_cliente(
        db_session,
        nome="Novo Cliente",
        nascimento_obj=date(1992, 10, 20),
        cpf="111.222.333-44",
        info_contato=sample_info_contato
    )
    assert cliente.id is not None
    assert cliente.nome == "Novo Cliente"
    assert cliente.cpf == "111.222.333-44"
    assert cliente.info_contato.email == "teste@example.com"

def test_criar_cliente_cpf_duplicado(db_session, sample_cliente, sample_info_contato):
    with pytest.raises(ValueError, match="Cliente com CPF 123.456.789-00 já existe."):
        crud_cliente.criar_cliente(
            db_session,
            nome="Outro Cliente",
            nascimento_obj=date(1995, 1, 1),
            cpf="123.456.789-00",
            info_contato=sample_info_contato
        )

def test_buscar_cliente_id(db_session, sample_cliente):
    found_cliente = crud_cliente.buscar_cliente_id(db_session, sample_cliente.id)
    assert found_cliente == sample_cliente

def test_atualizar_dados_cliente(db_session, sample_cliente):
    updated_cliente = crud_cliente.atualizar_dados_cliente(
        db_session,
        sample_cliente.id,
        nome="Cliente Atualizado",
        email="novo_email@example.com"
    )
    assert updated_cliente.nome == "Cliente Atualizado"
    assert updated_cliente.info_contato.email == "novo_email@example.com"

def test_deletar_cliente(db_session, sample_cliente):
    crud_cliente.deletar_cliente(db_session, sample_cliente.id)
    assert crud_cliente.buscar_cliente_id(db_session, sample_cliente.id) is None

def test_deletar_cliente_em_uso_agenda(db_session, sample_cliente, sample_agenda):
    with pytest.raises(Exception): # A exceção específica pode variar dependendo da configuração do ORM para FK
        crud_cliente.deletar_cliente(db_session, sample_cliente.id)
    db_session.rollback() # Garante que a sessão seja limpa após o erro

def test_deletar_cliente_em_uso_venda(db_session, sample_cliente, sample_venda):
    with pytest.raises(Exception): # A exceção específica pode variar dependendo da configuração do ORM para FK
        crud_cliente.deletar_cliente(db_session, sample_cliente.id)
    db_session.rollback() # Garante que a sessão seja limpa após o erro

# --- Testes para Funcionário ---
def test_criar_funcionario(db_session, sample_info_contato):
    funcionario = crud_funcionario.criar_funcionario(
        db_session,
        nome="Novo Funcionario",
        nascimento_obj=date(1990, 1, 1),
        cpf="111.222.333-55",
        ctps="9876543-21/0001",
        informacao_contato=sample_info_contato,
        salario=2500.00,
        data_admissao_obj=date(2021, 1, 1)
    )
    assert funcionario.id is not None
    assert funcionario.nome == "Novo Funcionario"
    assert funcionario.cpf == "111.222.333-55"

def test_buscar_funcionario_por_cpf(db_session, sample_funcionario):
    found_func = crud_funcionario.buscar_funcionario_por_cpf(db_session, sample_funcionario.cpf)
    assert found_func == sample_funcionario

def test_atualizar_dados_funcionario(db_session, sample_funcionario):
    updated_func = crud_funcionario.atualizar_dados_funcionario(
        db_session,
        sample_funcionario.id,
        salario=3500.00,
        data_demissao_obj=date(2023, 12, 31)
    )
    assert updated_func.salario == 3500.00
    assert updated_func.data_demissao == date(2023, 12, 31)

def test_deletar_funcionario_por_id(db_session, sample_funcionario):
    crud_funcionario.deletar_funcionario_por_id(db_session, sample_funcionario.id)
    assert crud_funcionario.buscar_funcionario_por_id(db_session, sample_funcionario.id) is None

def test_deletar_funcionario_em_uso_agenda(db_session, sample_funcionario, sample_agenda):
    with pytest.raises(Exception):
        crud_funcionario.deletar_funcionario_por_id(db_session, sample_funcionario.id)
    db_session.rollback()

def test_deletar_funcionario_em_uso_venda(db_session, sample_funcionario, sample_venda):
    with pytest.raises(Exception):
        crud_funcionario.deletar_funcionario_por_id(db_session, sample_funcionario.id)
    db_session.rollback()

# --- Testes para Produto ---
def test_criar_produto(db_session):
    produto = crud_produto.criar_produto(db_session, nome="Novo Produto", preco=25.00, estoque=50.00)
    assert produto.id is not None
    assert produto.nome == "Novo Produto"

def test_buscar_produto(db_session, sample_produto):
    found_produto = crud_produto.buscar_produto(db_session, sample_produto.nome)
    assert found_produto == sample_produto

def test_atualizar_dados_produto(db_session, sample_produto):
    updated_produto = crud_produto.atualizar_dados_produto(
        db_session,
        sample_produto.id,
        preco=60.00,
        estoque=120.00
    )
    assert updated_produto.preco == 60.00
    assert updated_produto.estoque == 120.00

def test_deletar_produto(db_session, sample_produto):
    crud_produto.deletar_produto(db_session, sample_produto.id)
    assert crud_produto.buscar_produto_id(db_session, sample_produto.id) is None

# --- Testes para Serviço ---
def test_criar_servico(db_session):
    servico = crud_servico.criar_servico(db_session, nome="Novo Servico", valor_venda=200.00, custo=70.00)
    assert servico.id is not None
    assert servico.nome == "Novo Servico"

def test_buscar_servico(db_session, sample_servico):
    found_servico = crud_servico.buscar_servico(db_session, sample_servico.nome)
    assert found_servico == sample_servico

def test_atualizar_dados_servico(db_session, sample_servico):
    updated_servico = crud_servico.atualizar_dados_servico(
        db_session,
        sample_servico.id,
        valor_venda=180.00,
        custo=60.00
    )
    assert updated_servico.valor_venda == 180.00
    assert updated_servico.custo == 60.00

def test_deletar_servico(db_session, sample_servico):
    crud_servico.deletar_servico(db_session, sample_servico.id)
    assert crud_servico.buscar_servico_id(db_session, sample_servico.id) is None

# --- Testes para Fornecedor ---
def test_criar_fornecedor(db_session, sample_info_contato):
    fornecedor = crud_fornecedor.criar_fornecedor(
        db_session,
        nome="Novo Fornecedor",
        cnpj="11.222.333/0001-44",
        info_contato=sample_info_contato
    )
    assert fornecedor.id is not None
    assert fornecedor.nome == "Novo Fornecedor"
    assert fornecedor.cnpj == "11.222.333/0001-44"

def test_buscar_fornecedor(db_session, sample_fornecedor):
    found_fornecedor = crud_fornecedor.buscar_fornecedor(db_session, sample_fornecedor.cnpj)
    assert found_fornecedor == sample_fornecedor

def test_atualizar_dados_fornecedor(db_session, sample_fornecedor):
    updated_fornecedor = crud_fornecedor.atualizar_dados_fornecedor(
        db_session,
        sample_fornecedor.id,
        nome="Fornecedor Atualizado",
        telefone="(21) 99887-7665"
    )
    assert updated_fornecedor.nome == "Fornecedor Atualizado"
    assert updated_fornecedor.info_contato.telefone == "(21) 99887-7665"

def test_deletar_fornecedor(db_session, sample_fornecedor):
    crud_fornecedor.deletar_fornecedor(db_session, sample_fornecedor.id)
    assert crud_fornecedor.buscar_fornecedor_id(db_session, sample_fornecedor.id) is None

# --- Testes para Suprimento ---
def test_criar_suprimento(db_session):
    suprimento = crud_suprimento.criar_suprimento(
        db_session,
        nome="Luvas Descartáveis",
        unidade_medida="caixa",
        custo_unitario=25.00,
        estoque=20.00
    )
    assert suprimento.id is not None
    assert suprimento.nome == "Luvas Descartáveis"

def test_buscar_suprimento_nome(db_session, sample_suprimento):
    found_suprimento = crud_suprimento.buscar_suprimento_nome(db_session, sample_suprimento.nome)
    assert found_suprimento == sample_suprimento

def test_atualizar_dados_suprimento(db_session, sample_suprimento):
    updated_suprimento = crud_suprimento.atualizar_dados_suprimento(
        db_session,
        sample_suprimento.id,
        estoque=75.00,
        custo_unitario=12.00
    )
    assert updated_suprimento.estoque == 75.00
    assert updated_suprimento.custo_unitario == 12.00

def test_deletar_suprimento(db_session, sample_suprimento):
    crud_suprimento.deletar_suprimento(db_session, sample_suprimento.id)
    assert crud_suprimento.buscar_suprimento_id(db_session, sample_suprimento.id) is None

# --- Testes para Máquina ---
def test_criar_maquina(db_session):
    maquina = crud_maquina.criar_maquina(
        db_session,
        nome="Máquina de Ultrassom",
        numero_serie="MU-002-ABC",
        custo_aquisicao=8000.00,
        status=StatusMaquina.MANUTENCAO
    )
    assert maquina.id is not None
    assert maquina.nome == "Máquina de Ultrassom"
    assert maquina.status == StatusMaquina.MANUTENCAO

def test_buscar_maquina_serie(db_session, sample_maquina):
    found_maquina = crud_maquina.buscar_maquina_serie(db_session, sample_maquina.numero_serie)
    assert found_maquina == sample_maquina

def test_atualizar_dados_maquina(db_session, sample_maquina):
    updated_maquina = crud_maquina.atualizar_dados_maquina(
        db_session,
        sample_maquina.id,
        status=StatusMaquina.BAIXADO,
        custo_aquisicao=14000.00
    )
    assert updated_maquina.status == StatusMaquina.BAIXADO
    assert updated_maquina.custo_aquisicao == 14000.00

def test_deletar_maquina(db_session, sample_maquina):
    crud_maquina.deletar_maquina(db_session, sample_maquina.id)
    assert crud_maquina.buscar_maquina_id(db_session, sample_maquina.id) is None

# --- Testes para Agenda ---
def test_criar_agenda(db_session, sample_funcionario, sample_cliente, sample_servico, sample_produto, sample_maquina, sample_suprimento):
    data_inicio = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0)
    data_fim = data_inicio + timedelta(hours=2)
    
    itens_agendados = [
        ItemAgendado(sample_servico, 1, sample_servico.valor_venda),
        ItemAgendado(sample_produto, 2, sample_produto.preco)
    ]
    maquinas_agendadas = [sample_maquina]
    suprimentos_utilizados = [SuprimentoAgendado(sample_suprimento, 0.5)]

    agenda = crud_agenda.criar_agenda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_hora_inicio_obj=data_inicio,
        data_hora_fim_obj=data_fim,
        itens_agendados=itens_agendados,
        maquinas_agendadas=maquinas_agendadas,
        suprimentos_utilizados=suprimentos_utilizados,
        comentario="Sessão completa"
    )

    assert agenda.id is not None
    assert agenda.funcionario_id == sample_funcionario.id
    assert agenda.cliente_id == sample_cliente.id
    assert agenda.status == AgendaStatus.AGENDADO
    assert agenda.valor_total == (sample_servico.valor_venda * 1) + (sample_produto.preco * 2)
    assert agenda.comentario == "Sessão completa"

    # Verifica itens agendados na tabela de associação
    itens_db = db_session.execute(agenda_itens_tabela.select().where(agenda_itens_tabela.c.agenda_id == agenda.id)).fetchall()
    assert len(itens_db) == 2
    assert any(item.item_tipo == 'Servico' and item.item_id == sample_servico.id for item in itens_db)
    assert any(item.item_tipo == 'Produto' and item.item_id == sample_produto.id for item in itens_db)

    # Verifica máquinas agendadas
    maquinas_db = db_session.execute(crud_agenda.agenda_maquinas_tabela.select().where(crud_agenda.agenda_maquinas_tabela.c.agenda_id == agenda.id)).fetchall()
    assert len(maquinas_db) == 1
    assert maquinas_db[0].maquina_id == sample_maquina.id

    # Verifica suprimentos agendados
    suprimentos_db = db_session.execute(agenda_suprimentos_tabela.select().where(agenda_suprimentos_tabela.c.agenda_id == agenda.id)).fetchall()
    assert len(suprimentos_db) == 1
    assert suprimentos_db[0].suprimento_id == sample_suprimento.id
    assert suprimentos_db[0].quantidade == 0.5

def test_atualizar_agenda(db_session, sample_agenda, sample_produto):
    # Adiciona um novo item e remove um existente (simulado por id_associacao)
    novo_item = ItemAgendado(sample_produto, 3, sample_produto.preco)
    
    # Para testar remoção, precisamos de um item existente com um id_associacao real.
    # No teste real, você buscaria o id_associacao do item que deseja remover.
    # Aqui, vamos simular que o item original (serviço) tem id_associacao = 1 (apenas para o teste)
    # Em um cenário real, você faria uma consulta para obter o ID da associação.
    
    # Primeiro, vamos criar uma agenda com um item para ter um id_associacao
    data_inicio_temp = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    data_fim_temp = data_inicio_temp + timedelta(hours=1)
    servico_temp = crud_servico.criar_servico(db_session, "Servico Temp", 100.0, 30.0)
    agenda_para_atualizar = crud_agenda.criar_agenda(
        db_session,
        funcionario_obj=sample_agenda.funcionario,
        cliente_obj=sample_agenda.cliente,
        data_hora_inicio_obj=data_inicio_temp,
        data_hora_fim_obj=data_fim_temp,
        itens_agendados=[ItemAgendado(servico_temp, 1, servico_temp.valor_venda)]
    )
    db_session.refresh(agenda_para_atualizar) # Garante que os itens sejam persistidos e IDs gerados

    # Obtém o id_associacao do item recém-criado
    item_existente_db = db_session.execute(agenda_itens_tabela.select().where(agenda_itens_tabela.c.agenda_id == agenda_para_atualizar.id)).fetchone()
    id_associacao_a_remover = item_existente_db.id if item_existente_db else None
    assert id_associacao_a_remover is not None

    updated_agenda = crud_agenda.atualizar_agenda(
        db_session,
        agenda_para_atualizar.id,
        itens_a_adicionar=[novo_item],
        ids_associacao_a_remover=[id_associacao_a_remover],
        comentario="Comentário atualizado",
        status=AgendaStatus.REALIZADO
    )

    assert updated_agenda.comentario == "Comentário atualizado"
    assert updated_agenda.status == AgendaStatus.REALIZADO

    # Verifica se o item antigo foi removido e o novo foi adicionado
    itens_na_agenda = db_session.execute(agenda_itens_tabela.select().where(agenda_itens_tabela.c.agenda_id == updated_agenda.id)).fetchall()
    assert len(itens_na_agenda) == 1 # Um item foi removido, um foi adicionado
    assert any(item.item_tipo == 'Produto' and item.item_id == sample_produto.id for item in itens_na_agenda)
    assert not any(item.id == id_associacao_a_remover for item in itens_na_agenda) # Verifica que o item antigo foi removido

    # Recalcula o valor total esperado
    expected_total = sample_produto.preco * 3
    assert updated_agenda.valor_total == expected_total

def test_deletar_agenda(db_session, sample_agenda):
    crud_agenda.deletar_agenda(db_session, sample_agenda.id)
    assert crud_agenda.buscar_agenda(db_session, sample_agenda.id) is None
    # Verifica se os itens associados também foram deletados
    itens_db = db_session.execute(agenda_itens_tabela.select().where(agenda_itens_tabela.c.agenda_id == sample_agenda.id)).fetchall()
    assert len(itens_db) == 0

def test_verificar_conflito_maquina(db_session, sample_maquina, sample_funcionario, sample_cliente, sample_servico):
    # Agenda 1: 10:00 - 11:00
    agenda1_start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    agenda1_end = agenda1_start + timedelta(hours=1)
    crud_agenda.criar_agenda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_hora_inicio_obj=agenda1_start,
        data_hora_fim_obj=agenda1_end,
        itens_agendados=[ItemAgendado(sample_servico, 1)],
        maquinas_agendadas=[sample_maquina]
    )

    # Conflito total: 10:30 - 11:30
    conflito_start = datetime.now().replace(hour=10, minute=30, second=0, microsecond=0)
    conflito_end = conflito_start + timedelta(hours=1)
    assert crud_agenda.verificar_conflito_maquina(db_session, sample_maquina.id, conflito_start, conflito_end)

    # Sem conflito: 11:00 - 12:00 (exatamente no final da primeira)
    no_conflito_start = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    no_conflito_end = no_conflito_start + timedelta(hours=1)
    assert not crud_agenda.verificar_conflito_maquina(db_session, sample_maquina.id, no_conflito_start, no_conflito_end)

    # Conflito ignorando a própria agenda (para atualização)
    agenda_to_update_start = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
    agenda_to_update_end = agenda_to_update_start + timedelta(hours=1)
    agenda_to_update = crud_agenda.criar_agenda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_hora_inicio_obj=agenda_to_update_start,
        data_hora_fim_obj=agenda_to_update_end,
        itens_agendados=[ItemAgendado(sample_servico, 1)],
        maquinas_agendadas=[sample_maquina]
    )
    # Não deve haver conflito se ignorarmos a própria agenda
    assert not crud_agenda.verificar_conflito_maquina(db_session, sample_maquina.id, agenda_to_update_start, agenda_to_update_end, agenda_to_update.id)


# --- Testes para Venda ---
def test_criar_venda_com_itens_avulsos(db_session, sample_funcionario, sample_cliente, sample_produto, sample_servico):
    initial_product_stock = sample_produto.estoque
    itens_venda = [
        crud_venda.ItemVenda(sample_produto, 2, sample_produto.preco),
        crud_venda.ItemVenda(sample_servico, 1, sample_servico.valor_venda)
    ]
    venda = crud_venda.criar_venda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_venda_obj=date.today(),
        itens_venda=itens_venda,
        comentario="Venda direta"
    )

    assert venda.id is not None
    assert venda.valor_total == (sample_produto.preco * 2) + (sample_servico.valor_venda * 1)
    assert venda.comentario == "Venda direta"
    assert sample_produto.estoque == initial_product_stock - 2 # Estoque deve ser atualizado

    # Verifica itens na tabela de associação
    itens_db = db_session.execute(venda_itens_tabela.select().where(venda_itens_tabela.c.venda_id == venda.id)).fetchall()
    assert len(itens_db) == 2
    assert any(item.item_tipo == 'Produto' and item.item_id == sample_produto.id for item in itens_db)
    assert any(item.item_tipo == 'Servico' and item.item_id == sample_servico.id for item in itens_db)

def test_criar_venda_a_partir_de_agenda(db_session, sample_agenda, sample_suprimento):
    # Adiciona um suprimento à agenda para testar a baixa de estoque
    db_session.execute(crud_agenda.agenda_suprimentos_tabela.insert().values(
        agenda_id=sample_agenda.id, suprimento_id=sample_suprimento.id, quantidade=0.1
    ))
    db_session.commit()
    db_session.refresh(sample_agenda)
    db_session.refresh(sample_suprimento)

    initial_suprimento_stock = sample_suprimento.estoque
    initial_agenda_status = sample_agenda.status

    venda = crud_venda.criar_venda(
        db_session,
        funcionario_obj=sample_agenda.funcionario,
        cliente_obj=sample_agenda.cliente,
        data_venda_obj=date.today(),
        itens_venda=[], # Itens virão da agenda
        agenda_obj=sample_agenda
    )

    assert venda.id is not None
    assert venda.agenda_id == sample_agenda.id
    assert venda.valor_total == sample_agenda.valor_total
    assert sample_agenda.status == AgendaStatus.REALIZADO # Status da agenda deve mudar
    assert sample_suprimento.estoque == initial_suprimento_stock - 0.1 # Estoque do suprimento deve ser baixado

def test_deletar_venda(db_session, sample_venda, sample_produto):
    initial_product_stock = sample_produto.estoque
    crud_venda.deletar_venda(db_session, sample_venda.id)
    assert crud_venda.buscar_venda(db_session, sample_venda.id) is None
    assert sample_produto.estoque == initial_product_stock + 2 # Estoque deve ser revertido

    # Verifica se os itens da venda foram deletados
    itens_db = db_session.execute(venda_itens_tabela.select().where(venda_itens_tabela.c.venda_id == sample_venda.id)).fetchall()
    assert len(itens_db) == 0

def test_deletar_venda_com_agenda(db_session, sample_agenda, sample_funcionario, sample_cliente):
    # Cria uma venda a partir da agenda
    venda_com_agenda = crud_venda.criar_venda(
        db_session,
        funcionario_obj=sample_funcionario,
        cliente_obj=sample_cliente,
        data_venda_obj=date.today(),
        itens_venda=[],
        agenda_obj=sample_agenda
    )
    db_session.refresh(sample_agenda)
    assert sample_agenda.status == AgendaStatus.REALIZADO

    crud_venda.deletar_venda(db_session, venda_com_agenda.id)
    db_session.refresh(sample_agenda)
    assert sample_agenda.status == AgendaStatus.AGENDADO # Status da agenda deve ser revertido

def test_atualizar_dados_venda(db_session, sample_venda):
    new_date = date(2023, 1, 1)
    updated_venda = crud_venda.atualizar_dados_venda(
        db_session,
        sample_venda.id,
        data_venda=new_date,
        comentario="Comentário da venda atualizado"
    )
    assert updated_venda.data_venda == new_date
    assert updated_venda.comentario == "Comentário da venda atualizado"

# --- Testes para Despesa ---
def test_criar_compra_produto(db_session, sample_fornecedor, sample_produto):
    initial_stock = sample_produto.estoque
    initial_cost = sample_produto.custo_compra
    
    crud_despesa.criar_compra(
        db_session,
        fornecedor_obj=sample_fornecedor,
        item_comprado=sample_produto,
        quantidade=10.0,
        valor_unitario=45.00,
        data_despesa_obj=date.today()
    )
    db_session.refresh(sample_produto) # Recarrega o produto para obter o estoque atualizado
    
    assert sample_produto.estoque == initial_stock + 10
    assert sample_produto.custo_compra == 45.00
    assert len(sample_produto.historico_custo_compra) == 1
    assert sample_produto.historico_custo_compra[0]['valor_unitario'] == 45.00

def test_criar_compra_suprimento(db_session, sample_fornecedor, sample_suprimento):
    initial_stock = sample_suprimento.estoque
    initial_cost = sample_suprimento.custo_unitario

    crud_despesa.criar_compra(
        db_session,
        fornecedor_obj=sample_fornecedor,
        item_comprado=sample_suprimento,
        quantidade=5.0,
        valor_unitario=9.00,
        data_despesa_obj=date.today()
    )
    db_session.refresh(sample_suprimento)

    assert sample_suprimento.estoque == initial_stock + 5
    assert sample_suprimento.custo_unitario == 9.00
    assert len(sample_suprimento.historico_custo_compra) == 1
    assert sample_suprimento.historico_custo_compra[0]['valor_unitario'] == 9.00

def test_criar_fixo_terceiro(db_session, sample_fornecedor):
    despesa = crud_despesa.criar_fixo_terceiro(
        db_session,
        valor=1000.00,
        tipo_despesa_str="Aluguel",
        data_despesa_obj=date.today(),
        fornecedor_obj=sample_fornecedor
    )
    assert despesa.valor_total == 1000.00
    assert despesa.tipo_despesa_str == "Aluguel"
    assert despesa.fornecedor_obj == sample_fornecedor

def test_criar_salario(db_session, sample_funcionario):
    despesa = crud_despesa.criar_salario(
        db_session,
        funcionario_obj=sample_funcionario,
        salario_bruto=3000.00,
        descontos=500.00,
        data_despesa_obj=date.today()
    )
    assert despesa.valor_total == 2500.00
    assert despesa.funcionario_obj == sample_funcionario

def test_criar_comissao(db_session, sample_funcionario):
    despesa = crud_despesa.criar_comissao(
        db_session,
        funcionario_obj=sample_funcionario,
        valor_soma_servicos=1000.00,
        valor_soma_produtos=500.00,
        taxa_servicos=0.1,
        taxa_produtos=0.05,
        data_despesa_obj=date.today()
    )
    assert despesa.valor_total == (1000 * 0.1) + (500 * 0.05)
    assert despesa.valor_total == 100.0 + 25.0
    assert despesa.valor_total == 125.0

def test_criar_outros(db_session):
    despesa = crud_despesa.criar_outros(
        db_session,
        valor=200.00,
        tipo_despesa_str="Material de Escritório",
        data_despesa_obj=date.today()
    )
    assert despesa.valor_total == 200.00
    assert despesa.tipo_despesa_str == "Material de Escritório"

def test_deletar_despesa(db_session, sample_fornecedor):
    despesa = crud_despesa.criar_fixo_terceiro(
        db_session,
        valor=100.00,
        tipo_despesa_str="Internet",
        data_despesa_obj=date.today(),
        fornecedor_obj=sample_fornecedor
    )
    crud_despesa.deletar_despesa(db_session, despesa.id)
    assert db_session.query(crud_despesa.Despesa).get(despesa.id) is None

def test_atualizar_dados_despesa_compra(db_session, sample_fornecedor, sample_produto):
    despesa_compra = crud_despesa.criar_compra(
        db_session,
        fornecedor_obj=sample_fornecedor,
        item_comprado=sample_produto,
        quantidade=10.0,
        valor_unitario=40.00,
        data_despesa_obj=date.today()
    )
    updated_despesa = crud_despesa.atualizar_dados_despesa(
        db_session,
        despesa_compra.id,
        quantidade=12.0,
        valor_unitario=42.00
    )
    assert updated_despesa.quantidade == 12.0
    assert updated_despesa.valor_unitario == 42.00
    assert updated_despesa.valor_total == 12.0 * 42.00

def test_atualizar_dados_despesa_salario(db_session, sample_funcionario):
    despesa_salario = crud_despesa.criar_salario(
        db_session,
        funcionario_obj=sample_funcionario,
        salario_bruto=3000.00,
        descontos=500.00,
        data_despesa_obj=date.today()
    )
    updated_despesa = crud_despesa.atualizar_dados_despesa(
        db_session,
        despesa_salario.id,
        salario_bruto=3200.00,
        descontos=600.00
    )
    assert updated_despesa.salario_bruto == 3200.00
    assert updated_despesa.descontos == 600.00
    assert updated_despesa.valor_total == 3200.00 - 600.00

def test_atualizar_dados_despesa_comissao(db_session, sample_funcionario):
    despesa_comissao = crud_despesa.criar_comissao(
        db_session,
        funcionario_obj=sample_funcionario,
        valor_soma_servicos=1000.00,
        valor_soma_produtos=500.00,
        taxa_servicos=0.1,
        taxa_produtos=0.05,
        data_despesa_obj=date.today()
    )
    updated_despesa = crud_despesa.atualizar_dados_despesa(
        db_session,
        despesa_comissao.id,
        valor_soma_servicos=1200.00,
        taxa_servicos=0.12
    )
    assert updated_despesa.valor_soma_servicos == 1200.00
    assert updated_despesa.taxa_servicos == 0.12
    assert updated_despesa.valor_total == (1200 * 0.12) + (500 * 0.05)

def test_listar_despesas_por_tipo(db_session, sample_fornecedor, sample_funcionario):
    crud_despesa.criar_fixo_terceiro(db_session, 500.0, "Aluguel", date(2023, 1, 1))
    crud_despesa.criar_salario(db_session, sample_funcionario, 3000.0, 500.0, date(2023, 1, 15))
    crud_despesa.criar_compra(db_session, sample_fornecedor, "Material", 1, 100.0, date(2023, 1, 20))

    despesas_fixas = crud_despesa.listar_despesas(db_session, tipos=['fixo_terceiro'])
    assert len(despesas_fixas) == 1
    assert isinstance(despesas_fixas[0], crud_despesa.FixoTerceiro)

    despesas_salario_compra = crud_despesa.listar_despesas(db_session, tipos=['salario', 'compra'])
    assert len(despesas_salario_compra) == 2
    assert any(isinstance(d, crud_despesa.Salario) for d in despesas_salario_compra)
    assert any(isinstance(d, crud_despesa.Compra) for d in despesas_salario_compra)

