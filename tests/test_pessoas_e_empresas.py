import pytest
from datetime import date, datetime, timedelta
# Importa as classes dos módulos que serão testados
import info
import pessoa
import cliente
import funcionario
import fornecedor

# --- Fixtures Reutilizáveis ---
@pytest.fixture
def info_contato_valida():
    # Retorna uma instância válida de Informacao para ser usada nos testes.
    return info.Informacao(
        telefone="11987654321",
        email="teste@dominio.com",
        endereco="Rua Teste, 123, Bairro Teste, Cidade Teste, SP",
        redes_sociais="instagram.com/teste"
    )

@pytest.fixture
def cpf_valido_aleatorio():
    # Retorna um CPF válido gerado aleatoriamente.
    return pessoa.gerar_cpf_valido()

@pytest.fixture
def cnpj_valido_aleatorio():
    # Retorna um CNPJ válido gerado aleatoriamente.
    return pessoa.gerar_cnpj_valido()

# --- Testes para a classe Informacao (info.py) ---

def test_informacao_criacao_valida(info_contato_valida):
    # Testa a criação de uma instância válida de Informacao.
    assert isinstance(info_contato_valida, info.Informacao)
    assert info_contato_valida.telefone == "11 98765 4321"
    assert info_contato_valida.email == "teste@dominio.com"
    assert info_contato_valida.endereco["nome_rua"] == "Rua Teste"
    assert info_contato_valida.redes_sociais == "instagram.com/teste"

def test_informacao_telefone_invalido():
    # Testa a validação de telefone inválido (ValueError).
    with pytest.raises(ValueError, match="Formato de número de telefone brasileiro inválido."):
        info.Informacao("123", "email@test.com", "Rua Teste, 123", "redes")
    with pytest.raises(ValueError, match="Formato de número de telefone brasileiro inválido."):
        info.Informacao("99999999999999999", "email@test.com", "Rua Teste, 123", "redes")
    with pytest.raises(ValueError, match="Formato de número de telefone brasileiro inválido."):
        info.Informacao("abcdefgh", "email@test.com", "Rua Teste, 123", "redes")
    with pytest.raises(ValueError, match="Formato de número de telefone brasileiro inválido."):
        info.Informacao("", "email@test.com", "Rua Teste, 123", "redes") # Telefone vazio
    with pytest.raises(ValueError, match=r"Número brasileiro inválido: DDD '01' inválido \(não pode começar ou terminar com 0\)\."):
        info.Informacao("01987654321", "email@test.com", "Rua Teste, 123", "redes") # DDD inválido (começa com 0)
    with pytest.raises(ValueError, match=r"Número brasileiro inválido: DDD '10' inválido \(não pode começar ou terminar com 0\)\."):
        info.Informacao("10987654321", "email@test.com", "Rua Teste, 123", "redes") # DDD inválido (termina com 0)
    with pytest.raises(ValueError, match=r"Número brasileiro inválido: Celular de 9 dígitos deve começar com 6, 7, 8 ou 9\."):
        info.Informacao("11587654321", "email@test.com", "Rua Teste, 123", "redes") # Celular de 9 dígitos começando com 5


def test_informacao_email_invalido():
    # Testa a validação de email inválido (ValueError).
    with pytest.raises(ValueError, match="Formato de e-mail inválido."):
        info.Informacao("11987654321", "emailinvalido", "Rua Teste, 123", "redes")
    with pytest.raises(ValueError, match="Formato de e-mail inválido."):
        info.Informacao("11987654321", "email@.com", "Rua Teste, 123", "redes")
    with pytest.raises(ValueError, match="Formato de e-mail inválido."):
        info.Informacao("11987654321", "", "Rua Teste, 123", "redes") # Email vazio

def test_informacao_endereco_invalido():
    # Testa a validação de endereço inválido (ValueError) com o padrão flexível.
    # "Endereco Invalido" (sem vírgula) deve falhar
    with pytest.raises(ValueError, match=r"Formato de endereço inválido\. Esperado: 'Nome da rua, número' ou 'Nome da rua, número, bairro, cidade, estado'"):
        info.Informacao("11987654321", "email@test.com", "Endereco Invalido", "redes")
    # "Rua Teste 123" (sem vírgula depois da rua) deve falhar
    with pytest.raises(ValueError, match=r"Formato de endereço inválido\. Esperado: 'Nome da rua, número' ou 'Nome da rua, número, bairro, cidade, estado'"):
        info.Informacao("11987654321", "email@test.com", "Rua Teste 123", "redes")
    # "Rua Teste, 123, Bairro, Cidade" (faltando o estado) deve falhar
    with pytest.raises(ValueError, match=r"Formato de endereço inválido\. Esperado: 'Nome da rua, número' ou 'Nome da rua, número, bairro, cidade, estado'"):
        info.Informacao("11987654321", "email@test.com", "Rua Teste, 123, Bairro, Cidade", "redes")
    with pytest.raises(ValueError, match=r"Formato de endereço inválido\. Esperado: 'Nome da rua, número' ou 'Nome da rua, número, bairro, cidade, estado'"):
        info.Informacao("11987654321", "email@test.com", "", "redes") # Endereço vazio

def test_informacao_endereco_valido_flexivel():
    # Testa a criação de endereço válido no formato flexível (apenas rua e número).
    info_flex = info.Informacao("11987654321", "flex@email.com", "Rua Flex, 456", "redes")
    assert info_flex.endereco["nome_rua"] == "Rua Flex"
    assert info_flex.endereco["numero"] == "456"
    assert info_flex.endereco["bairro"] is None
    assert info_flex.endereco["cidade"] is None
    assert info_flex.endereco["estado"] is None

def test_informacao_atualizar_telefone(info_contato_valida):
    # Testa a atualização do telefone.
    info_contato_valida.telefone = "21998765432"
    assert info_contato_valida.telefone == "21 99876 5432"
    with pytest.raises(ValueError, match="Formato de número de telefone brasileiro inválido."):
        info_contato_valida.telefone = "invalido"

def test_informacao_atualizar_email(info_contato_valida):
    # Testa a atualização do email.
    info_contato_valida.email = "novo.email@teste.org"
    assert info_contato_valida.email == "novo.email@teste.org"
    with pytest.raises(ValueError, match="Formato de e-mail inválido."):
        info_contato_valida.email = "email_errado"

def test_informacao_atualizar_endereco(info_contato_valida):
    # Testa a atualização do endereço.
    info_contato_valida.endereco = "Av. Principal, 456, Centro, Rio de Janeiro, RJ"
    assert info_contato_valida.endereco["nome_rua"] == "Av. Principal"
    assert info_contato_valida.endereco["estado"] == "RJ"
    with pytest.raises(ValueError, match=r"Formato de endereço inválido\."):
        info_contato_valida.endereco = "Endereco Invalido"

def test_informacao_atualizar_redes_sociais(info_contato_valida):
    # Testa a atualização das redes sociais.
    info_contato_valida.redes_sociais = "twitter.com/teste"
    assert info_contato_valida.redes_sociais == "twitter.com/teste"
    info_contato_valida.redes_sociais = ""
    assert info_contato_valida.redes_sociais == ""

def test_informacao_validar_e_formatar_telefone_brasileiro_validos():
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("11987654321") == "11 98765 4321" # Celular
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("(21)98765-4321") == "21 98765 4321" # Celular com formatação
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+55 11 98765 4321") == "11 98765 4321" # Celular com DDI
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("4130201000") == "41 3020 1000" # Fixo
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("021998765432") == "21 99876 5432" # Celular com 0 inicial no DDD
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("1112345678") == "11 1234 5678" # Fixo
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("99999999999") == "99 99999 9999" # Celular (DDD 99, numero 999999999)
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+1 234 567-8900") == "+1 234 567-8900" # Estrangeiro
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+44 7911 123456") == "+44 7911 123456" # Estrangeiro

