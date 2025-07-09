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
