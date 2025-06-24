from typing import Optional, Any
import re
from entidades import pessoa
from entidades import info as mod_info
from tabulate import tabulate
from db_connection import DBConnection

class Cliente(pessoa.Pessoa):
    # Representa um cliente da empresa.
    db_conn = DBConnection(host="localhost", database="pi", user="root", password="root")
    
    def __init__(self, id_cliente: Optional[int], nome: str, nascimento: str, cpf: str, info_contato: mod_info.Informacao) -> None:
        super().__init__(nome, nascimento, cpf)
        self.info_contato = info_contato

        if id_cliente is None:
            # Tenta inserir um novo cliente no banco de dados
            query = "INSERT INTO clientes (nome, nascimento, cpf, telefone, email, endereco, redes_sociais) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            params = (
                self.nome,
                self.nascimento.strftime('%Y-%m-%d'),
                self.cpf,
                self.info_contato.telefone,
                self.info_contato.email,
                str(self.info_contato.endereco),
                self.info_contato.redes_sociais
            )
            self.db_conn.connect()
            result = self.db_conn.execute_query(query, params)
            if result:
                # Se a inserção for bem-sucedida, recupera o ID gerado
                query_id = "SELECT LAST_INSERT_ID() as id"
                new_id = self.db_conn.execute_query(query_id, fetch_one=True)
                self._id = new_id['id']
            else:
                raise ValueError("Erro ao criar cliente no banco de dados.")
            self.db_conn.disconnect()
        else:
            # Se um ID for fornecido, tenta carregar o cliente do banco de dados
            query = "SELECT * FROM clientes WHERE id = %s"
            params = (id_cliente,)
            self.db_conn.connect()
            cliente_data = self.db_conn.execute_query(query, params, fetch_one=True)
            self.db_conn.disconnect()

            if cliente_data:
                self._id = cliente_data['id']
                self.nome = cliente_data['nome']
                self.nascimento = pessoa.Pessoa._parse_data(cliente_data['nascimento'].strftime('%Y-%m-%d'), is_datetime=False)
                self.cpf = cliente_data['cpf']
                self.info_contato = mod_info.Informacao(
                    cliente_data['telefone'],
                    cliente_data['email'],
                    cliente_data['endereco'],
                    cliente_data['redes_sociais']
                )
            else:
                raise ValueError(f"Cliente com ID {id_cliente} não encontrado.")

    def __str__(self) -> str:
        base_str: str = super().__str__()
        return (f"ID: {self._id}, {base_str}\n"
                f"  Informações de Contato: {self.info_contato}")

    def __repr__(self) -> str:
        base_repr: str = super().__repr__()
        base_repr_conteudo: str = base_repr[len('Pessoa('):-1]
        return (f"Cliente(id_cliente={self._id!r}, {base_repr_conteudo}, "
                f"info_contato={self.info_contato!r})")

    @property
    def id(self) -> int:
        return self._id

    @property
    def info_contato(self) -> mod_info.Informacao:
        return self._info_contato

    @info_contato.setter
    def info_contato(self, nova_info: mod_info.Informacao) -> None:
        if not isinstance(nova_info, mod_info.Informacao):
            raise TypeError("A informação de contato deve ser uma instância da classe Informacao.")
        self._info_contato = nova_info

    @staticmethod
    def buscar_cliente(cpf: str) -> Optional['Cliente']:
        query = "SELECT * FROM clientes WHERE cpf = %s"
        params = (cpf,)
        Cliente.db_conn.connect()
        cliente_data = Cliente.db_conn.execute_query(query, params, fetch_one=True)
        Cliente.db_conn.disconnect()
        if cliente_data:
            return Cliente(
                cliente_data['id'],
                cliente_data['nome'],
                cliente_data['nascimento'].strftime('%Y-%m-%d'),
                cliente_data['cpf'],
                mod_info.Informacao(
                    cliente_data['telefone'],
                    cliente_data['email'],
                    cliente_data['endereco'],
                    cliente_data['redes_sociais']
                )
            )
        return None

    @staticmethod
    def buscar_cliente_id(id_cliente: int) -> Optional['Cliente']:
        query = "SELECT * FROM clientes WHERE id = %s"
        params = (id_cliente,)
        Cliente.db_conn.connect()
        cliente_data = Cliente.db_conn.execute_query(query, params, fetch_one=True)
        Cliente.db_conn.disconnect()
        if cliente_data:
            return Cliente(
                cliente_data['id'],
                cliente_data['nome'],
                cliente_data['nascimento'].strftime('%Y-%m-%d'),
                cliente_data['cpf'],
                mod_info.Informacao(
                    cliente_data['telefone'],
                    cliente_data['email'],
                    cliente_data['endereco'],
                    cliente_data['redes_sociais']
                )
            )
        return None

    @staticmethod
    def buscar_cliente_por_nome_exato(nome: str) -> Optional['Cliente']:
        query = "SELECT * FROM clientes WHERE LOWER(nome) = LOWER(%s)"
        params = (nome,)
        Cliente.db_conn.connect()
        cliente_data = Cliente.db_conn.execute_query(query, params, fetch_one=True)
        Cliente.db_conn.disconnect()
        if cliente_data:
            return Cliente(
                cliente_data['id'],
                cliente_data['nome'],
                cliente_data['nascimento'].strftime('%Y-%m-%d'),
                cliente_data['cpf'],
                mod_info.Informacao(
                    cliente_data['telefone'],
                    cliente_data['email'],
                    cliente_data['endereco'],
                    cliente_data['redes_sociais']
                )
            )
        return None

    @staticmethod
    def buscar_clientes_por_nome_parcial(nome_parcial: str) -> list['Cliente']:
        query = "SELECT * FROM clientes WHERE LOWER(nome) LIKE %s"
        params = (f"%{nome_parcial.lower()}%",)
        Cliente.db_conn.connect()
        clientes_data = Cliente.db_conn.execute_query(query, params, fetch_all=True)
        Cliente.db_conn.disconnect()
        resultados = []
        if clientes_data:
            for cliente_data in clientes_data:
                resultados.append(Cliente(
                    cliente_data['id'],
                    cliente_data['nome'],
                    cliente_data['nascimento'].strftime('%Y-%m-%d'),
                    cliente_data['cpf'],
                    mod_info.Informacao(
                        cliente_data['telefone'],
                        cliente_data['email'],
                        cliente_data['endereco'],
                        cliente_data['redes_sociais']
                    )
                ))
        return resultados

    @staticmethod
    def listar_clientes() -> list['Cliente']:
        query = "SELECT * FROM clientes"
        Cliente.db_conn.connect()
        clientes_data = Cliente.db_conn.execute_query(query, fetch_all=True)
        Cliente.db_conn.disconnect()
        resultados = []
        if clientes_data:
            for cliente_data in clientes_data:
                resultados.append(Cliente(
                    cliente_data['id'],
                    cliente_data['nome'],
                    cliente_data['nascimento'].strftime('%Y-%m-%d'),
                    cliente_data['cpf'],
                    mod_info.Informacao(
                        cliente_data['telefone'],
                        cliente_data['email'],
                        cliente_data['endereco'],
                        cliente_data['redes_sociais']
                    )
                ))
        return resultados

    @staticmethod
    def atualizar_dados_cliente(id_cliente: int, **kwargs: Any) -> None:
        cliente_existente: Optional['Cliente'] = Cliente.buscar_cliente_id(id_cliente)
        if not cliente_existente:
            raise ValueError(f"Cliente com ID {id_cliente} não encontrado para atualização.")

        updates = []
        params = []

        for chave, valor in kwargs.items():
            if chave == 'id':
                continue
            if chave == 'info_contato':
                if not isinstance(valor, mod_info.Informacao):
                    raise TypeError("A informação de contato deve ser uma instância da classe Informacao.")
                updates.append("telefone = %s")
                params.append(valor.telefone)
                updates.append("email = %s")
                params.append(valor.email)
                updates.append("endereco = %s")
                params.append(str(valor.endereco))
                updates.append("redes_sociais = %s")
                params.append(valor.redes_sociais)
            elif chave == 'nascimento':
                updates.append(f"{chave} = %s")
                params.append(pessoa.Pessoa._parse_data(valor, is_datetime=False).strftime('%Y-%m-%d'))
            elif chave == 'cpf':
                # Validação de CPF já ocorre no setter da classe Pessoa
                updates.append(f"{chave} = %s")
                params.append(cliente_existente._formatar_cpf_para_busca(valor))
            elif hasattr(cliente_existente, chave):
                updates.append(f"{chave} = %s")
                setattr(cliente_existente, chave, valor) # Valida o valor antes de adicionar aos params
                params.append(getattr(cliente_existente, chave))

        if updates:
            query = f"UPDATE clientes SET {', '.join(updates)} WHERE id = %s"
            params.append(id_cliente)
            Cliente.db_conn.connect()
            Cliente.db_conn.execute_query(query, params)
            Cliente.db_conn.disconnect()

    @staticmethod
    def atualizar_cpf_cliente(id_cliente: int, novo_cpf: str) -> None:
        cliente: Optional['Cliente'] = Cliente.buscar_cliente_id(id_cliente)
        if not cliente:
            raise ValueError(f"Cliente com ID {id_cliente} não encontrado para atualização de CPF.")

        # A validação do CPF ocorre no setter da classe Pessoa
        cliente.cpf = novo_cpf

        query = "UPDATE clientes SET cpf = %s WHERE id = %s"
        params = (cliente.cpf, id_cliente)
        Cliente.db_conn.connect()
        Cliente.db_conn.execute_query(query, params)
        Cliente.db_conn.disconnect()

    @staticmethod
    def deletar_cliente(id_cliente: int) -> None:
        query = "DELETE FROM clientes WHERE id = %s"
        params = (id_cliente,)
        Cliente.db_conn.connect()
        result = Cliente.db_conn.execute_query(query, params)
        Cliente.db_conn.disconnect()
        if not result:
            raise ValueError(f"Cliente com ID {id_cliente} não encontrado para exclusão.")

    @staticmethod
    def criar_cliente(nome: str, nascimento: str, cpf: str, info_contato: mod_info.Informacao) -> 'Cliente':
        novo_cliente = Cliente(None, nome, nascimento, cpf, info_contato)
        return novo_cliente

    @staticmethod
    def _formatar_clientes_para_tabela(clientes: list['Cliente']) -> str:
        if not clientes:
            return "Nenhum cliente para exibir."

        cabecalhos = ["ID", "Nome", "CPF", "Nascimento", "Idade", "Telefone", "Email"]
        dados_tabela = []

        for cliente in clientes:
            nascimento_str = cliente.nascimento.strftime('%d/%m/%Y')
            telefone_str = cliente.info_contato.telefone
            email_str = cliente.info_contato.email
            
            dados_tabela.append([
                cliente.id,
                cliente.nome,
                cliente.cpf,
                nascimento_str,
                cliente.idade,
                telefone_str,
                email_str
            ])
        
        return tabulate(dados_tabela, headers=cabecalhos, tablefmt="grid")