def test_informacao_validar_e_formatar_telefone_brasileiro_invalidos():
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("123") is None # Muito curto
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("119876543210") is None # Muito longo para celular (12 digitos)
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("abcde12345") is None # Caracteres inválidos
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("1191234567") is None # Celular mas 8 dígitos, muito curto
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("11223456789") is None # Fixo de 8 dígitos com 9 inicial (agora inválido)
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("111234567") is None # Fixo com 7 dígitos (muito curto)
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("01198765432") is None # DDD 01 inválido
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("11") is None # DDD sem número
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+55 11 1234567") is None # DDI brasileiro, mas número local muito curto
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+55 11 9123456789") is None # DDI nacional, mas número local muito longo
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+54") is None # DDI sem número restante
    assert info.Informacao.validar_e_formatar_telefone_brasileiro("+54 ") is None # DDI com espaço e sem número restante

# --- Testes para a classe Pessoa (pessoa.py) ---

def test_pessoa_criacao_valida(cpf_valido_aleatorio):
    # Testa a criação de uma instância válida de Pessoa.
    p = pessoa.Pessoa("Fulano de Tal", "01/01/2000", cpf_valido_aleatorio)
    assert p.nome == "Fulano de Tal"
    assert p.nascimento == date(2000, 1, 1)
    assert p.cpf == cpf_valido_aleatorio
    assert p.idade >= (date.today().year - 2000) - (1 if date.today().month < 1 or (date.today().month == 1 and date.today().day < 1) else 0)

def test_pessoa_nome_invalido(cpf_valido_aleatorio):
    # Testa a validação de nome inválido (ValueError).
    with pytest.raises(ValueError, match="Formato de nome inválido."):
        pessoa.Pessoa("Fulano", "01/01/2000", cpf_valido_aleatorio) # Apenas um nome
    with pytest.raises(ValueError, match="Formato de nome inválido."):
        pessoa.Pessoa("  ", "01/01/2000", cpf_valido_aleatorio) # Nome vazio
    with pytest.raises(ValueError, match="Formato de nome inválido."):
        pessoa.Pessoa("123 Silva", "01/01/2000", cpf_valido_aleatorio) # Nome com números
    with pytest.raises(ValueError, match="Formato de nome inválido."):
        p = pessoa.Pessoa("Nome Teste", "01/01/2000", cpf_valido_aleatorio)
        p.nome = "Um Nome" # Setter também deve validar
        assert p.nome == "Um Nome"

def test_pessoa_nascimento_invalido(cpf_valido_aleatorio):
    # Testa a validação de data de nascimento inválida (ValueError).
    with pytest.raises(ValueError, match="Data de nascimento não pode ser no futuro."):
        pessoa.Pessoa("Fulano de Tal", (date.today() + timedelta(days=1)).strftime("%d/%m/%Y"), cpf_valido_aleatorio)
    with pytest.raises(ValueError, match="Data de nascimento indica uma idade de .* anos, o que excede o máximo permitido."):
        pessoa.Pessoa("Fulano de Tal", "01/01/1800", cpf_valido_aleatorio)
    with pytest.raises(ValueError, match="Formato de data inválido."):
        pessoa.Pessoa("Fulano de Tal", "data invalida", cpf_valido_aleatorio)
    with pytest.raises(ValueError, match="Data inválida: month must be in 1..12."):
        p = pessoa.Pessoa("Fulano de Tal", "01/01/2000", cpf_valido_aleatorio)
        p.nascimento = "01/13/2000" # Setter também deve validar

def test_pessoa_cpf_invalido():
    # Testa a validação de CPF inválido (ValueError).
    with pytest.raises(ValueError, match="Formato de CPF inválido."):
        pessoa.Pessoa("Fulano de Tal", "01/01/2000", "123") # Poucos dígitos
    with pytest.raises(ValueError, match="Formato de CPF inválido."):
        pessoa.Pessoa("Fulano de Tal", "01/01/2000", "123.456.789-0") # Formato incorreto
    with pytest.raises(ValueError, match="CPF inválido: Dígitos verificadores não correspondem ou padrão inválido."):
        pessoa.Pessoa("Fulano de Tal", "01/01/2000", "111.111.111-11") # Todos os dígitos iguais
    with pytest.raises(ValueError, match="CPF inválido: Dígitos verificadores não correspondem ou padrão inválido."):
        pessoa.Pessoa("Fulano de Tal", "01/01/2000", "12345678900") # Dígitos verificadores errados
    with pytest.raises(ValueError, match="Formato de CPF inválido."):
        p = pessoa.Pessoa("Fulano de Tal", "01/01/2000", pessoa.gerar_cpf_valido())
        p.cpf = "invalido" # Setter também deve validar

def test_pessoa_atualizar_nome(cpf_valido_aleatorio):
    # Testa a atualização do nome de Pessoa.
    p = pessoa.Pessoa("Nome Antigo", "01/01/2000", cpf_valido_aleatorio)
    p.nome = "Novo Nome Completo"
    assert p.nome == "Novo Nome Completo"

def test_pessoa_atualizar_nascimento(cpf_valido_aleatorio):
    # Testa a atualização da data de nascimento de Pessoa.
    p = pessoa.Pessoa("Nome Teste", "01/01/2000", cpf_valido_aleatorio)
    p.nascimento = "15/05/1990"
    assert p.nascimento == date(1990, 5, 15)

def test_pessoa_atualizar_cpf(cpf_valido_aleatorio):
    # Testa a atualização do CPF de Pessoa.
    p = pessoa.Pessoa("Nome Teste", "01/01/2000", cpf_valido_aleatorio)
    novo_cpf = pessoa.gerar_cpf_valido()
    p.cpf = novo_cpf
    assert p.cpf == novo_cpf

def test_pessoa_eh_cpf_valido_digitos_validos():
    # Testes para CPFs válidos
    assert pessoa.Pessoa._eh_cpf_valido_digitos("12345678909") is True
    assert pessoa.Pessoa._eh_cpf_valido_digitos("00000000000") is False # Todos iguais

def test_pessoa_eh_cpf_valido_digitos_invalidos():
    # Testes para CPFs inválidos
    assert pessoa.Pessoa._eh_cpf_valido_digitos("123") is False # Curto
    assert pessoa.Pessoa._eh_cpf_valido_digitos("123456789098") is False # Longo
    assert pessoa.Pessoa._eh_cpf_valido_digitos("12345678901") is False # Dígito verificador incorreto
    assert pessoa.Pessoa._eh_cpf_valido_digitos("11111111111") is False # Todos iguais
    assert pessoa.Pessoa._eh_cpf_valido_digitos("abcdefghijk") is False # Não dígitos
    assert pessoa.Pessoa._eh_cpf_valido_digitos("14227845053") is False 

def test_pessoa_parse_data_flexivel_date_validos():
    # Testes para formatos de data válidos
    assert pessoa.Pessoa._parse_data_flexivel("01/01/2000", is_datetime=False) == date(2000, 1, 1)
    assert pessoa.Pessoa._parse_data_flexivel("15-03-1995", is_datetime=False) == date(1995, 3, 15)
    assert pessoa.Pessoa._parse_data_flexivel("28022023", is_datetime=False) == date(2023, 2, 28)
    assert pessoa.Pessoa._parse_data_flexivel("05 06 99", is_datetime=False) == date(1999, 6, 5) # Ano com 2 dígitos
    assert pessoa.Pessoa._parse_data_flexivel("05 06 2099", is_datetime=False) == date(2099, 6, 5) # Ano no futuro distante, 4 dígitos

def test_pessoa_parse_data_flexivel_datetime_validos():
    # Testes para formatos de data/hora válidos
    assert pessoa.Pessoa._parse_data_flexivel("01/01/2000 10:30", is_datetime=True) == datetime(2000, 1, 1, 10, 30)
    assert pessoa.Pessoa._parse_data_flexivel("15-03-1995 23:59", is_datetime=True) == datetime(1995, 3, 15, 23, 59)
    assert pessoa.Pessoa._parse_data_flexivel("28022023 00:00", is_datetime=True) == datetime(2023, 2, 28, 0, 0)

