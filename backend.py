from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QTableView, QStackedWidget, QListWidget, QListWidgetItem,
                               QDialog, QLineEdit, QFormLayout, QMessageBox, QDialogButtonBox,
                               QComboBox, QDateEdit, QDoubleSpinBox, QCalendarWidget, QHeaderView,
                               QLabel, QTimeEdit, QScrollArea, QButtonGroup, QCompleter)
from PySide6.QtCore import (Qt, QAbstractTableModel, QModelIndex, QTime, QDate, QStringListModel)
from PySide6.QtGui import QFont, QPalette, QColor
import sys
from datetime import datetime, time
from typing import Optional, List, Any

import database
import cliente as crud_cliente
import funcionario as crud_funcionario
import produto as crud_produto
import servico as crud_servico
import maquina as crud_maquina
from maquina import StatusMaquina
import fornecedor as crud_fornecedor
import suprimento as crud_suprimento
import agenda as crud_agenda
from agenda import ItemAgendado
import despesa as crud_despesa
import venda as crud_venda
import info as mod_info


class ModeloTabelaSqlAlchemy(QAbstractTableModel):
    def __init__(self, colunas: List[str], parent=None):
        super().__init__(parent); self._dados, self._objetos, self._colunas = [], [], colunas; self.db_session = database.SessionLocal(); self.carregar_dados()
    def rowCount(self, parent=QModelIndex()): return len(self._dados)
    def columnCount(self, parent=QModelIndex()): return len(self._colunas)
    def headerData(self, s, o, r=Qt.ItemDataRole.DisplayRole):
        if r == Qt.ItemDataRole.DisplayRole and o == Qt.Orientation.Horizontal: return self._colunas[s]
    def data(self, i, r=Qt.ItemDataRole.DisplayRole):
        if i.isValid() and r == Qt.ItemDataRole.DisplayRole: return self._dados[i.row()][i.column()]
    def obter_objeto_por_indice(self, i):
        if i.isValid() and 0 <= i.row() < len(self._objetos): return self._objetos[i.row()]
    def carregar_dados(self): raise NotImplementedError
    def atualizar_dados(self): self.db_session.expire_all(); self.beginResetModel(); self.carregar_dados(); self.endResetModel()
    def __del__(self): self.db_session.close()

class ModeloCliente(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "CPF", "Nascimento", "Telefone", "Email"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_cliente.Cliente).order_by(crud_cliente.Cliente.id).all(); self._dados = [[ o.nome, o.cpf, o.nascimento.strftime('%d/%m/%Y'), o.info_contato.telefone, o.info_contato.email] for o in self._objetos]

class ModeloFuncionario(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "CPF", "Admissão", "Salário"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_funcionario.Funcionario).order_by(crud_funcionario.Funcionario.id).all(); self._dados = [[ o.nome, o.cpf, o.data_admissao.strftime('%d/%m/%Y'), f"R$ {o.salario:.2f}"] for o in self._objetos]

class ModeloProduto(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "Preço Venda", "Estoque"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_produto.Produto).order_by(crud_produto.Produto.id).all(); self._dados = [[ o.nome, f"R$ {o.preco:.2f}", f"{o.estoque:.2f}"] for o in self._objetos]

class ModeloServico(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "Valor de Venda"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_servico.Servico).order_by(crud_servico.Servico.id).all(); self._dados = [[ o.nome, f"R$ {o.valor_venda:.2f}"] for o in self._objetos]

class ModeloFornecedor(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "CNPJ", "Telefone"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_fornecedor.Fornecedor).order_by(crud_fornecedor.Fornecedor.id).all(); self._dados = [[o.nome, o.cnpj, o.telefone] for o in self._objetos]

class ModeloSuprimento(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "Unidade", "Custo", "Estoque"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_suprimento.Suprimento).order_by(crud_suprimento.Suprimento.id).all(); self._dados = [[o.nome, o.unidade_medida, f"R$ {o.custo_unitario:.2f}", f"{o.estoque:.2f}"] for o in self._objetos]

