from typing import Optional, Any
from datetime import date
import re
from entidades import pessoa
from entidades import info as mod_info
from tabulate import tabulate
from db_connection import DBConnection

class Funcionario(pessoa.Pessoa):
    # Representa um funcionário da empresa.
    db_conn = DBConnection(host="localhost", database="pi", user="root", password="root")

    def __init__(self, id_funcionario: Optional[int], nome: str, nascimento: str, cpf: str, ctps: str,
                 informacao_contato: mod_info.Informacao, salario: float, data_admissao: str,
                 data_demissao: Optional[str] = None, nis: Optional[str] = None) -> None:
        super().__init__(nome, nascimento, cpf)
        self.ctps = ctps
        self.informacao_contato = informacao_contato
        self.salario = salario
        self.data_admissao = data_admissao
        self.data_demissao = data_demissao
        self.nis = nis

        if id_funcionario is None:
            # Tenta inserir um novo funcionário no banco de dados
            query = "INSERT INTO funcionarios (nome, nascimento, cpf, ctps, telefone, email, endereco, redes, salario, data_admissao, data_demissao, nis) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = (
                self.nome,
                self.nascimento.strftime("%Y-%m-%d"),
                self.cpf,
                self.ctps,
                self.informacao_contato.telefone,
                self.informacao_contato.email,
                str(self.informacao_contato.endereco),
                self.informacao_contato.redes_sociais,
                self.salario,
                self.data_admissao.strftime("%Y-%m-%d"),
                self.data_demissao.strftime("%Y-%m-%d") if self.data_demissao else None,
                self.nis
            )
            self.db_conn.connect()
            result = self.db_conn.execute_query(query, params)
            if result:
                # Se a inserção for bem-sucedida, recupera o ID gerado
                query_id = "SELECT LAST_INSERT_ID() as id"
                new_id = self.db_conn.execute_query(query_id, fetch_one=True)
                self._id = new_id["id"]
            else:
                raise ValueError("Erro ao criar funcionário no banco de dados.")
            self.db_conn.disconnect()
        else:
            # Se um ID for fornecido, tenta carregar o funcionário do banco de dados
            query = "SELECT * FROM funcionarios WHERE id = %s"
            params = (id_funcionario,)
            self.db_conn.connect()
            funcionario_data = self.db_conn.execute_query(query, params, fetch_one=True)
            self.db_conn.disconnect()

            if funcionario_data:
                self._id = funcionario_data["id"]
                self.nome = funcionario_data["nome"]
                self.nascimento = pessoa.Pessoa._parse_data(funcionario_data["nascimento"].strftime("%Y-%m-%d"), is_datetime=False)
                self.cpf = funcionario_data["cpf"]
                self.ctps = funcionario_data["ctps"]
                self.informacao_contato = mod_info.Informacao(
                    funcionario_data["telefone"],
                    funcionario_data["email"],
                    funcionario_data["endereco"],
                    funcionario_data["redes"]
                )
                self.salario = funcionario_data["salario"]
                self.data_admissao = pessoa.Pessoa._parse_data(funcionario_data["data_admissao"].strftime("%Y-%m-%d"), is_datetime=False)
                self.data_demissao = pessoa.Pessoa._parse_data(funcionario_data["data_demissao"].strftime("%Y-%m-%d"), is_datetime=False) if funcionario_data["data_demissao"] else None
                self.nis = funcionario_data["nis"]
            else:
                raise ValueError(f"Funcionário com ID {id_funcionario} não encontrado.")

    def __str__(self) -> str:
        base_str = super().__str__()
        demissao_str = f", Demissão: {self._data_demissao.strftime('%d/%m/%Y')}" if self._data_demissao else ""
        nis_str = f", NIS: {self._nis}" if self._nis else ""
        return (f"ID: {self._id}, {base_str}\n"
                f"  CTPS: {self._ctps}, Salário: R${self._salario:.2f}, "
                f"Admissão: {self._data_admissao.strftime('%d/%m/%Y')}{demissao_str}{nis_str}\n"
                f"  Informações de Contato: {self.informacao_contato}")

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        base_repr_conteudo = base_repr[len("Pessoa("):-1]

        data_demissao_repr = repr(self._data_demissao) if self._data_demissao is not None else "None"
        nis_repr = repr(self._nis) if self._nis is not None else "None"

        return (f"Funcionario(id_funcionario={self._id!r}, {base_repr_conteudo}, "
                f"ctps={self._ctps!r}, informacao_contato={self._informacao_contato!r}, salario={self._salario!r}, "
                f"data_admissao={self._data_admissao!r}, data_demissao={data_demissao_repr}, "
                f"nis={nis_repr})")

    @property
    def id(self) -> int:
        return self._id

    @property
    def ctps(self) -> str:
        return self._ctps

    @ctps.setter
    def ctps(self, ctps_str: str) -> None:
        ctps_limpa = ctps_str.strip()
        if not ctps_limpa:
            raise ValueError("CTPS não pode ser vazia.")
        self._ctps = ctps_limpa

    @property
    def informacao_contato(self) -> mod_info.Informacao:
        return self._informacao_contato

    @informacao_contato.setter
    def informacao_contato(self, nova_informacao: mod_info.Informacao) -> None:
        if not isinstance(nova_informacao, mod_info.Informacao):
            raise TypeError("Informação de contato deve ser uma instância da classe Informacao.")
        self._informacao_contato = nova_informacao

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, valor: float) -> None:
        if not isinstance(valor, (int, float)):
            raise TypeError("Salário deve ser um número válido.")
        if valor < 0:
            raise ValueError("Salário deve ser um número não negativo.")
        self._salario = float(valor)

    @property
    def data_admissao(self) -> date:
        return self._data_admissao

    @data_admissao.setter
    def data_admissao(self, data_str: str) -> None:
        try:
            data_parseada = pessoa.Pessoa._parse_data(data_str, is_datetime=False)
        except ValueError as e:
            raise ValueError(f"Data de admissão inválida: {e}")
        if data_parseada > date.today():
            raise ValueError("Data de admissão não pode ser no futuro.")
        self._data_admissao = data_parseada

    @property
    def data_demissao(self) -> Optional[date]:
        return self._data_demissao

    @data_demissao.setter
    def data_demissao(self, data_str: Optional[str]) -> None:
        if data_str is None:
            self._data_demissao = None
            return
        try:
            data_parseada = pessoa.Pessoa._parse_data(data_str, is_datetime=False)
        except ValueError as e:
            raise ValueError(f"Data de demissão inválida: {e}")

        if data_parseada < self.data_admissao:
            raise ValueError("Data de demissão não pode ser anterior à data de admissão.")
        self._data_demissao = data_parseada

    @property
    def nis(self) -> Optional[str]:
        return self._nis

    @nis.setter
    def nis(self, nis_str: Optional[str]) -> None:
        if nis_str is None or not nis_str.strip():
            self._nis = None
            return

        nis_limpo = re.sub(r'\\D', '', nis_str)
        if not nis_limpo.isdigit() or len(nis_limpo) != 11:
            raise ValueError("NIS inválido: Deve conter exatamente 11 dígitos numéricos.")

        self._nis = nis_limpo

    @staticmethod
    def buscar_funcionario_por_cpf(cpf: str) -> Optional["Funcionario"]:
        query = "SELECT * FROM funcionarios WHERE cpf = %s"
        params = (cpf,)
        Funcionario.db_conn.connect()
        funcionario_data = Funcionario.db_conn.execute_query(query, params, fetch_one=True)
        Funcionario.db_conn.disconnect()
        if funcionario_data:
            return Funcionario(
                funcionario_data["id"],
                funcionario_data["nome"],
                funcionario_data["nascimento"].strftime("%Y-%m-%d"),
                funcionario_data["cpf"],
                funcionario_data["ctps"],
                mod_info.Informacao(
                    funcionario_data["telefone"],
                    funcionario_data["email"],
                    funcionario_data["endereco"],
                    funcionario_data["redes"]
                ),
                funcionario_data["salario"],
                funcionario_data["data_admissao"].strftime("%Y-%m-%d"),
                funcionario_data["data_demissao"].strftime("%Y-%m-%d") if funcionario_data["data_demissao"] else None,
                funcionario_data["nis"]
            )
        return None

    @staticmethod
    def buscar_funcionario_por_id(id_func: int) -> Optional["Funcionario"]:
        query = "SELECT * FROM funcionarios WHERE id = %s"
        params = (id_func,)
        Funcionario.db_conn.connect()
        funcionario_data = Funcionario.db_conn.execute_query(query, params, fetch_one=True)
        Funcionario.db_conn.disconnect()
        if funcionario_data:
            return Funcionario(
                funcionario_data["id"],
                funcionario_data["nome"],
                funcionario_data["nascimento"].strftime("%Y-%m-%d"),
                funcionario_data["cpf"],
                funcionario_data["ctps"],
                mod_info.Informacao(
                    funcionario_data["telefone"],
                    funcionario_data["email"],
                    funcionario_data["endereco"],
                    funcionario_data["redes"]
                ),
                funcionario_data["salario"],
                funcionario_data["data_admissao"].strftime("%Y-%m-%d"),
                funcionario_data["data_demissao"].strftime("%Y-%m-%d") if funcionario_data["data_demissao"] else None,
                funcionario_data["nis"]
            )
        return None

    @staticmethod
    def buscar_funcionario_por_nome_exato(nome: str) -> Optional["Funcionario"]:
        query = "SELECT * FROM funcionarios WHERE LOWER(nome) = LOWER(%s)"
        params = (nome,)
        Funcionario.db_conn.connect()
        funcionario_data = Funcionario.db_conn.execute_query(query, params, fetch_one=True)
        Funcionario.db_conn.disconnect()
        if funcionario_data:
            return Funcionario(
                funcionario_data["id"],
                funcionario_data["nome"],
                funcionario_data["nascimento"].strftime("%Y-%m-%d"),
                funcionario_data["cpf"],
                funcionario_data["ctps"],
                mod_info.Informacao(
                    funcionario_data["telefone"],
                    funcionario_data["email"],
                    funcionario_data["endereco"],
                    funcionario_data["redes"]
                ),
                funcionario_data["salario"],
                funcionario_data["data_admissao"].strftime("%Y-%m-%d"),
                funcionario_data["data_demissao"].strftime("%Y-%m-%d") if funcionario_data["data_demissao"] else None,
                funcionario_data["nis"]
            )
        return None

    @staticmethod
    def listar_funcionarios() -> list["Funcionario"]:
        query = "SELECT * FROM funcionarios"
        Funcionario.db_conn.connect()
        funcionarios_data = Funcionario.db_conn.execute_query(query, fetch_all=True)
        Funcionario.db_conn.disconnect()
        resultados = []
        if funcionarios_data:
            for funcionario_data in funcionarios_data:
                resultados.append(Funcionario(
                    funcionario_data["id"],
                    funcionario_data["nome"],
                    funcionario_data["nascimento"].strftime("%Y-%m-%d"),
                    funcionario_data["cpf"],
                    funcionario_data["ctps"],
                    mod_info.Informacao(
                        funcionario_data["telefone"],
                        funcionario_data["email"],
                        funcionario_data["endereco"],
                        funcionario_data["redes"]
                    ),
                    funcionario_data["salario"],
                    funcionario_data["data_admissao"].strftime("%Y-%m-%d"),
                    funcionario_data["data_demissao"].strftime("%Y-%m-%d") if funcionario_data["data_demissao"] else None,
                    funcionario_data["nis"]
                ))
        return resultados

    @staticmethod
    def atualizar_cpf(id_func: int, novo_cpf: str) -> None:
        func = Funcionario.buscar_funcionario_por_id(id_func)
        if not func:
            raise ValueError(f"Funcionário com ID {id_func} não encontrado para atualização.")

        func.cpf = novo_cpf # Validação do CPF ocorre no setter da classe Pessoa

        query = "UPDATE funcionarios SET cpf = %s WHERE id = %s"
        params = (func.cpf, id_func)
        Funcionario.db_conn.connect()
        Funcionario.db_conn.execute_query(query, params)
        Funcionario.db_conn.disconnect()

    @staticmethod
    def atualizar_nome_por_id(id_func: int, novo_nome: str) -> None:
        func = Funcionario.buscar_funcionario_por_id(id_func)
        if not func:
            raise ValueError(f"Funcionário com ID {id_func} não encontrado.")
        func.nome = novo_nome
        query = "UPDATE funcionarios SET nome = %s WHERE id = %s"
        params = (func.nome, id_func)
        Funcionario.db_conn.connect()
        Funcionario.db_conn.execute_query(query, params)
        Funcionario.db_conn.disconnect()

    @staticmethod
    def atualizar_data_nascimento_por_id(id_func: int, nova_data_nascimento: str) -> None:
        func = Funcionario.buscar_funcionario_por_id(id_func)
        if not func:
            raise ValueError(f"Funcionário com ID {id_func} não encontrado.")
        func.nascimento = nova_data_nascimento
        query = "UPDATE funcionarios SET nascimento = %s WHERE id = %s"
        params = (func.nascimento.strftime("%Y-%m-%d"), id_func)
        Funcionario.db_conn.connect()
        Funcionario.db_conn.execute_query(query, params)
        Funcionario.db_conn.disconnect()

    @staticmethod
    def atualizar_ctps_por_id(id_func: int, nova_ctps: str) -> None:
        func = Funcionario.buscar_funcionario_por_id(id_func)
        if not func:
            raise ValueError(f"Funcionário com ID {id_func} não encontrado.")
        func.ctps = nova_ctps
        query = "UPDATE funcionarios SET ctps = %s WHERE id = %s"
        params = (func.ctps, id_func)
        Funcionario.db_conn.connect()
        Funcionario.db_conn.execute_query(query, params)
        Funcionario.db_conn.disconnect()

    @staticmethod
    def atualizar_informacao_contato(id_func: int, nova_informacao: mod_info.Informacao) -> None:
        func = Funcionario.buscar_funcionario_por_id(id_func)
        if not func:
            raise ValueError(f"Funcionário com ID {id_func} não encontrado.")
        func.informacao_contato = nova_informacao
        query = "UPDATE funcionarios SET telefone = %s, email = %s, endereco = %s, redes_sociais = %s WHERE id = %s"
        params = (
            func.informacao_contato.telefone,
            func.informacao_contato.email,
            str(func.informacao_contato.endereco),
            func.informacao_contato.redes_sociais,
            id_func
        )
        Funcionario.db_conn.connect()
        Funcionario.db_conn.execute_query(query, params)
        Funcionario.db_conn.disconnect()

    @staticmethod
    def atualizar_salario_por_id(id_func: int, novo_salario: float) -> None:
        func = Funcionario.buscar_funciona