def test_pessoa_parse_data_flexivel_invalidos():
    # Testes para formatos inválidos
    with pytest.raises(ValueError, match="Formato de data inválido."):
        pessoa.Pessoa._parse_data_flexivel("data invalida", is_datetime=False)
    with pytest.raises(ValueError, match="Formato de data/hora inválido."):
        pessoa.Pessoa._parse_data_flexivel("01/01/2000", is_datetime=True) # Faltando hora
    with pytest.raises(ValueError, match="Data inválida: day is out of range for month."):
        pessoa.Pessoa._parse_data_flexivel("30/02/2023", is_datetime=False) # Data inválida
    with pytest.raises(ValueError, match="Data inválida: hour must be in 0..23."):
        pessoa.Pessoa._parse_data_flexivel("01/01/2000 25:00", is_datetime=True) # Hora inválida
    with pytest.raises(ValueError, match="Data inválida: minute must be in 0..59."):
        pessoa.Pessoa._parse_data_flexivel("01/01/2000 10:65", is_datetime=True) # Minuto inválido

# --- Testes para a classe Cliente (cliente.py) ---

def test_cliente_criacao_valida(info_contato_valida, cpf_valido_aleatorio):
    # Testa a criação de um cliente válido.
    id_inicial = cliente.Cliente._proximo_id_disponivel
    c = cliente.Cliente(None, "Cliente Teste", "10/10/1990", cpf_valido_aleatorio, info_contato_valida)
    assert c.id == id_inicial
    assert c.nome == "Cliente Teste"
    assert c.cpf == cpf_valido_aleatorio
    assert c.info_contato == info_contato_valida
    assert cliente.Cliente.buscar_cliente_id(c.id) == c
    assert cliente.Cliente.buscar_cliente(c.cpf) == c

def test_cliente_criacao_id_especifico(info_contato_valida, cpf_valido_aleatorio):
    # Testa a criação de um cliente com ID específico.
    c = cliente.Cliente(100, "Cliente ID", "10/10/1990", cpf_valido_aleatorio, info_contato_valida)
    assert c.id == 100
    assert cliente.Cliente.buscar_cliente_id(100) == c

def test_cliente_colisao_cpf(info_contato_valida, cpf_valido_aleatorio):
    # Testa a colisão de CPF ao criar um novo cliente.
    cliente.Cliente(None, "Cliente Um", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match=f"Cliente com CPF {cpf_valido_aleatorio} já existe."):
        cliente.Cliente(None, "Cliente Dois", "02/02/1990", cpf_valido_aleatorio, info_contato_valida)

def test_cliente_colisao_id(info_contato_valida, cpf_valido_aleatorio):
    # Testa a colisão de ID ao criar um novo cliente.
    cliente.Cliente(1, "Cliente Um", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="Já existe um cliente com o ID 1."):
        cliente.Cliente(1, "Cliente Dois", "02/02/1990", pessoa.gerar_cpf_valido(), info_contato_valida)

def test_cliente_id_invalido(info_contato_valida, cpf_valido_aleatorio):
    # Testa a criação de cliente com ID inválido.
    with pytest.raises(ValueError, match="O ID do cliente deve ser um número inteiro positivo."):
        cliente.Cliente(0, "Cliente Zero", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="O ID do cliente deve ser um número inteiro positivo."):
        cliente.Cliente(-5, "Cliente Negativo", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="O ID do cliente deve ser um número inteiro positivo."):
        cliente.Cliente("abc", "Cliente String", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)

def test_cliente_info_contato_tipo_invalido(cpf_valido_aleatorio):
    # Testa a criação de cliente com tipo de info_contato inválido.
    with pytest.raises(TypeError, match="A informação de contato deve ser uma instância da classe Informacao."):
        cliente.Cliente(None, "Cliente Invalido", "01/01/1990", cpf_valido_aleatorio, "nao_info")

