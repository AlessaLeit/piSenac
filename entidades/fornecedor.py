import re
from typing import Optional, Any
from entidades import info as mod_info
from tabulate import tabulate
from db_connection import DBConnection

class Fornecedor:
    # Representa um fornecedor de produtos ou serviços.
    _fornecedores_por_cnpj: dict[str, 'Fornecedor'] = {}
    _fornecedores_por_id: dict[int, 'Fornecedor'] = {}
    _proximo_id_disponivel: int = 1
    db_conn = DBConnection(host="localhost", database="pi", user="root", password="root")

    def __init__(self, id_fornecedor: Optional[int], nome: str, cnpj: str, info_contato: mod_info.Informacao) -> None:
        self.nome = nome
        self.cnpj = cnpj
        self.info_contato = info_contato

        if id_fornecedor is None:
            # Tenta inserir um novo fornecedor no banco de dados
            query = "INSERT INTO fornecedor (nome, cnpj, telefone, endereco, redes) VALUES (%s, %s, %s, %s, %s)"
            params = (
                self.nome,
                self.cnpj,
                self.info_contato.telefone,
                str(self.info_contato.endereco),
                self.info_contato.redes_sociais
            )
            self.db_conn.connect()
            result = self.db_conn.execute_query(query, params)
            if result:
                # Se a inserção for bem-sucedida, recupera o ID gerado
                query_id = "SELECT LAST_INSERT_ID() as id_fornecedor"
                new_id = self.db_conn.execute_query(query_id, fetch_one=True)
                self._id = new_id["id_fornecedor"]
            else:
                raise ValueError("Erro ao criar fornecedor no banco de dados.")
            self.db_conn.disconnect()
        else:
            # Se um ID for fornecido, tenta carregar o fornecedor do banco de dados
            query = "SELECT * FROM fornecedor WHERE id_fornecedor = %s"
            params = (id_fornecedor,)
            self.db_conn.connect()
            fornecedor_data = self.db_conn.execute_query(query, params, fetch_one=True)
            self.db_conn.disconnect()

            if fornecedor_data:
                self._id = fornecedor_data["id_fornecedor"]
                self.nome = fornecedor_data["nome"]
                self.cnpj = fornecedor_data["cnpj"]
                self.info_contato = mod_info.Informacao(
                    fornecedor_data["telefone"],
                    fornecedor_data["endereco"],
                    fornecedor_data["redes"]
                )
            else:
                raise ValueError(f"Fornecedor com ID {id_fornecedor} não encontrado.")

    def __str__(self) -> str:
        return (f"ID: {self._id}, Nome: {self._nome}, CNPJ: {self._cnpj}\n"
                f"  Informações de Contato: {self.info_contato}")

    def __repr__(self) -> str:
        return (f"Fornecedor(id_fornecedor={self._id!r}, nome={self._nome!r}, cnpj={self._cnpj!r}, "
                f"info_contato={self.info_contato!r})")

    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, nome_str: str) -> None:
        nome_limpo = nome_str.strip()
        if not nome_limpo:
            raise ValueError("O nome do fornecedor não pode ser vazio.")
        self._nome = nome_limpo

    @property
    def cnpj(self) -> str:
        return self._cnpj

    @cnpj.setter
    def cnpj(self, cnpj_str: str) -> None:
        cnpj_limpo: str = re.sub(r'\D', '', cnpj_str)
        if len(cnpj_limpo) != 14:
            raise ValueError("CNPJ inválido: Deve conter exatamente 14 dígitos.")
        if not Fornecedor._eh_cnpj_valido(cnpj_limpo):
            raise ValueError("CNPJ inválido: Dígitos verificadores não correspondem ou padrão inválido.")
        cnpj_formatado: str = (
            f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/"
            f"{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        )
        self._cnpj = cnpj_formatado

    @staticmethod
    def _eh_cnpj_valido(numeros_cnpj: str) -> bool:
        if not numeros_cnpj.isdigit() or len(numeros_cnpj) != 14:
            return False

        if len(set(numeros_cnpj)) == 1:
            return False
        soma1: int = 0
        multiplicadores1: list[int] = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(12):
            soma1 += int(numeros_cnpj[i]) * multiplicadores1[i]
        primeiro_dv_calculado: int = 11 - (soma1 % 11)
        if primeiro_dv_calculado > 9:
            primeiro_dv_calculado = 0
        if primeiro_dv_calculado != int(numeros_cnpj[12]):
            return False
        soma2: int = 0
        multiplicadores2: list[int] = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(13):
            soma2 += int(numeros_cnpj[i]) * multiplicadores2[i]
        segundo_dv_calculado: int = 11 - (soma2 % 11)
        if segundo_dv_calculado > 9:
            segundo_dv_calculado = 0
        return segundo_dv_calculado == int(numeros_cnpj[13])


    @property
    def info_contato(self) -> mod_info.Informacao:
        return self._info_contato

    @info_contato.setter
    def info_contato(self, nova_info: mod_info.Informacao) -> None:
        if not isinstance(nova_info, mod_info.Informacao):
            raise TypeError("A informação de contato deve ser uma instância da classe Informacao.")
        self._info_contato = nova_info

    @staticmethod
    def buscar_fornecedor(cnpj: str) -> Optional["Fornecedor"]:
        query = "SELECT * FROM fornecedor WHERE cnpj = %s"
        params = (cnpj,)
        Fornecedor.db_conn.connect()
        fornecedor_data = Fornecedor.db_conn.execute_query(query, params, fetch_one=True)
        Fornecedor.db_conn.disconnect()
        if fornecedor_data:
            return Fornecedor(
                fornecedor_data["id_fornecedor"],
                fornecedor_data["nome"],
                fornecedor_data["cnpj"],
                mod_info.Informacao(
                    fornecedor_data["telefone"],
                    fornecedor_data["endereco"],
                    fornecedor_data["redes"]
                )
            )
        return None

    @staticmethod
    def buscar_fornecedor_id(id_fornecedor: int) -> Optional["Fornecedor"]:
        query = "SELECT * FROM fornecedor WHERE id_fornecedor = %s"
        params = (id_fornecedor,)
        Fornecedor.db_conn.connect()
        fornecedor_data = Fornecedor.db_conn.execute_query(query, params, fetch_one=True)
        Fornecedor.db_conn.disconnect()
        if fornecedor_data:
            return Fornecedor(
                fornecedor_data["id_fornecedor"],
                fornecedor_data["nome"],
                fornecedor_data["cnpj"],
                mod_info.Informacao(
                    fornecedor_data["telefone"],
                    fornecedor_data["endereco"],
                    fornecedor_data["redes"]
                )
            )
        return None

    @staticmethod
    def buscar_fornecedor_por_nome_exato(nome: str) -> Optional["Fornecedor"]:
        query = "SELECT * FROM fornecedor WHERE LOWER(nome) = LOWER(%s)"
        params = (nome,)
        Fornecedor.db_conn.connect()
        fornecedor_data = Fornecedor.db_conn.execute_query(query, params, fetch_one=True)
        Fornecedor.db_conn.disconnect()
        if fornecedor_data:
            return Fornecedor(
                fornecedor_data["id_fornecedor"],
                fornecedor_data["nome"],
                fornecedor_data["cnpj"],
                mod_info.Informacao(
                    fornecedor_data["telefone"],
                    fornecedor_data["endereco"],
                    fornecedor_data["redes"]
                )
            )
        return None

    @staticmethod
    def buscar_fornecedores_por_nome_parcial(nome_parcial: str) -> list["Fornecedor"]:
        query = "SELECT * FROM fornecedor WHERE LOWER(nome) LIKE %s"
        params = (f"%{nome_parcial.lower()}%",)
        Fornecedor.db_conn.connect()
        fornecedores_data = Fornecedor.db_conn.execute_query(query, params, fetch_all=True)
        Fornecedor.db_conn.disconnect()
        resultados = []
        if fornecedores_data:
            for fornecedor_data in fornecedores_data:
                resultados.append(Fornecedor(
                    fornecedor_data["id_fornecedor"],
                    fornecedor_data["nome"],
                    fornecedor_data["cnpj"],
                    mod_info.Informacao(
                        fornecedor_data["telefone"],
                        fornecedor_data["endereco"],
                        fornecedor_data["redes"]
                    )
                ))
        return resultados

    @staticmethod
    def listar_fornecedores() -> list["Fornecedor"]:
        query = "SELECT * FROM fornecedor"
        Fornecedor.db_conn.connect()
        fornecedores_data = Fornecedor.db_conn.execute_query(query, fetch_all=True)
        Fornecedor.db_conn.disconnect()
        resultados = []
        if fornecedores_data:
            for fornecedor_data in fornecedores_data:
                resultados.append(Fornecedor(
                    fornecedor_data["id_fornecedor"],
                    fornecedor_data["nome"],
                    fornecedor_data["cnpj"],
                    mod_info.Informacao(
                        fornecedor_data["telefone"],
                        fornecedor_data["endereco"],
                        fornecedor_data["redes"]
                    )
                ))
        return resultados

    @staticmethod
    def atualizar_dados_fornecedor(id_fornecedor: int, **kwargs: Any) -> None:
        fornecedor_existente: Optional["Fornecedor"] = Fornecedor.buscar_fornecedor_id(id_fornecedor)
        if not fornecedor_existente:
            raise ValueError(f"Fornecedor com ID {id_fornecedor} não encontrado para atualização.")

        updates = []
        params = []

        for chave, valor in kwargs.items():
            if chave == "id_fornecedor":
                continue
            if chave == "info_contato":
                if not isinstance(valor, mod_info.Informacao):
                    raise TypeError("A informação de contato deve ser uma instância da classe Informacao.")
                updates.append("telefone = %s")
                params.append(valor.telefone)
                updates.append("endereco = %s")
                params.append(str(valor.endereco))
                updates.append("redes = %s")
                params.append(valor.redes_sociais)
            elif chave == "cnpj":
                # Validação de CNPJ já ocorre no setter da classe Fornecedor
                fornecedor_existente.cnpj = valor # Chama o setter para validação
                updates.append(f"{chave} = %s")
                params.append(fornecedor_existente.cnpj)
            elif hasattr(fornecedor_existente, chave):
                updates.append(f"{chave} = %s")
                setattr(fornecedor_existente, chave, valor) # Valida o valor antes de adicionar aos params
                params.append(getattr(fornecedor_existente, chave))

        if updates:
            query = f"UPDATE fornecedor SET {', '.join(updates)} WHERE id_fornecedor = %s"
            params.append(id_fornecedor)
            Fornecedor.db_conn.connect()
            Fornecedor.db_conn.execute_query(query, params)
            Fornecedor.db_conn.disconnect()

    @staticmethod
    def atualizar_cnpj_fornecedor(id_fornecedor: int, novo_cnpj: str) -> None:
        fornecedor: Optional["Fornecedor"] = Fornecedor.buscar_fornecedor_id(id_fornecedor)
        if not fornecedor:
            raise ValueError(f"Fornecedor com ID {id_fornecedor} não encontrado para atualização de CNPJ.")

        # A validação do CNPJ ocorre no setter da classe Fornecedor
        fornecedor.cnpj = novo_cnpj

        query = "UPDATE fornecedor SET cnpj = %s WHERE id_fornecedor = %s"
        params = (fornecedor.cnpj, id_fornecedor)
        Fornecedor.db_conn.connect()
        Fornecedor.db_conn.execute_query(query, params)
        Fornecedor.db_conn.disconnect()

    @staticmethod
    def deletar_fornecedor(id_fornecedor: int) -> None:
        query = "DELETE FROM fornecedor WHERE id_fornecedor = %s"
        params = (id_fornecedor,)
        Fornecedor.db_conn.connect()
        result = Fornecedor.db_conn.execute_query(query, params)
        Fornecedor.db_conn.disconnect()
        if not result:
            raise ValueError(f"Fornecedor com ID {id_fornecedor} não encontrado para exclusão.")

    @staticmethod
    def criar_fornecedor(nome: str, cnpj: str, info_contato: mod_info.Informacao) -> "Fornecedor":
        novo_fornecedor = Fornecedor(None, nome, cnpj, info_contato)
        return novo_fornecedor

    @staticmethod
    def _formatar_fornecedores_para_tabela(fornecedores: list["Fornecedor"]) -> str:
        if not fornecedores:
            return "Nenhum fornecedor para exibir."

        cabecalhos = ["ID", "Nome", "CNPJ", "Telefone"]
        dados_tabela = []

        for forn in fornecedores:
            telefone_str = forn.info_contato.telefone
            
            dados_tabela.append([
                forn.id,
                forn.nome,
                forn.cnpj,
                telefone_str,
            ])
        
        return tabulate(dados_tabela, headers=cabecalhos, tablefmt="grid")