class ModeloMaquina(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Nome", "Nº Série", "Status"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_maquina.Maquina).order_by(crud_maquina.Maquina.id).all(); self._dados = [[ o.nome, o.numero_serie, o.status.value] for o in self._objetos]

class ModeloVenda(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__([ "Data", "Funcionário", "Cliente", "Valor"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_venda.Venda).order_by(crud_venda.Venda.data_venda.desc()).all(); self._dados = [[ o.data_venda.strftime('%d/%m/%Y'), o.funcionario.nome, o.cliente.nome, f"R$ {o.valor_total:.2f}"] for o in self._objetos]

class ModeloDespesa(ModeloTabelaSqlAlchemy):
    def __init__(self, parent=None): super().__init__(["Data", "Tipo", "Valor", "Detalhes"], parent)
    def carregar_dados(self): self._objetos = self.db_session.query(crud_despesa.Despesa).order_by(crud_despesa.Despesa.data_despesa.desc()).all(); self._dados = [[ o.data_despesa.strftime("%d/%m/%Y"), o.__class__.__name__, f"R$ {o.valor_total:.2f}", self._obter_detalhes(o)] for o in self._objetos]
    def _obter_detalhes(self, d: crud_despesa.Despesa) -> str:
        if isinstance(d, crud_despesa.Compra): return f"Item: {d.item_descricao or d.item_tipo} | Forn: {d.fornecedor_obj.nome}"
        if isinstance(d, crud_despesa.FixoTerceiro): return f"{d.tipo_despesa_str} | Forn: {d.fornecedor_obj.nome if d.fornecedor_obj else 'N/A'}"
        if isinstance(d, crud_despesa.Salario): return f"Salário: {d.funcionario_obj.nome} (Bruto: R${d.salario_bruto:.2f})"
        if isinstance(d, crud_despesa.Comissao): return f"Comissão: {d.funcionario_obj.nome}"
        if isinstance(d, crud_despesa.Outros): return d.tipo_despesa_str
        return d.comentario or "N/A"

class ModeloItensAgenda(QAbstractTableModel):
    def __init__(self, dados, parent=None): super().__init__(parent); self._dados = dados
    def rowCount(self, parent=QModelIndex()): return len(self._dados)
    def columnCount(self, parent=QModelIndex()): return 2
    def headerData(self, s, o, r=Qt.ItemDataRole.DisplayRole):
        if r == Qt.ItemDataRole.DisplayRole and o == Qt.Orientation.Horizontal: return ["Item", "Quantidade"][s]
    def data(self, i, r=Qt.ItemDataRole.DisplayRole):
        if i.isValid() and r == Qt.ItemDataRole.DisplayRole: return self._dados[i.row()][["nome", "quantidade"][i.column()]]

class DialogoBase(QDialog):
    NOME_ENTIDADE = "Entidade"
    def __init__(self, objeto_edicao: Optional[Any] = None, parent: Optional[QWidget] = None, db_session=None):
        super().__init__(parent); self.objeto_edicao = objeto_edicao; self.setWindowTitle(f"{'Editar' if objeto_edicao else 'Adicionar'} {self.NOME_ENTIDADE}"); self.setMinimumWidth(450)
        self.layout = QVBoxLayout(self); self.form_layout = QFormLayout(); self.db_session = db_session or database.SessionLocal(); self._is_session_owner = not db_session
        self.criar_widgets()
        if self.objeto_edicao: self.preencher_dados()
        self.botoes = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel); self.botoes.accepted.connect(self.accept); self.botoes.rejected.connect(self.reject)
        self.layout.addLayout(self.form_layout); self.layout.addWidget(self.botoes)
    def criar_widgets(self): raise NotImplementedError
    def preencher_dados(self): pass
    def salvar_dados(self): raise NotImplementedError
    def accept(self):
        try: 
            self.salvar_dados(); 
            self.db_session.commit();
            QMessageBox.information(self, "Sucesso", "Operação realizada com sucesso."); 
            super().accept()
        except Exception as e: 
            self.db_session.rollback(); 
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {e}\n\nA operação foi revertida.")
   
    def __del__(self):
        if hasattr(self, '_is_session_owner') and self._is_session_owner: 
            self.db_session.close()

class DialogoCliente(DialogoBase):
    NOME_ENTIDADE = "Cliente"
    def criar_widgets(self):
        self.nome_input, self.cpf_input, self.nascimento_input = QLineEdit(), QLineEdit(), QDateEdit(calendarPopup=True)
        self.telefone_input, self.email_input, self.endereco_input = QLineEdit(), QLineEdit(), QLineEdit()
        self.cpf_input.setInputMask("000.000.000-00;_"); self.nascimento_input.setDisplayFormat("dd/MM/yyyy"); self.nascimento_input.setDate(QDate.currentDate().addYears(-18))
        self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("CPF:", self.cpf_input); self.form_layout.addRow("Nascimento:", self.nascimento_input); self.form_layout.addRow("Telefone:", self.telefone_input); self.form_layout.addRow("E-mail:", self.email_input); self.form_layout.addRow("Endereço:", self.endereco_input)
    def preencher_dados(self):
        self.nome_input.setText(self.objeto_edicao.nome); self.cpf_input.setText(self.objeto_edicao.cpf); self.nascimento_input.setDate(self.objeto_edicao.nascimento); self.telefone_input.setText(self.objeto_edicao.info_contato.telefone); self.email_input.setText(self.objeto_edicao.info_contato.email); self.endereco_input.setText(self.objeto_edicao.endereco_str)
    def salvar_dados(self):
        info = mod_info.Informacao(self.telefone_input.text(), self.email_input.text(), self.endereco_input.text() or "Rua, 1", ""); dados = {'nome': self.nome_input.text(), 'cpf': self.cpf_input.text(), 'nascimento_obj': self.nascimento_input.date().toPython(), 'info_contato': info}
        if self.objeto_edicao: crud_cliente.atualizar_dados_cliente(self.db_session, self.objeto_edicao.id, **{k.replace('_obj', ''): v for k, v in dados.items()})
        else: crud_cliente.criar_cliente(self.db_session, **dados)

class DialogoFuncionario(DialogoBase):
    NOME_ENTIDADE = "Funcionário"
    def criar_widgets(self):
        self.nome_input, self.cpf_input, self.ctps_input = QLineEdit(), QLineEdit(), QLineEdit(); self.nascimento_input, self.admissao_input = QDateEdit(calendarPopup=True), QDateEdit(calendarPopup=True); self.salario_input = QDoubleSpinBox(maximum=99999.99, prefix="R$ "); self.telefone_input, self.email_input, self.endereco_input = QLineEdit(), QLineEdit(), QLineEdit(); self.cpf_input.setInputMask("000.000.000-00;_"); self.nascimento_input.setDisplayFormat("dd/MM/yyyy"); self.nascimento_input.setDate(QDate.currentDate().addYears(-18)); self.admissao_input.setDisplayFormat("dd/MM/yyyy"); self.admissao_input.setDate(QDate.currentDate()); self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("CPF:", self.cpf_input); self.form_layout.addRow("Nascimento:", self.nascimento_input); self.form_layout.addRow("CTPS:", self.ctps_input); self.form_layout.addRow("Salário:", self.salario_input); self.form_layout.addRow("Admissão:", self.admissao_input); self.form_layout.addRow("Telefone:", self.telefone_input); self.form_layout.addRow("E-mail:", self.email_input); self.form_layout.addRow("Endereço:", self.endereco_input)
    def preencher_dados(self):
        self.nome_input.setText(self.objeto_edicao.nome); self.cpf_input.setText(self.objeto_edicao.cpf); self.nascimento_input.setDate(self.objeto_edicao.nascimento); self.ctps_input.setText(self.objeto_edicao.ctps); self.salario_input.setValue(self.objeto_edicao.salario); self.admissao_input.setDate(self.objeto_edicao.data_admissao); self.telefone_input.setText(self.objeto_edicao.info_contato.telefone); self.email_input.setText(self.objeto_edicao.info_contato.email); self.endereco_input.setText(self.objeto_edicao.endereco_str)
    def salvar_dados(self):
        info = mod_info.Informacao(self.telefone_input.text(), self.email_input.text(), self.endereco_input.text() or "Rua, 1", ""); dados = {'nome': self.nome_input.text(), 'nascimento_obj': self.nascimento_input.date().toPython(), 'cpf': self.cpf_input.text(), 'ctps': self.ctps_input.text(), 'informacao_contato': info, 'salario': self.salario_input.value(), 'data_admissao_obj': self.admissao_input.date().toPython()}
        if self.objeto_edicao:
            dados_upd = {k.replace('_obj', ''): v for k, v in dados.items()}; dados_upd['info_contato'] = dados_upd.pop('informacao_contato'); crud_funcionario.atualizar_dados_funcionario(self.db_session, self.objeto_edicao.id, **dados_upd)
        else: crud_funcionario.criar_funcionario(self.db_session, **dados)

class DialogoProduto(DialogoBase):
    NOME_ENTIDADE = "Produto"
    def criar_widgets(self): self.nome_input = QLineEdit(); self.preco_input = QDoubleSpinBox(maximum=99999.99, prefix="R$ "); self.estoque_input = QDoubleSpinBox(maximum=99999.99); self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("Preço Venda:", self.preco_input); self.form_layout.addRow("Estoque:", self.estoque_input)
    def preencher_dados(self): self.nome_input.setText(self.objeto_edicao.nome); self.preco_input.setValue(self.objeto_edicao.preco); self.estoque_input.setValue(self.objeto_edicao.estoque)
    def salvar_dados(self): dados = {'nome': self.nome_input.text(), 'preco': self.preco_input.value(), 'estoque': self.estoque_input.value()}; (crud_produto.atualizar_dados_produto(self.db_session, self.objeto_edicao.id, **dados) if self.objeto_edicao else crud_produto.criar_produto(self.db_session, **dados))

class DialogoServico(DialogoBase):
    NOME_ENTIDADE = "Serviço"
    def criar_widgets(self): self.nome_input = QLineEdit(); self.valor_venda_input = QDoubleSpinBox(maximum=99999.99, prefix="R$ "); self.custo_input = QDoubleSpinBox(maximum=99999.99, prefix="R$ "); self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("Valor Venda:", self.valor_venda_input); self.form_layout.addRow("Custo:", self.custo_input)
    def preencher_dados(self): self.nome_input.setText(self.objeto_edicao.nome); self.valor_venda_input.setValue(self.objeto_edicao.valor_venda); self.custo_input.setValue(self.objeto_edicao.custo)
    def salvar_dados(self): dados = {'nome': self.nome_input.text(), 'valor_venda': self.valor_venda_input.value(), 'custo': self.custo_input.value()}; (crud_servico.atualizar_dados_servico(self.db_session, self.objeto_edicao.id, **dados) if self.objeto_edicao else crud_servico.criar_servico(self.db_session, **dados))

class DialogoFornecedor(DialogoBase):
    NOME_ENTIDADE = "Fornecedor"
    def criar_widgets(self): self.nome_input, self.cnpj_input = QLineEdit(), QLineEdit(); self.telefone_input, self.email_input, self.endereco_input = QLineEdit(), QLineEdit(), QLineEdit(); self.cnpj_input.setInputMask("00.000.000/0000-00;_"); self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("CNPJ:", self.cnpj_input); self.form_layout.addRow("Telefone:", self.telefone_input); self.form_layout.addRow("E-mail:", self.email_input); self.form_layout.addRow("Endereço:", self.endereco_input)
    def preencher_dados(self): self.nome_input.setText(self.objeto_edicao.nome); self.cnpj_input.setText(self.objeto_edicao.cnpj); self.telefone_input.setText(self.objeto_edicao.info_contato.telefone); self.email_input.setText(self.objeto_edicao.info_contato.email); self.endereco_input.setText(self.objeto_edicao.endereco_str)
    def salvar_dados(self): info = mod_info.Informacao(self.telefone_input.text(), self.email_input.text(), self.endereco_input.text() or "Rua, 1", ""); dados = {'nome': self.nome_input.text(), 'cnpj': self.cnpj_input.text(), 'info_contato': info}; (crud_fornecedor.atualizar_dados_fornecedor(self.db_session, self.objeto_edicao.id, **dados) if self.objeto_edicao else crud_fornecedor.criar_fornecedor(self.db_session, **dados))

class DialogoSuprimento(DialogoBase):
    NOME_ENTIDADE = "Suprimento"
    def criar_widgets(self): self.nome_input, self.unidade_input = QLineEdit(), QLineEdit(); self.custo_input = QDoubleSpinBox(maximum=99999.99, prefix="R$ "); self.estoque_input = QDoubleSpinBox(maximum=99999.99); self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("Unidade Medida:", self.unidade_input); self.form_layout.addRow("Custo Unitário:", self.custo_input); self.form_layout.addRow("Estoque:", self.estoque_input)
    def preencher_dados(self): self.nome_input.setText(self.objeto_edicao.nome); self.unidade_input.setText(self.objeto_edicao.unidade_medida); self.custo_input.setValue(self.objeto_edicao.custo_unitario); self.estoque_input.setValue(self.objeto_edicao.estoque)
    def salvar_dados(self): dados = {'nome': self.nome_input.text(), 'unidade_medida': self.unidade_input.text(), 'custo_unitario': self.custo_input.value(), 'estoque': self.estoque_input.value()}; (crud_suprimento.atualizar_dados_suprimento(self.db_session, self.objeto_edicao.id, **dados) if self.objeto_edicao else crud_suprimento.criar_suprimento(self.db_session, **dados))

class DialogoMaquina(DialogoBase):
    NOME_ENTIDADE = "Máquina"
    def criar_widgets(self): self.nome_input, self.serie_input = QLineEdit(), QLineEdit(); self.custo_input = QDoubleSpinBox(maximum=999999.99, prefix="R$ "); self.status_combo = QComboBox(); [self.status_combo.addItem(s.value, s) for s in StatusMaquina]; self.form_layout.addRow("Nome:", self.nome_input); self.form_layout.addRow("Nº Série:", self.serie_input); self.form_layout.addRow("Custo Aquisição:", self.custo_input); self.form_layout.addRow("Status:", self.status_combo)
    def preencher_dados(self): self.nome_input.setText(self.objeto_edicao.nome); self.serie_input.setText(self.objeto_edicao.numero_serie); self.custo_input.setValue(self.objeto_edicao.custo_aquisicao); self.status_combo.setCurrentIndex(self.status_combo.findData(self.objeto_edicao.status))
    def salvar_dados(self): dados = {'nome': self.nome_input.text(), 'numero_serie': self.serie_input.text(), 'custo_aquisicao': self.custo_input.value(), 'status': self.status_combo.currentData()}; (crud_maquina.atualizar_dados_maquina(self.db_session, self.objeto_edicao.id, **dados) if self.objeto_edicao else crud_maquina.criar_maquina(self.db_session, **dados))

class DialogoAdicionarItemAgenda(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Adicionar Item"); self.layout = QFormLayout(self); self.item_combo = QComboBox(); self.quantidade_spin = QDoubleSpinBox(minimum=0.01, maximum=999); self.layout.addRow("Item (Serviço/Produto):", self.item_combo); self.layout.addRow("Quantidade:", self.quantidade_spin); self.botoes = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel); self.botoes.accepted.connect(self.accept); self.botoes.rejected.connect(self.reject); self.layout.addWidget(self.botoes); self._popular_itens(); self.resultado = None
    def _popular_itens(self):
        with database.SessionLocal() as db:
            for s in db.query(crud_servico.Servico).all(): self.item_combo.addItem(f"[S] {s.nome}", s)
            for p in db.query(crud_produto.Produto).all(): self.item_combo.addItem(f"[P] {p.nome}", p)
    def accept(self): self.resultado = {"item": self.item_combo.currentData(), "quantidade": self.quantidade_spin.value()}; super().accept()

class DialogoAgenda(DialogoBase):
    NOME_ENTIDADE = "Agendamento"
    def __init__(self, objeto_edicao: Optional[Any] = None, parent: Optional[QWidget] = None, data_selecionada: Optional[QDate] = None, db_session=None):
        self.data_selecionada = data_selecionada or (QDate(objeto_edicao.data_hora_inicio.date()) if objeto_edicao else QDate.currentDate()); self.itens_agendados_memoria = []; self.maquinas_selecionadas = []
        super().__init__(objeto_edicao, parent, db_session)
    def criar_widgets(self):
        self.funcionario_combo = QComboBox(); self.cliente_combo = QComboBox(); self.data_label = QLabel(self.data_selecionada.toString("dd/MM/yyyy")); self.hora_inicio_input = QLineEdit(); self.hora_inicio_input.setInputMask("00:00"); self.hora_fim_input = QLineEdit(); self.hora_fim_input.setInputMask("00:00"); self.form_layout.addRow("Funcionário:", self.funcionario_combo); self.form_layout.addRow("Cliente:", self.cliente_combo); self.form_layout.addRow("Data:", self.data_label); self.form_layout.addRow("Início (HH:MM):", self.hora_inicio_input); self.form_layout.addRow("Fim (HH:MM):", self.hora_fim_input); self._configurar_combo_busca(self.funcionario_combo, crud_funcionario.Funcionario); self._configurar_combo_busca(self.cliente_combo, crud_cliente.Cliente); self.layout.addSpacing(15); self.layout.addWidget(QLabel("<b>Itens do Agendamento</b>")); item_botoes_layout = QHBoxLayout(); btn_add_item = QPushButton("Adicionar Item"); btn_rem_item = QPushButton("Remover Item"); item_botoes_layout.addWidget(btn_add_item); item_botoes_layout.addWidget(btn_rem_item); item_botoes_layout.addStretch(); self.layout.addLayout(item_botoes_layout); self.tabela_itens = QTableView(); self.tabela_itens.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows); self.layout.addWidget(self.tabela_itens); btn_add_item.clicked.connect(self._adicionar_item); btn_rem_item.clicked.connect(self._remover_item)
        
        # Add machine selection UI
        self.layout.addSpacing(15)
        self.layout.addWidget(QLabel("<b>Máquinas do Agendamento</b>"))
        self.maquinas_list = QListWidget()
        self.maquinas_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.layout.addWidget(self.maquinas_list)
        self._carregar_maquinas()
        
    def _carregar_maquinas(self):
        maquinas = self.db_session.query(crud_maquina.Maquina).filter(crud_maquina.Maquina.status == StatusMaquina.OPERANDO).order_by(crud_maquina.Maquina.nome).all()
        for maquina in maquinas:
            item = QListWidgetItem(maquina.nome)
            item.setData(Qt.ItemDataRole.UserRole, maquina)
            self.maquinas_list.addItem(item)
    def preencher_dados(self):
        self.funcionario_combo.setCurrentText(self.objeto_edicao.funcionario.nome)
        self.cliente_combo.setCurrentText(self.objeto_edicao.cliente.nome)
        self.hora_inicio_input.setText(self.objeto_edicao.data_hora_inicio.strftime("%H:%M"))
        self.hora_fim_input.setText(self.objeto_edicao.data_hora_fim.strftime("%H:%M"))
        itens_db = crud_agenda.get_itens_agendados_detalhes(self.db_session, self.objeto_edicao.id)
        for item in itens_db:
            item_obj = self.db_session.query(crud_produto.Produto if '[P]' in item['nome'] else crud_servico.Servico).filter_by(nome=item['nome']).first()
            if item_obj: item['item_obj'] = item_obj
        self.itens_agendados_memoria = itens_db
        self._atualizar_tabela_itens()
        
        # Set selected machines in the list
        maquinas_selecionadas = {m.id for m in self.objeto_edicao.maquinas_agendadas}
        for i in range(self.maquinas_list.count()):
            item = self.maquinas_list.item(i)
            maquina = item.data(Qt.ItemDataRole.UserRole)
            if maquina.id in maquinas_selecionadas:
                item.setSelected(True)
    def _adicionar_item(self):
        dialogo = DialogoAdicionarItemAgenda(self)
        if dialogo.exec() and dialogo.resultado:
            item_selecionado = dialogo.resultado["item"]; qtd = dialogo.resultado["quantidade"]; novo_item = {"nome": item_selecionado.nome, "quantidade": qtd, "item_obj": item_selecionado, "id_associacao": None}; self.itens_agendados_memoria.append(novo_item); self._atualizar_tabela_itens()
    def _remover_item(self):
        selecao = self.tabela_itens.selectionModel().selectedRows()
        if not selecao: QMessageBox.warning(self, "Aviso", "Selecione um item para remover."); return
        del self.itens_agendados_memoria[selecao[0].row()]; self._atualizar_tabela_itens()
    def _atualizar_tabela_itens(self):
        modelo = ModeloItensAgenda(self.itens_agendados_memoria); self.tabela_itens.setModel(modelo)
    def salvar_dados(self):
        func_id = self.funcionario_combo.currentData(); cli_id = self.cliente_combo.currentData()
        if not func_id or not cli_id: raise ValueError("Funcionário e Cliente devem ser válidos e selecionados da lista.")
        dt_inicio = datetime.combine(self.data_selecionada.toPython(), datetime.strptime(self.hora_inicio_input.text(), "%H:%M").time()); dt_fim = datetime.combine(self.data_selecionada.toPython(), datetime.strptime(self.hora_fim_input.text(), "%H:%M").time())
        func_obj = self.db_session.get(crud_funcionario.Funcionario, func_id); cli_obj = self.db_session.get(crud_cliente.Cliente, cli_id)
        itens_para_salvar = [ItemAgendado(i['item_obj'], i['quantidade']) for i in self.itens_agendados_memoria if 'item_obj' in i]
        
        # Get selected machines
        maquinas_selecionadas = []
        for i in range(self.maquinas_list.count()):
            item = self.maquinas_list.item(i)
            if item.isSelected():
                maquinas_selecionadas.append(item.data(Qt.ItemDataRole.UserRole))
        
        if self.objeto_edicao:
            crud_agenda.atualizar_agenda(self.db_session, self.objeto_edicao.id, itens_a_adicionar=itens_para_salvar, maquinas_agendadas=maquinas_selecionadas, data_hora_inicio=dt_inicio, data_hora_fim=dt_fim, funcionario_id=func_id, cliente_id=cli_id)
        else:
            if not itens_para_salvar: raise ValueError("Um novo agendamento deve ter pelo menos um item.")
            crud_agenda.criar_agenda(self.db_session, func_obj, cli_obj, dt_inicio, dt_fim, itens_agendados=itens_para_salvar, maquinas_agendadas=maquinas_selecionadas)
    def _configurar_combo_busca(self, combo: QComboBox, model_class):
        combo.clear()
        items = self.db_session.query(model_class).order_by(model_class.nome).all()
        for item in items:
            combo.addItem(item.nome, item.id)

class DialogoVenda(DialogoBase):
    NOME_ENTIDADE = "Venda"
    def criar_widgets(self):
        self.agenda_combo = QComboBox(); self.data_venda_input = QDateEdit(calendarPopup=True, displayFormat="dd/MM/yyyy", date=QDate.currentDate()); self.label_info = QLabel("Selecione uma agenda com status 'Agendado'.\nCliente e Funcionário serão preenchidos da agenda."); self.label_info.setStyleSheet("font-style: italic; color: gray;"); self.form_layout.addRow(self.label_info); self.form_layout.addRow("Agenda para Faturar:", self.agenda_combo); self.form_layout.addRow("Data da Venda:", self.data_venda_input); self._popular_agendas()
    def _popular_agendas(self):
        agendas = self.db_session.query(crud_agenda.Agenda).filter(crud_agenda.Agenda.status == crud_agenda.AgendaStatus.AGENDADO).all()
        self.agenda_combo.addItem("Selecione uma Agenda...", None); [self.agenda_combo.addItem(f"ID: {ag.id} - {ag.cliente.nome} ({ag.data_hora_inicio.strftime('%d/%m')})", ag.id) for ag in agendas]
    def salvar_dados(self):
        agenda_id = self.agenda_combo.currentData();
        if not agenda_id: raise ValueError("É necessário selecionar uma agenda para faturar.")
        agenda_obj = self.db_session.get(crud_agenda.Agenda, agenda_id); data_venda = self.data_venda_input.date().toPython()
        crud_venda.criar_venda(self.db_session, agenda_obj.funcionario, agenda_obj.cliente, data_venda, itens_venda=[], agenda_obj=agenda_obj)

class DialogoEditarVenda(DialogoBase):
    NOME_ENTIDADE = "Venda"
    def criar_widgets(self): self.data_input = QDateEdit(calendarPopup=True, displayFormat="dd/MM/yyyy"); self.comentario_input = QLineEdit(); self.form_layout.addRow("Data da Venda:", self.data_input); self.form_layout.addRow("Comentário:", self.comentario_input)
    def preencher_dados(self): self.data_input.setDate(self.objeto_edicao.data_venda); self.comentario_input.setText(self.objeto_edicao.comentario or "")
    def salvar_dados(self): crud_venda.atualizar_dados_venda(self.db_session, self.objeto_edicao.id, data_venda=self.data_input.date().toPython(), comentario=self.comentario_input.text())

class DialogoDespesa(DialogoBase):
    NOME_ENTIDADE = "Despesa"
    def criar_widgets(self): self.tipo_combo = QComboBox(); self.form_stack = QStackedWidget(); self.tipo_combo.addItems(["Compra", "Fixo/Terceiro", "Salário", "Outros"]); self.tipo_combo.currentIndexChanged.connect(self.form_stack.setCurrentIndex); self.form_layout.addRow("Tipo de Despesa:", self.tipo_combo); self.layout.insertWidget(1, self.form_stack); self._criar_form_compra(); self._criar_form_fixo(); self._criar_form_salario(); self._criar_form_outros(); self._preencher_combos()
    def _preencher_combos(self):
        for f in self.db_session.query(crud_fornecedor.Fornecedor).all(): self.compra_fornecedor.addItem(f.nome, f.id)
        for p in self.db_session.query(crud_produto.Produto).all(): self.compra_item.addItem(f"[P] {p.nome}", p)
        for s in self.db_session.query(crud_suprimento.Suprimento).all(): self.compra_item.addItem(f"[S] {s.nome}", s)
        for func in self.db_session.query(crud_funcionario.Funcionario).all(): self.salario_func.addItem(func.nome, func.id)
    def _criar_form_compra(self): w=QWidget(); f=QFormLayout(w); self.compra_fornecedor=QComboBox(); self.compra_item=QComboBox(); self.compra_qtd=QDoubleSpinBox(maximum=9999); self.compra_valor=QDoubleSpinBox(maximum=99999, prefix="R$ "); self.compra_data=QDateEdit(calendarPopup=True, date=QDate.currentDate(), displayFormat="dd/MM/yyyy"); f.addRow("Fornecedor:", self.compra_fornecedor); f.addRow("Item:", self.compra_item); f.addRow("Qtd:", self.compra_qtd); f.addRow("Valor Unit.:", self.compra_valor); f.addRow("Data:", self.compra_data); self.form_stack.addWidget(w)
    def _criar_form_fixo(self): w=QWidget(); f=QFormLayout(w); self.fixo_desc=QLineEdit(); self.fixo_valor=QDoubleSpinBox(maximum=99999, prefix="R$ "); self.fixo_data=QDateEdit(calendarPopup=True, date=QDate.currentDate(), displayFormat="dd/MM/yyyy"); f.addRow("Descrição:", self.fixo_desc); f.addRow("Valor:", self.fixo_valor); f.addRow("Data:", self.fixo_data); self.form_stack.addWidget(w)
    def _criar_form_salario(self): w=QWidget(); f=QFormLayout(w); self.salario_func=QComboBox(); self.salario_bruto=QDoubleSpinBox(maximum=99999, prefix="R$ "); self.salario_descontos=QDoubleSpinBox(maximum=99999, prefix="R$ "); self.salario_data=QDateEdit(calendarPopup=True, date=QDate.currentDate(), displayFormat="dd/MM/yyyy"); f.addRow("Funcionário:", self.salario_func); f.addRow("Salário Bruto:", self.salario_bruto); f.addRow("Descontos:", self.salario_descontos); f.addRow("Data:", self.salario_data); self.form_stack.addWidget(w)
    def _criar_form_outros(self): w=QWidget(); f=QFormLayout(w); self.outros_desc=QLineEdit(); self.outros_valor=QDoubleSpinBox(maximum=99999, prefix="R$ "); self.outros_data=QDateEdit(calendarPopup=True, date=QDate.currentDate(), displayFormat="dd/MM/yyyy"); f.addRow("Descrição:", self.outros_desc); f.addRow("Valor:", self.outros_valor); f.addRow("Data:", self.outros_data); self.form_stack.addWidget(w)
    def preencher_dados(self):
        self.tipo_combo.setEnabled(False)
        if isinstance(self.objeto_edicao, crud_despesa.Compra): self.tipo_combo.setCurrentText("Compra"); self.compra_qtd.setValue(self.objeto_edicao.quantidade); self.compra_valor.setValue(self.objeto_edicao.valor_unitario); self.compra_data.setDate(self.objeto_edicao.data_despesa)
        elif isinstance(self.objeto_edicao, crud_despesa.FixoTerceiro): self.tipo_combo.setCurrentText("Fixo/Terceiro"); self.fixo_desc.setText(self.objeto_edicao.tipo_despesa_str); self.fixo_valor.setValue(self.objeto_edicao.valor_total); self.fixo_data.setDate(self.objeto_edicao.data_despesa)
        elif isinstance(self.objeto_edicao, crud_despesa.Salario): self.tipo_combo.setCurrentText("Salário"); self.salario_func.setCurrentIndex(self.salario_func.findData(self.objeto_edicao.funcionario_id)); self.salario_bruto.setValue(self.objeto_edicao.salario_bruto); self.salario_descontos.setValue(self.objeto_edicao.descontos); self.salario_data.setDate(self.objeto_edicao.data_despesa)
        elif isinstance(self.objeto_edicao, crud_despesa.Outros): self.tipo_combo.setCurrentText("Outros"); self.outros_desc.setText(self.objeto_edicao.tipo_despesa_str); self.outros_valor.setValue(self.objeto_edicao.valor_total); self.outros_data.setDate(self.objeto_edicao.data_despesa)
    def salvar_dados(self):
        tipo = self.tipo_combo.currentText()
        if self.objeto_edicao:
            dados = {}
            if tipo == "Compra": dados = {'quantidade': self.compra_qtd.value(), 'valor_unitario': self.compra_valor.value(), 'data_despesa': self.compra_data.date().toPython()}
            elif tipo == "Fixo/Terceiro": dados = {'tipo_despesa_str': self.fixo_desc.text(), 'valor_total': self.fixo_valor.value(), 'data_despesa': self.fixo_data.date().toPython()}
            elif tipo == "Salário": dados = {'salario_bruto': self.salario_bruto.value(), 'descontos': self.salario_descontos.value(), 'data_despesa': self.salario_data.date().toPython()}
            elif tipo == "Outros": dados = {'tipo_despesa_str': self.outros_desc.text(), 'valor_total': self.outros_valor.value(), 'data_despesa': self.outros_data.date().toPython()}
            crud_despesa.atualizar_dados_despesa(self.db_session, self.objeto_edicao.id, **dados)
        else:
            if tipo == "Compra": forn_obj = self.db_session.get(crud_fornecedor.Fornecedor, self.compra_fornecedor.currentData()); item_obj = self.compra_item.currentData(); crud_despesa.criar_compra(self.db_session, forn_obj, item_obj, self.compra_qtd.value(), self.compra_valor.value(), self.compra_data.date().toPython())
            elif tipo == "Fixo/Terceiro": crud_despesa.criar_fixo_terceiro(self.db_session, self.fixo_valor.value(), self.fixo_desc.text(), self.fixo_data.date().toPython())
            elif tipo == "Salário": func_obj = self.db_session.get(crud_funcionario.Funcionario, self.salario_func.currentData()); crud_despesa.criar_salario(self.db_session, func_obj, self.salario_bruto.value(), self.salario_descontos.value(), self.salario_data.date().toPython())
            elif tipo == "Outros": crud_despesa.criar_outros(self.db_session, self.outros_valor.value(), self.outros_desc.text(), self.outros_data.date().toPython())

class WidgetGerenciamento(QWidget):
    def __init__(self, nome_entidade: str, modelo: ModeloTabelaSqlAlchemy, dialogo_add: Optional[type] = None, dialogo_edit: Optional[type] = None, parent=None):
        super().__init__(parent); self.modelo, self.dialogo_add, self.dialogo_edit = modelo, dialogo_add, dialogo_edit or dialogo_add; self.layout = QVBoxLayout(self); botoes_layout = QHBoxLayout(); self.btn_adicionar = QPushButton("Adicionar"); self.btn_editar = QPushButton("Editar"); self.btn_deletar = QPushButton("Deletar"); botoes_layout.addWidget(QLabel(f"<b>Gerenciamento de {nome_entidade}</b>")); botoes_layout.addStretch(); botoes_layout.addWidget(self.btn_adicionar); botoes_layout.addWidget(self.btn_editar); botoes_layout.addWidget(self.btn_deletar); self.layout.addLayout(botoes_layout); self.tabela = QTableView(); self.tabela.setModel(self.modelo); self.tabela.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows); self.tabela.setSelectionMode(QTableView.SelectionMode.SingleSelection); self.tabela.horizontalHeader().setStretchLastSection(True); self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents); self.layout.addWidget(self.tabela); self.btn_adicionar.clicked.connect(self.adicionar_item); self.btn_editar.clicked.connect(self.editar_item); self.btn_deletar.clicked.connect(self.deletar_item)
        if not self.dialogo_add: self.btn_adicionar.setEnabled(False)
        if not self.dialogo_edit: self.btn_editar.setEnabled(False)
    def _executar_dialogo(self, dialogo_cls, objeto=None):
       if dialogo_cls:
            dialogo = dialogo_cls(objeto_edicao=objeto, parent=self, db_session=self.modelo.db_session)
            if dialogo.exec(): 
                self.modelo.atualizar_dados()
                self.tabela.viewport().update()
    def adicionar_item(self): self._executar_dialogo(self.dialogo_add)
    def editar_item(self):
        selecao = self.tabela.selectionModel().selectedRows()
        if not selecao: QMessageBox.warning(self, "Aviso", "Selecione um item para editar."); return
        objeto = self.modelo.obter_objeto_por_indice(selecao[0]);
        if objeto: self._executar_dialogo(self.dialogo_edit, objeto)
    def deletar_item(self):
        selecao = self.tabela.selectionModel().selectedRows()
        if not selecao:
            QMessageBox.warning(self, "Aviso", "Selecione um item para deletar.")
            return
        
        objeto = self.modelo.obter_objeto_por_indice(selecao[0])
        if not objeto:
            return
        if QMessageBox.question(self, "Confirmar", f"Tem certeza que deseja deletar o item ID {objeto.id}?") == QMessageBox.StandardButton.Yes:
            try:
                # Usa a sessão do modelo para deletar o item
                # Isso garante que a mesma sessão que o modelo usa seja atualizada
                item_para_deletar = self.modelo.db_session.get(type(objeto), objeto.id)
                if item_para_deletar:
                    self.modelo.db_session.delete(item_para_deletar)
                    self.modelo.db_session.commit()
                
                QMessageBox.information(self, "Sucesso", "Item deletado com sucesso.")
                self.modelo.atualizar_dados() # Atualiza a tabela após a exclusão
            except Exception as e:
                self.modelo.db_session.rollback() # Reverte em caso de erro
                QMessageBox.critical(self, "Erro", f"Não foi possível deletar o item: {e}")
                