def test_cliente_buscar_cliente(info_contato_valida, cpf_valido_aleatorio):
    # Testa a busca de cliente por CPF.
    c = cliente.Cliente(None, "Cliente Busca", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    found_c = cliente.Cliente.buscar_cliente(cpf_valido_aleatorio)
    assert found_c == c
    assert cliente.Cliente.buscar_cliente("999.999.999-99") is None
    assert cliente.Cliente.buscar_cliente("cpf_invalido") is None # Teste com formato inválido de CPF na busca

def test_cliente_buscar_cliente_id(info_contato_valida, cpf_valido_aleatorio):
    # Testa a busca de cliente por ID.
    c = cliente.Cliente(None, "Cliente Busca ID", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    found_c = cliente.Cliente.buscar_cliente_id(c.id)
    assert found_c == c
    assert cliente.Cliente.buscar_cliente_id(9999) is None

def test_cliente_buscar_cliente_por_nome_exato(info_contato_valida, cpf_valido_aleatorio):
    # Testa a busca de cliente por nome exato.
    c = cliente.Cliente(None, "Cliente Exato", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    found_c = cliente.Cliente.buscar_cliente_por_nome_exato("Cliente Exato")
    assert found_c == c
    assert cliente.Cliente.buscar_cliente_por_nome_exato("cliente exato") == c # Case-insensitive
    assert cliente.Cliente.buscar_cliente_por_nome_exato("Cliente Inexistente") is None

def test_cliente_buscar_clientes_por_nome_parcial(info_contato_valida, cpf_valido_aleatorio):
    # Testa a busca de clientes por nome parcial.
    c1 = cliente.Cliente(None, "Ana Clara", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    c2 = cliente.Cliente(None, "Joao Ana", "01/01/1990", pessoa.gerar_cpf_valido(), info_contato_valida)
    c3 = cliente.Cliente(None, "Maria Silva", "01/01/1990", pessoa.gerar_cpf_valido(), info_contato_valida)

    results = cliente.Cliente.buscar_clientes_por_nome_parcial("Ana")
    assert len(results) == 2
    assert c1 in results
    assert c2 in results

    results_lower = cliente.Cliente.buscar_clientes_por_nome_parcial("ana")
    assert len(results_lower) == 2
    assert c1 in results_lower
    assert c2 in results_lower

    assert not cliente.Cliente.buscar_clientes_por_nome_parcial("Inexistente")

def test_cliente_listar_clientes(info_contato_valida, cpf_valido_aleatorio):
    # Testa a listagem de todos os clientes.
    c1 = cliente.Cliente(None, "Listar Um", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    c2 = cliente.Cliente(None, "Listar Dois", "01/01/1990", pessoa.gerar_cpf_valido(), info_contato_valida)
    all_clients = cliente.Cliente.listar_clientes()
    assert len(all_clients) == 2
    assert c1 in all_clients
    assert c2 in all_clients

def test_cliente_atualizar_dados_cliente(info_contato_valida, cpf_valido_aleatorio):
    # Testa a atualização de dados de um cliente.
    c = cliente.Cliente(None, "Cliente Antigo", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)

    novo_info_contato = info.Informacao(
        telefone="11999998888", # Número de telefone válido, será formatado para "11 99999 8888"
        email="novo.email@cliente.com",
        endereco="Rua Nova, 456, Outro Bairro, Outra Cidade, MG",
        redes_sociais=""
    )

    cliente.Cliente.atualizar_dados_cliente(c.id, nome="Cliente Novo", nascimento="05/05/1985", info_contato=novo_info_contato)
    
    assert c.nome == "Cliente Novo"
    assert c.nascimento == date(1985, 5, 5)
    assert c.info_contato.telefone == "11999998888"
    assert c.info_contato.email == "novo.email@cliente.com"
    assert c.info_contato.endereco["nome_rua"] == "Rua Nova"

def test_cliente_atualizar_dados_cliente_nao_encontrado():
    # Testa a atualização de dados de um cliente inexistente.
    with pytest.raises(ValueError, match="Cliente com ID 999 não encontrado para atualização."):
        cliente.Cliente.atualizar_dados_cliente(999, nome="Inexistente")

def test_cliente_atualizar_dados_cliente_id_e_cpf_nao_alteraveis(info_contato_valida, cpf_valido_aleatorio):
    # Testa que ID e CPF não podem ser alterados via atualizar_dados_cliente.
    c = cliente.Cliente(None, "Cliente Teste", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    
    # O método não deve levantar erro, mas imprimir aviso e não alterar
    cliente.Cliente.atualizar_dados_cliente(c.id, id=999, cpf=pessoa.gerar_cpf_valido()) #tentativa de alteração
    assert c.id != 999
    assert c.cpf == cpf_valido_aleatorio # O CPF não deve ter sido alterado

def test_cliente_atualizar_dados_cliente_info_contato_tipo_invalido(info_contato_valida, cpf_valido_aleatorio):
    # Testa a atualização de info_contato com tipo inválido.
    c = cliente.Cliente(None, "Cliente Teste", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    with pytest.raises(TypeError, match="A informação de contato deve ser uma instância da classe Informacao."):
        cliente.Cliente.atualizar_dados_cliente(c.id, info_contato="string")

def test_cliente_atualizar_cpf_cliente_invalido(info_contato_valida, cpf_valido_aleatorio):
    # Testa a atualização do CPF de um cliente com CPF inválido.
    c = cliente.Cliente(None, "Cliente CPF Inv", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match=r"Erro ao atualizar CPF: Formato de CPF inválido\. Aceito: '999\.999\.999-99' ou '99999999999'\."):
        cliente.Cliente.atualizar_cpf_cliente(c.id, "123")

def test_cliente_atualizar_cpf_cliente_colisao(info_contato_valida, cpf_valido_aleatorio):
    # Testa a atualização do CPF de um cliente com CPF já existente em outro cliente.
    c1 = cliente.Cliente(None, "Cliente Um", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    cpf_duplicado = pessoa.gerar_cpf_valido()
    c2 = cliente.Cliente(None, "Cliente Dois", "02/02/1990", cpf_duplicado, info_contato_valida)

    with pytest.raises(ValueError, match=f"Já existe outro cliente com o CPF {cpf_duplicado}."):
        cliente.Cliente.atualizar_cpf_cliente(c1.id, cpf_duplicado)

def test_cliente_atualizar_cpf_cliente_nao_encontrado():
    # Testa a atualização de CPF para um cliente inexistente.
    with pytest.raises(ValueError, match="Cliente com ID 999 não encontrado para atualização de CPF."):
        cliente.Cliente.atualizar_cpf_cliente(999, pessoa.gerar_cpf_valido())

def test_cliente_deletar_cliente(info_contato_valida, cpf_valido_aleatorio):
    # Testa a deleção de um cliente.
    c = cliente.Cliente(None, "Cliente Deletar", "01/01/1990", cpf_valido_aleatorio, info_contato_valida)
    cliente.Cliente.deletar_cliente(c.id)
    assert cliente.Cliente.buscar_cliente_id(c.id) is None
    assert cliente.Cliente.buscar_cliente(c.cpf) is None
    assert c not in cliente.Cliente.listar_clientes()

def test_cliente_deletar_cliente_nao_encontrado():
    # Testa a deleção de um cliente inexistente.
    with pytest.raises(ValueError, match="Cliente com ID 999 não encontrado para exclusão."):
        cliente.Cliente.deletar_cliente(999)

def test_cliente_formatar_cpf_para_busca():
    # Testar _formatar_cpf_para_busca
    assert cliente.Cliente._formatar_cpf_para_busca("12345678909") == "123.456.789-09"
    assert cliente.Cliente._formatar_cpf_para_busca("123.456.789-09") == "123.456.789-09"
    assert cliente.Cliente._formatar_cpf_para_busca("123456789") is None # CPF curto
    assert cliente.Cliente._formatar_cpf_para_busca("123456789098") is None # CPF longo

def test_cliente_inicializar_proximo_id_vazio():
    # Testa _inicializar_proximo_id quando a lista está vazia
    cliente.Cliente._clientes_por_id.clear()
    cliente.Cliente._proximo_id_disponivel = 0 # Reset para garantir
    cliente.Cliente._inicializar_proximo_id()
    assert cliente.Cliente._proximo_id_disponivel == 1

def test_cliente_inicializar_proximo_id_populado(info_contato_valida):
    # Testa _inicializar_proximo_id quando a lista está populada
    c1 = cliente.Cliente(10, "Cliente A", "01/01/1990", pessoa.gerar_cpf_valido(), info_contato_valida)
    c2 = cliente.Cliente(5, "Cliente B", "01/01/1990", pessoa.gerar_cpf_valido(), info_contato_valida)
    cliente.Cliente._proximo_id_disponivel = 0 # Reset para garantir
    cliente.Cliente._inicializar_proximo_id()
    assert cliente.Cliente._proximo_id_disponivel == 11 # Max ID + 1

# --- Testes para a classe Funcionario (funcionario.py) ---

@pytest.fixture
def funcionario_valido(info_contato_valida, cpf_valido_aleatorio):
    # Retorna uma instância válida de Funcionario para ser usada nos testes.
    id_inicial = funcionario.Funcionario._proximo_id_disponivel
    return funcionario.Funcionario(
        None, "Funcionario Teste Completo", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
        info_contato_valida, 2500.00, "01/01/2020", None, "12345678901"
    )

def test_funcionario_criacao_valida(funcionario_valido, info_contato_valida, cpf_valido_aleatorio):
    # Testa a criação de um funcionário válido.
    id_esperado = funcionario_valido.id
    assert funcionario_valido.id == id_esperado
    assert funcionario_valido.nome == "Funcionario Teste Completo"
    assert funcionario_valido.nascimento == date(1990, 1, 1)
    assert funcionario_valido.cpf == cpf_valido_aleatorio
    assert funcionario_valido.ctps == "1234567-89"
    assert funcionario_valido.informacao_contato == info_contato_valida
    assert funcionario_valido.salario == 2500.00
    assert funcionario_valido.data_admissao == date(2020, 1, 1)
    assert funcionario_valido.data_demissao is None
    assert funcionario_valido.nis == "12345678901"
    assert funcionario.Funcionario.buscar_funcionario_por_id(id_esperado) == funcionario_valido
    assert funcionario.Funcionario.buscar_funcionario_por_cpf(cpf_valido_aleatorio) == funcionario_valido

def test_funcionario_criacao_id_especifico(info_contato_valida, cpf_valido_aleatorio):
    # Testa a criação de funcionário com ID específico.
    f = funcionario.Funcionario(
        100, "Funcionario ID Especifico", "01/01/1990", cpf_valido_aleatorio, "1111111-11",
        info_contato_valida, 2000.00, "01/01/2021", None, None
    )
    assert f.id == 100
    assert funcionario.Funcionario.buscar_funcionario_por_id(100) == f

def test_funcionario_colisao_cpf(funcionario_valido, info_contato_valida):
    # Testa a colisão de CPF ao criar um novo funcionário.
    with pytest.raises(ValueError, match=f"Funcionário com CPF {funcionario_valido.cpf} já existe."):
        funcionario.Funcionario(
            None, "Nome Duplicado CPF", "01/01/1990", funcionario_valido.cpf, "2222222-22",
            info_contato_valida, 1000.00, "01/01/2022", None, None
        )

def test_funcionario_colisao_id(funcionario_valido, info_contato_valida):
    # Testa a colisão de ID ao criar um novo funcionário.
    with pytest.raises(ValueError, match=f"Já existe funcionário com o ID {funcionario_valido.id}."):
        funcionario.Funcionario(
            funcionario_valido.id, "Duplicado ID", "01/01/1990", pessoa.gerar_cpf_valido(), "3333333-33",
            info_contato_valida, 1000.00, "01/01/2022", None, None
        )

def test_funcionario_id_invalido(info_contato_valida, cpf_valido_aleatorio):
    # Testa a criação de funcionário com ID inválido.
    with pytest.raises(ValueError, match="ID do funcionário deve ser um número inteiro positivo."):
        funcionario.Funcionario(
            0, "Zero ID", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            info_contato_valida, 2500.00, "01/01/2020", None, "12345678901"
        )
    with pytest.raises(ValueError, match="ID do funcionário deve ser um número inteiro positivo."):
        funcionario.Funcionario(
            "abc", "String ID", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            info_contato_valida, 2500.00, "01/01/2020", None, "12345678901"
        )

def test_funcionario_ctps_invalida(info_contato_valida, cpf_valido_aleatorio):
    # Testa a validação de CTPS inválida.
    with pytest.raises(ValueError, match="CTPS não pode ser vazia."):
        funcionario.Funcionario(
            None, "Nome Teste Completo", "01/01/1990", cpf_valido_aleatorio, "",
            info_contato_valida, 2500.00, "01/01/2020", None, None
        )
    f = funcionario.Funcionario(None, "Nome Teste Completo", "01/01/1990", pessoa.gerar_cpf_valido(), "1234567-89", info_contato_valida, 2500.00, "01/01/2020", None, None)
    with pytest.raises(ValueError, match="CTPS não pode ser vazia."):
        f.ctps = " "

def test_funcionario_info_contato_tipo_invalido(cpf_valido_aleatorio):
    # Testa a criação de funcionário com tipo de info_contato inválido.
    with pytest.raises(TypeError, match="Informação de contato deve ser uma instância da classe Informacao."):
        funcionario.Funcionario(
            None, "Nome Teste Completo", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            "nao_info", 2500.00, "01/01/2020", None, None
        )
    f = funcionario.Funcionario(None, "Nome Teste Completo", "01/01/1990", pessoa.gerar_cpf_valido(), "1234567-89", info.Informacao("11987654321", "email@test.com", "Rua A, 1", ""), 2500.00, "01/01/2020", None, None)
    with pytest.raises(TypeError, match="Informação de contato deve ser uma instância da classe Informacao."):
        f.informacao_contato = "string"

def test_funcionario_salario_invalido(info_contato_valida, cpf_valido_aleatorio):
    # Testa a validação de salário inválido.
    with pytest.raises(ValueError, match="Salário deve ser um número não negativo."):
        funcionario.Funcionario(
            None, "Nome Teste Completo", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            info_contato_valida, -100.00, "01/01/2020", None, None
        )
    f = funcionario.Funcionario(None, "Nome Teste Completo", "01/01/1990", pessoa.gerar_cpf_valido(), "1234567-89", info_contato_valida, 2500.00, "01/01/2020", None, None)
    with pytest.raises(ValueError, match="Salário deve ser um número não negativo."):
        f.salario = -50.00
    with pytest.raises(TypeError, match="Salário deve ser um número válido."): # Espera TypeError
        f.salario = "abc"

def test_funcionario_data_admissao_invalida(info_contato_valida, cpf_valido_aleatorio):
    # Testa a validação de data de admissão inválida.
    with pytest.raises(ValueError, match="Data de admissão não pode ser no futuro."):
        funcionario.Funcionario(
            None, "Nome Teste Completo", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            info_contato_valida, 2500.00, (date.today() + timedelta(days=1)).strftime("%d/%m/%Y"), None, None
        )
    f = funcionario.Funcionario(None, "Nome Teste Completo", "01/01/1990", pessoa.gerar_cpf_valido(), "1234567-89", info_contato_valida, 2500.00, "01/01/2020", None, None)
    with pytest.raises(ValueError, match="Data de admissão inválida: Formato de data inválido."):
        f.data_admissao = "data_errada"

def test_funcionario_data_demissao_invalida(info_contato_valida, cpf_valido_aleatorio):
    # Testa a validação de data de demissão inválida.
    with pytest.raises(ValueError, match="Data de demissão não pode ser anterior à data de admissão."):
        funcionario.Funcionario(
            None, "Nome Teste Completo", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            info_contato_valida, 2500.00, "01/01/2020", "01/01/2019", None
        )
    f = funcionario.Funcionario(None, "Nome Teste Completo", "01/01/1990", pessoa.gerar_cpf_valido(), "1234567-89", info_contato_valida, 2500.00, "01/01/2020", None, None)
    with pytest.raises(ValueError, match="Data de demissão inválida: Formato de data inválido."):
        f.data_demissao = "data_errada"

def test_funcionario_nis_invalido(info_contato_valida, cpf_valido_aleatorio):
    # Testa a validação de NIS inválido.
    with pytest.raises(ValueError, match="NIS inválido: Deve conter exatamente 11 dígitos numéricos."):
        funcionario.Funcionario(
            None, "Nome Teste Completo", "01/01/1990", cpf_valido_aleatorio, "1234567-89",
            info_contato_valida, 2500.00, "01/01/2020", None, "123"
        )
    f = funcionario.Funcionario(None, "Nome Teste Completo", "01/01/1990", pessoa.gerar_cpf_valido(), "1234567-89", info_contato_valida, 2500.00, "01/01/2020", None, None)
    with pytest.raises(ValueError, match="NIS inválido: Deve conter exatamente 11 dígitos numéricos."):
        f.nis = "abc"

def test_funcionario_buscar_por_cpf(funcionario_valido):
    # Testa a busca de funcionário por CPF.
    found_f = funcionario.Funcionario.buscar_funcionario_por_cpf(funcionario_valido.cpf)
    assert found_f == funcionario_valido
    assert funcionario.Funcionario.buscar_funcionario_por_cpf("999.999.999-99") is None
    assert funcionario.Funcionario.buscar_funcionario_por_cpf("cpf_invalido_format") is None

def test_funcionario_buscar_por_id(funcionario_valido):
    # Testa a busca de funcionário por ID.
    found_f = funcionario.Funcionario.buscar_funcionario_por_id(funcionario_valido.id)
    assert found_f == funcionario_valido
    assert funcionario.Funcionario.buscar_funcionario_por_id(9999) is None

def test_funcionario_buscar_por_nome_exato(funcionario_valido):
    # Testa a busca de funcionário por nome exato.
    found_f = funcionario.Funcionario.buscar_funcionario_por_nome_exato("Funcionario Teste Completo")
    assert found_f == funcionario_valido
    assert funcionario.Funcionario.buscar_funcionario_por_nome_exato("funcionario teste completo") == funcionario_valido # Case-insensitive
    assert funcionario.Funcionario.buscar_funcionario_por_nome_exato("Nome Inexistente") is None

def test_funcionario_listar_funcionarios(funcionario_valido, info_contato_valida, cpf_valido_aleatorio):
    # Testa a listagem de todos os funcionários.
    f2 = funcionario.Funcionario(
        None, "Outro Funcionario Teste", "01/01/1990", pessoa.gerar_cpf_valido(), "9876543-21",
        info_contato_valida, 2000.00, "01/01/2021", None, None
    )
    all_funcs = funcionario.Funcionario.listar_funcionarios()
    assert len(all_funcs) == 2
    assert funcionario_valido in all_funcs
    assert f2 in all_funcs

def test_funcionario_atualizar_cpf(funcionario_valido):
    # Testa a atualização do CPF do funcionário.
    cpf_antigo = funcionario_valido.cpf # Captura o CPF antigo antes da atualização
    novo_cpf = pessoa.gerar_cpf_valido()
    funcionario.Funcionario.atualizar_cpf(cpf_antigo, novo_cpf) # Passa o CPF antigo
    assert funcionario_valido.cpf == novo_cpf
    assert funcionario.Funcionario.buscar_funcionario_por_cpf(novo_cpf) == funcionario_valido
    assert funcionario.Funcionario.buscar_funcionario_por_cpf(cpf_antigo) is None # Verifica se o CPF antigo não existe mais no sistema

def test_funcionario_atualizar_cpf_nao_encontrado():
    # Testa atualização de CPF de funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com CPF 999.999.999-99 não encontrado para atualização."):
        funcionario.Funcionario.atualizar_cpf("999.999.999-99", pessoa.gerar_cpf_valido())

def test_funcionario_atualizar_cpf_invalido(funcionario_valido):
    # Testa atualização de CPF com formato inválido.
    with pytest.raises(ValueError, match="Novo CPF inválido: Dígitos verificadores não correspondem ou padrão inválido."):
        funcionario.Funcionario.atualizar_cpf(funcionario_valido.cpf, "111.111.111-11")

def test_funcionario_atualizar_cpf_colisao(funcionario_valido, info_contato_valida):
    # Testa atualização de CPF para um já existente.
    f_dup = funcionario.Funcionario(None, "Duplicado CPF", "01/01/1990", pessoa.gerar_cpf_valido(), "4444444-44", info_contato_valida, 1000.00, "01/01/2022", None, None)
    with pytest.raises(ValueError, match=f"Já existe outro funcionário com o CPF {f_dup.cpf}."):
        funcionario.Funcionario.atualizar_cpf(funcionario_valido.cpf, f_dup.cpf)

def test_funcionario_atualizar_nome_por_id(funcionario_valido):
    # Testa a atualização do nome do funcionário por ID.
    funcionario.Funcionario.atualizar_nome_por_id(funcionario_valido.id, "Nome Atualizado")
    assert funcionario_valido.nome == "Nome Atualizado"
    with pytest.raises(ValueError, match="Formato de nome inválido."):
        funcionario.Funcionario.atualizar_nome_por_id(funcionario_valido.id, "Nome")

def test_funcionario_atualizar_nome_por_id_nao_encontrado():
    # Testa atualização de nome para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com ID 999 não encontrado."):
        funcionario.Funcionario.atualizar_nome_por_id(999, "Nome Inexistente")

def test_funcionario_atualizar_data_nascimento_por_id(funcionario_valido):
    # Testa a atualização da data de nascimento do funcionário por ID.
    funcionario.Funcionario.atualizar_data_nascimento_por_id(funcionario_valido.id, "15/07/1985")
    assert funcionario_valido.nascimento == date(1985, 7, 15)
    with pytest.raises(ValueError, match="Data de nascimento não pode ser no futuro."):
        funcionario.Funcionario.atualizar_data_nascimento_por_id(funcionario_valido.id, (date.today() + timedelta(days=1)).strftime("%d/%m/%Y"))

def test_funcionario_atualizar_data_nascimento_por_id_nao_encontrado():
    # Testa atualização de data de nascimento para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com ID 999 não encontrado."):
        funcionario.Funcionario.atualizar_data_nascimento_por_id(999, "01/01/1990")

def test_funcionario_atualizar_ctps_por_id(funcionario_valido):
    # Testa a atualização da CTPS do funcionário por ID.
    funcionario.Funcionario.atualizar_ctps_por_id(funcionario_valido.id, "9988776-65")
    assert funcionario_valido.ctps == "9988776-65"
    with pytest.raises(ValueError, match="CTPS não pode ser vazia."):
        funcionario.Funcionario.atualizar_ctps_por_id(funcionario_valido.id, " ")

def test_funcionario_atualizar_ctps_por_id_nao_encontrado():
    # Testa atualização de CTPS para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com ID 999 não encontrado."):
        funcionario.Funcionario.atualizar_ctps_por_id(999, "1234567-89")

def test_funcionario_atualizar_informacao_contato(funcionario_valido):
    # Testa a atualização das informações de contato do funcionário.
    nova_info = info.Informacao("31912345678", "novo@email.com", "Rua Z, 789, Centro, BH, MG", "")
    funcionario.Funcionario.atualizar_informacao_contato(funcionario_valido.cpf, nova_info)
    assert funcionario_valido.informacao_contato.email == "novo@email.com"
    with pytest.raises(TypeError, match="Informação de contato deve ser uma instância da classe Informacao."):
        funcionario.Funcionario.atualizar_informacao_contato(funcionario_valido.cpf, "string")

def test_funcionario_atualizar_informacao_contato_nao_encontrado():
    # Testa atualização de informações de contato para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com CPF 999.999.999-99 não encontrado."):
        funcionario.Funcionario.atualizar_informacao_contato("999.999.999-99", info.Informacao("11987654321", "email@test.com", "Rua A, 1", ""))

def test_funcionario_atualizar_salario_por_cpf(funcionario_valido):
    # Testa a atualização do salário do funcionário por CPF.
    funcionario.Funcionario.atualizar_salario_por_cpf(funcionario_valido.cpf, 3000.00)
    assert funcionario_valido.salario == 3000.00
    with pytest.raises(ValueError, match="Salário deve ser um número não negativo."):
        funcionario.Funcionario.atualizar_salario_por_cpf(funcionario_valido.cpf, -100.00)

def test_funcionario_atualizar_salario_por_cpf_nao_encontrado():
    # Testa atualização de salário para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com CPF 999.999.999-99 não encontrado."):
        funcionario.Funcionario.atualizar_salario_por_cpf("999.999.999-99", 1000.00)

def test_funcionario_atualizar_data_admissao_por_cpf(funcionario_valido):
    # Testa a atualização da data de admissão do funcionário por CPF.
    funcionario.Funcionario.atualizar_data_admissao_por_cpf(funcionario_valido.cpf, "01/01/2018")
    assert funcionario_valido.data_admissao == date(2018, 1, 1)
    with pytest.raises(ValueError, match="Data de admissão não pode ser no futuro."):
        funcionario.Funcionario.atualizar_data_admissao_por_cpf(funcionario_valido.cpf, (date.today() + timedelta(days=1)).strftime("%d/%m/%Y"))

def test_funcionario_atualizar_data_admissao_por_cpf_nao_encontrado():
    # Testa atualização de data de admissão para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com CPF 999.999.999-99 não encontrado."):
        funcionario.Funcionario.atualizar_data_admissao_por_cpf("999.999.999-99", "01/01/2020")

def test_funcionario_atualizar_data_demissao_por_cpf(funcionario_valido):
    # Testa a atualização da data de demissão do funcionário por CPF.
    funcionario.Funcionario.atualizar_data_demissao_por_cpf(funcionario_valido.cpf, "01/01/2023")
    assert funcionario_valido.data_demissao == date(2023, 1, 1)
    funcionario.Funcionario.atualizar_data_demissao_por_cpf(funcionario_valido.cpf, None)
    assert funcionario_valido.data_demissao is None
    with pytest.raises(ValueError, match="Data de demissão não pode ser anterior à data de admissão."):
        funcionario.Funcionario.atualizar_data_demissao_por_cpf(funcionario_valido.cpf, "01/01/2000") # Antes da admissão

def test_funcionario_atualizar_data_demissao_por_cpf_nao_encontrado():
    # Testa atualização de data de demissão para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com CPF 999.999.999-99 não encontrado."):
        funcionario.Funcionario.atualizar_data_demissao_por_cpf("999.999.999-99", "01/01/2023")

def test_funcionario_atualizar_nis_por_id(funcionario_valido):
    # Testa a atualização do NIS do funcionário por ID.
    funcionario.Funcionario.atualizar_nis_por_id(funcionario_valido.id, "99887766554")
    assert funcionario_valido.nis == "99887766554"
    funcionario.Funcionario.atualizar_nis_por_id(funcionario_valido.id, None)
    assert funcionario_valido.nis is None
    with pytest.raises(ValueError, match="NIS inválido: Deve conter exatamente 11 dígitos numéricos."):
        funcionario.Funcionario.atualizar_nis_por_id(funcionario_valido.id, "123")

def test_funcionario_atualizar_nis_por_id_nao_encontrado():
    # Testa atualização de NIS para funcionário inexistente.
    with pytest.raises(ValueError, match="Funcionário com ID 999 não encontrado."):
        funcionario.Funcionario.atualizar_nis_por_id(999, "12345678901")

def test_funcionario_deletar_funcionario_por_cpf(funcionario_valido):
    # Testa a deleção de funcionário por CPF.
    funcionario.Funcionario.deletar_funcionario_por_cpf(funcionario_valido.cpf)
    assert funcionario.Funcionario.buscar_funcionario_por_cpf(funcionario_valido.cpf) is None
    assert funcionario.Funcionario.buscar_funcionario_por_id(funcionario_valido.id) is None

def test_funcionario_deletar_funcionario_por_cpf_nao_encontrado():
    # Testa a deleção de funcionário inexistente por CPF.
    with pytest.raises(ValueError, match="Funcionário com CPF 999.999.999-99 não encontrado para exclusão."):
        funcionario.Funcionario.deletar_funcionario_por_cpf("999.999.999-99")

def test_funcionario_deletar_funcionario_por_id(info_contato_valida):
    # Testa a deleção de funcionário por ID.
    f_new = funcionario.Funcionario(
        None, "Para Deletar Teste", "01/01/1995", pessoa.gerar_cpf_valido(), "5555555-55",
        info_contato_valida, 1800.00, "01/01/2022", None, None
    )
    funcionario.Funcionario.deletar_funcionario_por_id(f_new.id)
    assert funcionario.Funcionario.buscar_funcionario_por_id(f_new.id) is None
    assert funcionario.Funcionario.buscar_funcionario_por_cpf(f_new.cpf) is None

def test_funcionario_deletar_funcionario_por_id_nao_encontrado():
    # Testa a deleção de funcionário inexistente por ID.
    with pytest.raises(ValueError, match="Funcionário com ID 999 não encontrado para exclusão."):
        funcionario.Funcionario.deletar_funcionario_por_id(999)

def test_funcionario_inicializar_proximo_id_vazio():
    # Testa _inicializar_proximo_id quando a lista está vazia
    funcionario.Funcionario._funcionarios_por_id.clear()
    funcionario.Funcionario._proximo_id_disponivel = 0 # Reset para garantir
    funcionario.Funcionario._inicializar_proximo_id()
    assert funcionario.Funcionario._proximo_id_disponivel == 1

def test_funcionario_inicializar_proximo_id_populado(info_contato_valida):
    # Testa _inicializar_proximo_id quando a lista está populada
    f1 = funcionario.Funcionario(10, "Func A", "01/01/1990", pessoa.gerar_cpf_valido(), "1111111-11", info_contato_valida, 1000.0, "01/01/2020", None, None)
    f2 = funcionario.Funcionario(5, "Func B", "01/01/1990", pessoa.gerar_cpf_valido(), "2222222-22", info_contato_valida, 1000.0, "01/01/2020", None, None)
    funcionario.Funcionario._proximo_id_disponivel = 0 # Reset para garantir
    funcionario.Funcionario._inicializar_proximo_id()
    assert funcionario.Funcionario._proximo_id_disponivel == 11 # Max ID + 1

# --- Testes para a classe Fornecedor (fornecedor.py) ---

def test_fornecedor_criacao_valida(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a criação de um fornecedor válido.
    id_inicial = fornecedor.Fornecedor._proximo_id_disponivel
    f = fornecedor.Fornecedor(None, "Fornecedor Teste Ltda", cnpj_valido_aleatorio, info_contato_valida)
    assert f.id == id_inicial
    assert f.nome == "Fornecedor Teste Ltda"
    assert f.cnpj == cnpj_valido_aleatorio
    assert f.info_contato == info_contato_valida
    assert fornecedor.Fornecedor.buscar_fornecedor_id(f.id) == f
    assert fornecedor.Fornecedor.buscar_fornecedor(f.cnpj) == f

def test_fornecedor_criacao_id_especifico(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a criação de um fornecedor com ID específico.
    f = fornecedor.Fornecedor(100, "Fornecedor ID", cnpj_valido_aleatorio, info_contato_valida)
    assert f.id == 100
    assert fornecedor.Fornecedor.buscar_fornecedor_id(100) == f

def test_fornecedor_colisao_cnpj(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a colisão de CNPJ ao criar um novo fornecedor.
    fornecedor.Fornecedor(None, "Fornecedor Um", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match=f"Fornecedor com CNPJ {cnpj_valido_aleatorio} já existe."):
        fornecedor.Fornecedor(None, "Fornecedor Dois", cnpj_valido_aleatorio, info_contato_valida)

def test_fornecedor_colisao_id(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a colisão de ID ao criar um novo fornecedor.
    fornecedor.Fornecedor(1, "Fornecedor Um", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="Já existe um fornecedor com o ID 1."):
        fornecedor.Fornecedor(1, "Fornecedor Dois", pessoa.gerar_cnpj_valido(), info_contato_valida)

def test_fornecedor_id_invalido(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a criação de fornecedor com ID inválido.
    with pytest.raises(ValueError, match="O ID do fornecedor deve ser um número inteiro positivo."):
        fornecedor.Fornecedor(0, "Fornecedor Zero", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="O ID do fornecedor deve ser um número inteiro positivo."):
        fornecedor.Fornecedor(-5, "Fornecedor Negativo", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="O ID do fornecedor deve ser um número inteiro positivo."):
        fornecedor.Fornecedor("abc", "Fornecedor String", cnpj_valido_aleatorio, info_contato_valida)

def test_fornecedor_nome_vazio(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a validação de nome vazio para fornecedor.
    with pytest.raises(ValueError, match="O nome do fornecedor não pode ser vazio."):
        fornecedor.Fornecedor(None, " ", cnpj_valido_aleatorio, info_contato_valida)
    f = fornecedor.Fornecedor(None, "Nome Teste", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match="O nome do fornecedor não pode ser vazio."):
        f.nome = " "

def test_fornecedor_cnpj_invalido(info_contato_valida):
    # Testa a validação de CNPJ inválido.
    with pytest.raises(ValueError, match="CNPJ inválido: Deve conter exatamente 14 dígitos."):
        fornecedor.Fornecedor(None, "Forn CNPJ Curto", "123", info_contato_valida)
    with pytest.raises(ValueError, match="CNPJ inválido: Dígitos verificadores não correspondem ou padrão inválido."):
        fornecedor.Fornecedor(None, "Forn CNPJ Invalido", "11.111.111/1111-11", info_contato_valida)
    f = fornecedor.Fornecedor(None, "Forn Teste", pessoa.gerar_cnpj_valido(), info_contato_valida)
    with pytest.raises(ValueError, match="CNPJ inválido: Deve conter exatamente 14 dígitos."):
        f.cnpj = "123"

def test_fornecedor_info_contato_tipo_invalido(cnpj_valido_aleatorio):
    # Testa a criação de fornecedor com tipo de info_contato inválido.
    with pytest.raises(TypeError, match="A informação de contato deve ser uma instância da classe Informacao."):
        fornecedor.Fornecedor(None, "Forn Invalido", cnpj_valido_aleatorio, "nao_info")
    f = fornecedor.Fornecedor(None, "Forn Teste", cnpj_valido_aleatorio, info.Informacao("11987654321", "email@test.com", "Rua A, 1", ""))
    with pytest.raises(TypeError, match="A informação de contato deve ser uma instância da classe Informacao."):
        f.info_contato = "string"

def test_fornecedor_eh_cnpj_valido_digitos_validos():
    # Testes para CNPJs válidos
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos("00000000000191") is True # Um CNPJ válido conhecido
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos(pessoa.gerar_cnpj_valido().replace('.', '').replace('/', '').replace('-', '')) is True

def test_fornecedor_eh_cnpj_valido_digitos_invalidos():
    # Testes para CNPJs inválidos
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos("123") is False # Curto
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos("11111111111111") is False # Todos iguais
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos("00000000000000") is False # Todos zeros
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos("12345678901234") is False # Dígitos verificadores incorretos
    assert fornecedor.Fornecedor._eh_cnpj_valido_digitos("abcdefghijklmn") is False # Não dígitos

def test_fornecedor_buscar_fornecedor(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a busca de fornecedor por CNPJ.
    f = fornecedor.Fornecedor(None, "Fornecedor Busca", cnpj_valido_aleatorio, info_contato_valida)
    found_f = fornecedor.Fornecedor.buscar_fornecedor(cnpj_valido_aleatorio)
    assert found_f == f
    assert fornecedor.Fornecedor.buscar_fornecedor("99.999.999/9999-99") is None
    assert fornecedor.Fornecedor.buscar_fornecedor("cnpj_invalido_format") is None

def test_fornecedor_buscar_fornecedor_id(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a busca de fornecedor por ID.
    f = fornecedor.Fornecedor(None, "Fornecedor Busca ID", cnpj_valido_aleatorio, info_contato_valida)
    found_f = fornecedor.Fornecedor.buscar_fornecedor_id(f.id)
    assert found_f == f
    assert fornecedor.Fornecedor.buscar_fornecedor_id(9999) is None

def test_fornecedor_buscar_fornecedor_por_nome_exato(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a busca de fornecedor por nome exato.
    f = fornecedor.Fornecedor(None, "Fornecedor Exato", cnpj_valido_aleatorio, info_contato_valida)
    found_f = fornecedor.Fornecedor.buscar_fornecedor_por_nome_exato("Fornecedor Exato")
    assert found_f == f
    assert fornecedor.Fornecedor.buscar_fornecedor_por_nome_exato("fornecedor exato") == f # Case-insensitive
    assert fornecedor.Fornecedor.buscar_fornecedor_por_nome_exato("Fornecedor Inexistente") is None

def test_fornecedor_buscar_fornecedores_por_nome_parcial(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a busca de fornecedores por nome parcial.
    f1 = fornecedor.Fornecedor(None, "ABC Materiais", cnpj_valido_aleatorio, info_contato_valida)
    f2 = fornecedor.Fornecedor(None, "DEF Comércio ABC", pessoa.gerar_cnpj_valido(), info_contato_valida)
    f3 = fornecedor.Fornecedor(None, "GHI Serviços", pessoa.gerar_cnpj_valido(), info_contato_valida)

    results = fornecedor.Fornecedor.buscar_fornecedores_por_nome_parcial("ABC")
    assert len(results) == 2
    assert f1 in results
    assert f2 in results

    results_lower = fornecedor.Fornecedor.buscar_fornecedores_por_nome_parcial("abc")
    assert len(results_lower) == 2
    assert f1 in results_lower
    assert f2 in results_lower

    assert not fornecedor.Fornecedor.buscar_fornecedores_por_nome_parcial("Inexistente")

def test_fornecedor_listar_fornecedores(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a listagem de todos os fornecedores.
    f1 = fornecedor.Fornecedor(None, "Listar Um", cnpj_valido_aleatorio, info_contato_valida)
    f2 = fornecedor.Fornecedor(None, "Listar Dois", pessoa.gerar_cnpj_valido(), info_contato_valida)
    all_forns = fornecedor.Fornecedor.listar_fornecedores()
    assert len(all_forns) == 2
    assert f1 in all_forns
    assert f2 in all_forns

def test_fornecedor_atualizar_dados_fornecedor(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a atualização de dados de um fornecedor.
    f = fornecedor.Fornecedor(None, "Forn Antigo", cnpj_valido_aleatorio, info_contato_valida)

    novo_info_contato = info.Informacao(
        telefone="11999998888", # Número de telefone válido, será formatado para "11 99999 8888"
        email="novo.email@forn.com",
        endereco="Rua Nova do Fornecedor, 789, Outro Bairro, Outra Cidade, SC",
        redes_sociais=""
    )

    fornecedor.Fornecedor.atualizar_dados_fornecedor(f.id, nome="Fornecedor Novo", info_contato=novo_info_contato)
    
    assert f.nome == "Fornecedor Novo"
    assert f.info_contato.telefone == "11999998888"
    assert f.info_contato.email == "novo.email@forn.com"
    assert f.info_contato.endereco["nome_rua"] == "Rua Nova do Fornecedor"

def test_fornecedor_atualizar_dados_fornecedor_nao_encontrado():
    # Testa a atualização de dados de um fornecedor inexistente.
    with pytest.raises(ValueError, match="Fornecedor com ID 999 não encontrado para atualização."):
        fornecedor.Fornecedor.atualizar_dados_fornecedor(999, nome="Inexistente")

def test_fornecedor_atualizar_dados_fornecedor_id_e_cnpj_nao_alteraveis(info_contato_valida, cnpj_valido_aleatorio):
    # Testa que ID e CNPJ não podem ser alterados via atualizar_dados_fornecedor.
    f = fornecedor.Fornecedor(None, "Forn Teste", cnpj_valido_aleatorio, info_contato_valida)
    
    # O método não deve levantar erro, mas imprimir aviso e não alterar
    fornecedor.Fornecedor.atualizar_dados_fornecedor(f.id, id=999, cnpj=pessoa.gerar_cnpj_valido())
    assert f.id != 999
    assert f.cnpj == cnpj_valido_aleatorio

def test_fornecedor_atualizar_dados_fornecedor_info_contato_tipo_invalido(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a atualização de info_contato com tipo inválido.
    f = fornecedor.Fornecedor(None, "Forn Teste", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(TypeError, match="A informação de contato deve ser uma instância da classe Informacao."):
        fornecedor.Fornecedor.atualizar_dados_fornecedor(f.id, info_contato="string")

def test_fornecedor_atualizar_cnpj_fornecedor_valido(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a atualização do CNPJ de um fornecedor.
    f = fornecedor.Fornecedor(None, "Forn CNPJ", cnpj_valido_aleatorio, info_contato_valida)
    novo_cnpj = pessoa.gerar_cnpj_valido()
    fornecedor.Fornecedor.atualizar_cnpj_fornecedor(f.id, novo_cnpj)
    assert f.cnpj == novo_cnpj
    assert fornecedor.Fornecedor.buscar_fornecedor(novo_cnpj) == f
    assert fornecedor.Fornecedor.buscar_fornecedor(cnpj_valido_aleatorio) is None # CNPJ antigo deve ter sido removido

def test_fornecedor_atualizar_cnpj_fornecedor_invalido(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a atualização do CNPJ de um fornecedor com CNPJ inválido.
    f = fornecedor.Fornecedor(None, "Forn CNPJ Inv", cnpj_valido_aleatorio, info_contato_valida)
    with pytest.raises(ValueError, match=r"Formato de CNPJ inválido ou CNPJ inválido: CNPJ inválido: Deve conter exatamente 14 dígitos\."):
        fornecedor.Fornecedor.atualizar_cnpj_fornecedor(f.id, "123")

def test_fornecedor_atualizar_cnpj_fornecedor_colisao(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a atualização do CNPJ de um fornecedor com CNPJ já existente em outro fornecedor.
    f1 = fornecedor.Fornecedor(None, "Forn Um", cnpj_valido_aleatorio, info_contato_valida)
    cnpj_duplicado = pessoa.gerar_cnpj_valido()
    f2 = fornecedor.Fornecedor(None, "Forn Dois", cnpj_duplicado, info_contato_valida)

    with pytest.raises(ValueError, match=f"Já existe outro fornecedor com o CNPJ {cnpj_duplicado}."):
        fornecedor.Fornecedor.atualizar_cnpj_fornecedor(f1.id, cnpj_duplicado)

def test_fornecedor_atualizar_cnpj_fornecedor_nao_encontrado():
    # Testa a atualização de CNPJ para um fornecedor inexistente.
    with pytest.raises(ValueError, match="Fornecedor com ID 999 não encontrado para atualização de CNPJ."):
        fornecedor.Fornecedor.atualizar_cnpj_fornecedor(999, pessoa.gerar_cnpj_valido())

def test_fornecedor_deletar_fornecedor(info_contato_valida, cnpj_valido_aleatorio):
    # Testa a deleção de um fornecedor.
    f = fornecedor.Fornecedor(None, "Forn Deletar", cnpj_valido_aleatorio, info_contato_valida)
    fornecedor.Fornecedor.deletar_fornecedor(f.id)
    assert fornecedor.Fornecedor.buscar_fornecedor_id(f.id) is None
    assert fornecedor.Fornecedor.buscar_fornecedor(f.cnpj) is None
    assert f not in fornecedor.Fornecedor.listar_fornecedores()

def test_fornecedor_deletar_fornecedor_nao_encontrado():
    # Testa a deleção de um fornecedor inexistente.
    with pytest.raises(ValueError, match="Fornecedor com ID 999 não encontrado para exclusão."):
        fornecedor.Fornecedor.deletar_fornecedor(999)

def test_fornecedor_inicializar_proximo_id_vazio():
    # Testa _inicializar_proximo_id quando a lista está vazia
    fornecedor.Fornecedor._fornecedores_por_id.clear()
    fornecedor.Fornecedor._proximo_id_disponivel = 0 # Reset para garantir
    fornecedor.Fornecedor._inicializar_proximo_id()
    assert fornecedor.Fornecedor._proximo_id_disponivel == 1

def test_fornecedor_inicializar_proximo_id_populado(info_contato_valida):
    # Testa _inicializar_proximo_id quando a lista está populada
    f1 = fornecedor.Fornecedor(10, "Forn A", pessoa.gerar_cnpj_valido(), info_contato_valida)
    f2 = fornecedor.Fornecedor(5, "Forn B", pessoa.gerar_cnpj_valido(), info_contato_valida)
    fornecedor.Fornecedor._proximo_id_disponivel = 0 # Reset para garantir
    fornecedor.Fornecedor._inicializar_proximo_id()
    assert fornecedor.Fornecedor._proximo_id_disponivel == 11 # Max ID + 1
    