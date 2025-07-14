from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QDateEdit, QComboBox, QScrollArea,
                               QTextEdit, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
import backend
import database
import cliente as crud_cliente
import funcionario as crud_funcionario
import venda as crud_venda
import despesa as crud_despesa

class WidgetRelatorios(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_session = database.SessionLocal()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Título da Página
        title_label = QLabel("<h2>📊 Relatórios Financeiros e de Operações</h2>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Controles de Filtro
        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.Shape.StyledPanel)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        # Data Inicial
        label_data_inicio = QLabel("Data Início:")
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(label_data_inicio)
        filter_layout.addWidget(self.date_start)

        # Data Final
        label_data_fim = QLabel("Data Fim:")
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDate(QDate.currentDate())
        filter_layout.addWidget(label_data_fim)
        filter_layout.addWidget(self.date_end)

        # Tipo de Relatório
        label_tipo_relatorio = QLabel("Tipo de Relatório:")
        self.combo_report_type = QComboBox()
        self.combo_report_type.addItems([
            "Relatório Mensal",
            "Relatório de Clientes",
            "Relatório de Funcionários",
            "Relatório de Vendas",
            "Relatório de Despesas"
        ])
        filter_layout.addWidget(label_tipo_relatorio)
        filter_layout.addWidget(self.combo_report_type)

        # Botão Gerar Relatório
        self.btn_generate = QPushButton("Gerar Relatório")
        self.btn_generate.clicked.connect(self.generate_report)
        filter_layout.addWidget(self.btn_generate)

        main_layout.addWidget(filter_frame)

        # Área de Texto para Exibir Relatório
        self.report_area = QTextEdit()
        self.report_area.setReadOnly(True)
        self.report_area.setFont(QFont("Courier", 10))
        main_layout.addWidget(self.report_area)

    def generate_report(self):
        report_type = self.combo_report_type.currentText()
        start_date = self.date_start.date().toPython()
        end_date = self.date_end.date().toPython()

        if report_type == "Relatório Mensal":
            self.generate_monthly_report(start_date, end_date)
        elif report_type == "Relatório de Clientes":
            self.generate_client_report()
        elif report_type == "Relatório de Funcionários":
            self.generate_employee_report()
        elif report_type == "Relatório de Vendas":
            self.generate_sales_report(start_date, end_date)
        elif report_type == "Relatório de Despesas":
            self.generate_expense_report(start_date, end_date)
        else:
            self.report_area.setText("Tipo de relatório desconhecido.")

    def generate_monthly_report(self, start_date, end_date):
        # Summarize sales and expenses in the period
        vendas = crud_venda.listar_vendas(self.db_session, data_inicio=start_date, data_fim=end_date)
        despesas = crud_despesa.listar_despesas(self.db_session, data_inicio=start_date, data_fim=end_date)

        total_vendas = sum(v.valor_total for v in vendas)
        total_despesas = sum(d.valor_total for d in despesas)
        lucro = total_vendas - total_despesas

        report_text = f"Relatório Mensal de {start_date} até {end_date}\n"
        report_text += f"Total de Vendas: R$ {total_vendas:.2f}\n"
        report_text += f"Total de Despesas: R$ {total_despesas:.2f}\n"
        report_text += f"Lucro Líquido: R$ {lucro:.2f}\n"

        self.report_area.setText(report_text)

    def generate_client_report(self):
        clientes = crud_cliente.listar_clientes(self.db_session)
        report_text = "Relatório de Clientes\n"
        report_text += f"Total de Clientes: {len(clientes)}\n\n"
        for c in clientes:
            report_text += f"ID: {c.id} - Nome: {c.nome} - Telefone: {c.info_contato.telefone}\n"
        self.report_area.setText(report_text)

    def generate_employee_report(self):
        funcionarios = crud_funcionario.listar_funcionarios(self.db_session)
        report_text = "Relatório de Funcionários\n"
        report_text += f"Total de Funcionários: {len(funcionarios)}\n\n"
        for f in funcionarios:
            report_text += f"ID: {f.id} - Nome: {f.nome} - Salário: R$ {f.salario:.2f}\n"
        self.report_area.setText(report_text)

    def generate_sales_report(self, start_date, end_date):
        vendas = crud_venda.listar_vendas(self.db_session, data_inicio=start_date, data_fim=end_date)
        report_text = f"Relatório de Vendas de {start_date} até {end_date}\n"
        report_text += f"Total de Vendas: {len(vendas)}\n\n"
        for v in vendas:
            report_text += f"ID: {v.id} - Cliente: {v.cliente.nome} - Valor: R$ {v.valor_total:.2f} - Data: {v.data_venda}\n"
        self.report_area.setText(report_text)

    def generate_expense_report(self, start_date, end_date):
        despesas = crud_despesa.listar_despesas(self.db_session, data_inicio=start_date, data_fim=end_date)
        report_text = f"Relatório de Despesas de {start_date} até {end_date}\n"
        report_text += f"Total de Despesas: {len(despesas)}\n\n"
        for d in despesas:
            report_text += f"ID: {d.id} - Descrição: {getattr(d, 'tipo_despesa_str', 'N/A')} - Valor: R$ {d.valor_total:.2f} - Data: {d.data_despesa}\n"
        self.report_area.setText(report_text)
        
        