class WidgetAgenda(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.db_session = database.SessionLocal()
        self.calendario = QCalendarWidget()
        self.calendario.selectionChanged.connect(self._atualizar_visualizacao_diaria)
        self.layout.addWidget(self.calendario, 1)

        view_direita = QWidget()
        layout_direita = QVBoxLayout(view_direita)

        self.label_data = QLabel()
        layout_direita.addWidget(self.label_data)

        botoes_layout = QHBoxLayout()
        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_del = QPushButton("Deletar")
        self.btn_atualizar = QPushButton("Atualizar")
        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_add)
        botoes_layout.addWidget(self.btn_edit)
        botoes_layout.addWidget(self.btn_del)
        botoes_layout.addWidget(self.btn_atualizar)
        layout_direita.addLayout(botoes_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.grade_horarios_widget = QWidget()
        self.grade_layout = QVBoxLayout(self.grade_horarios_widget)
        self.scroll_area.setWidget(self.grade_horarios_widget)
        layout_direita.addWidget(self.scroll_area)

        self.layout.addWidget(view_direita, 2)

        self.agendamentos_do_dia = []
        self.grupo_botoes_agenda = QButtonGroup(self)
        self.grupo_botoes_agenda.setExclusive(True)

        self.btn_add.clicked.connect(self.adicionar_agendamento)
        self.btn_edit.clicked.connect(self.editar_agendamento)
        self.btn_del.clicked.connect(self.deletar_agendamento)
        self.btn_atualizar.clicked.connect(self._atualizar_visualizacao_diaria)

        self._atualizar_visualizacao_diaria()
    def _atualizar_visualizacao_diaria(self):
        data_selecionada = self.calendario.selectedDate().toPython()
        self.label_data.setText(f"<b>Agendamentos para {data_selecionada.strftime('%d/%m/%Y')}</b>")
        inicio_dia = datetime.combine(data_selecionada, time.min)
        fim_dia = datetime.combine(data_selecionada, time.max)
        self.db_session.expire_all()
        self.db_session.commit()  # Added commit to refresh database state
        self.agendamentos_do_dia = self.db_session.query(crud_agenda.Agenda).filter(crud_agenda.Agenda.data_hora_inicio.between(inicio_dia, fim_dia)).order_by(crud_agenda.Agenda.data_hora_inicio).all()
        self._recriar_grade_horarios()
    def _recriar_grade_horarios(self):
        for btn in self.grupo_botoes_agenda.buttons(): self.grupo_botoes_agenda.removeButton(btn)
        while self.grade_layout.count():
            layout_item = self.grade_layout.takeAt(0)
            if layout_item and layout_item.widget(): layout_item.widget().deleteLater()
        for hora in range(7, 20):
            for minuto in (0, 30):
                horario = time(hora, minuto); btn_horario = QPushButton(f"{hora:02d}:{minuto:02d}"); btn_horario.setCheckable(True); agendamento = next((ag for ag in self.agendamentos_do_dia if ag.data_hora_inicio.time() <= horario < ag.data_hora_fim.time()), None)
                if agendamento: btn_horario.setText(f"{agendamento.data_hora_inicio.strftime('%H:%M')} - {agendamento.cliente.nome}\nFuncionário: {agendamento.funcionario.nome}"); btn_horario.setStyleSheet("QPushButton { background-color: #3B7B9A; text-align: left; padding: 5px; border-radius: 3px; border: 1px solid #3B7B9A; } QPushButton:checked { border: 2px solid #00BFFF; }"); self.grupo_botoes_agenda.addButton(btn_horario, agendamento.id)
                else: btn_horario.setEnabled(False)
                self.grade_layout.addWidget(btn_horario)
        self.grade_layout.addStretch()
    def _obter_agenda_selecionada(self):
        id_selecionado = self.grupo_botoes_agenda.checkedId()
        if id_selecionado > 0: return self.db_session.get(crud_agenda.Agenda, id_selecionado)
    def adicionar_agendamento(self):
        dialogo = DialogoAgenda(parent=self, data_selecionada=self.calendario.selectedDate());
        if dialogo.exec(): self._atualizar_visualizacao_diaria()
    def editar_agendamento(self):
        agenda_obj = self._obter_agenda_selecionada()
        if not agenda_obj: QMessageBox.warning(self, "Aviso", "Selecione um agendamento para editar."); return
        dialogo = DialogoAgenda(objeto_edicao=agenda_obj, parent=self, db_session=self.db_session);
        if dialogo.exec(): self._atualizar_visualizacao_diaria()
    def deletar_agendamento(self):
        agenda_obj = self._obter_agenda_selecionada()
        if not agenda_obj: QMessageBox.warning(self, "Aviso", "Selecione um agendamento para deletar."); return
        if QMessageBox.question(self, "Confirmar", f"Deletar agendamento do cliente {agenda_obj.cliente.nome}?") == QMessageBox.StandardButton.Yes:
            try: crud_agenda.deletar_agenda(self.db_session, agenda_obj.id); self._atualizar_visualizacao_diaria()
            except Exception as e: self.db_session.rollback(); QMessageBox.critical(self, "Erro", f"Não foi possível deletar: {e}")

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("Sistema de Gestão Integrado"); self.setGeometry(100, 100, 1280, 800); self.widget_central = QWidget(); self.setCentralWidget(self.widget_central); self.layout_principal = QHBoxLayout(self.widget_central); self.menu_lateral = QListWidget(maximumWidth=200); self.conteudo_stack = QStackedWidget(); fonte_menu = QFont(); fonte_menu.setPointSize(12); self.menu_lateral.setFont(fonte_menu); self.layout_principal.addWidget(self.menu_lateral); self.layout_principal.addWidget(self.conteudo_stack); self.mapear_modulos(); self.menu_lateral.currentItemChanged.connect(lambda curr, prev: self.conteudo_stack.setCurrentIndex(self.menu_lateral.row(curr)));
        if self.menu_lateral.count() > 0: self.menu_lateral.setCurrentRow(0)

    def mapear_modulos(self):
        modulos_config = {"Agenda": ("widget_agenda", WidgetAgenda, None, None, None), "Vendas": ("widget_crud", WidgetGerenciamento, ModeloVenda, DialogoVenda, DialogoEditarVenda), "Despesas": ("widget_crud", WidgetGerenciamento, ModeloDespesa, DialogoDespesa, DialogoDespesa), "Clientes": ("widget_crud", WidgetGerenciamento, ModeloCliente, DialogoCliente, DialogoCliente), "Funcionários": ("widget_crud", WidgetGerenciamento, ModeloFuncionario, DialogoFuncionario, DialogoFuncionario), "Produtos": ("widget_crud", WidgetGerenciamento, ModeloProduto, DialogoProduto, DialogoProduto), "Serviços": ("widget_crud", WidgetGerenciamento, ModeloServico, DialogoServico, DialogoServico), "Fornecedores": ("widget_crud", WidgetGerenciamento, ModeloFornecedor, DialogoFornecedor, DialogoFornecedor), "Suprimentos": ("widget_crud", WidgetGerenciamento, ModeloSuprimento, DialogoSuprimento, DialogoSuprimento), "Máquinas": ("widget_crud", WidgetGerenciamento, ModeloMaquina, DialogoMaquina, DialogoMaquina)}
        for nome, config in modulos_config.items():
            tipo_widget, widget_or_model_cls, p2, p3, p4 = config
            if tipo_widget == "widget_agenda": widget = widget_or_model_cls()
            else: widget = widget_or_model_cls(nome, p2(), p3, p4)
            self.menu_lateral.addItem(nome); self.conteudo_stack.addWidget(widget)

if __name__ == "__main__":
    database.criar_banco(); app = QApplication(sys.argv); app.setStyle("Fusion"); palette = QPalette(); palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53)); palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white); palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25)); palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53)); palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white); palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white); palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white); palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53)); palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white); palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red); palette.setColor(QPalette.ColorRole.Link, QColor("#8a2be2")); palette.setColor(QPalette.ColorRole.Highlight, QColor("#8a2be2")); palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black); app.setPalette(palette); janela = JanelaPrincipal(); janela.show(); sys.exit(app.exec())