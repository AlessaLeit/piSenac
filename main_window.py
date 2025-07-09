import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea,
                               QGridLayout, QStackedWidget, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QColor
from functools import partial

# Importações dos módulos do teeste.py
from backend import (database, WidgetGerenciamento, WidgetAgenda,
    ModeloCliente, DialogoCliente,
    ModeloFuncionario, DialogoFuncionario,
    ModeloProduto, DialogoProduto,
    ModeloServico, DialogoServico,
    ModeloFornecedor, DialogoFornecedor,
    ModeloSuprimento, DialogoSuprimento,
    ModeloMaquina, DialogoMaquina,
    ModeloVenda, DialogoVenda, DialogoEditarVenda,
    ModeloDespesa, DialogoDespesa
)

class SidebarButton(QPushButton):
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"{icon_text}  {text}")
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #333333;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QPushButton:checked {
                background-color: #8A2BE2;
                color: white;
            }
        """)
        self.setCheckable(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão - Clínica de Estética")
        self.setGeometry(100, 100, 1200, 800)

        # Banco
        database.criar_banco()

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.white)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.black)
        palette.setColor(QPalette.ColorRole.Base, Qt.white)
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.black)
        palette.setColor(QPalette.ColorRole.Button, Qt.white)
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.black)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 122, 204))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.white)
        self.setPalette(palette)

        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.create_sidebar(main_layout)

        # Conteúdo principal
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Carregar páginas reais do sistema
        self.load_real_pages()

    def create_sidebar(self, parent_layout):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #E0E0E0;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(8)

        title_label = QLabel("Clínica de Estética")
        title_label.setStyleSheet("""
            QLabel {
                color: #8A2BE2;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 24px;
            }
        """)
        sidebar_layout.addWidget(title_label)

        self.page_titles = [
           "Agenda", "Clientes", "Vendas", "Despesas", "Produtos",
            "Serviços", "Suprimentos", "Fornecedores", "Máquinas", "Funcionários"
        ]

        icons = ["📅", "👥", "💰", "💸", "🛍️", "🔧", "📦", "🏭", "⚙️", "👨‍💼"]

        self.nav_buttons = []
        for icon, name in zip(icons, self.page_titles):
            btn = SidebarButton(name, icon)
            btn.clicked.connect(partial(self.switch_page, len(self.nav_buttons)))
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        self.nav_buttons[0].setChecked(True)
        sidebar_layout.addStretch()
        parent_layout.addWidget(sidebar)

    def load_real_pages(self):
        widgets = [
            WidgetAgenda(),
            WidgetGerenciamento("Cliente", ModeloCliente(), DialogoCliente),
            WidgetGerenciamento("Venda", ModeloVenda(), DialogoVenda, DialogoEditarVenda),
            WidgetGerenciamento("Despesa", ModeloDespesa(), DialogoDespesa),
            WidgetGerenciamento("Produto", ModeloProduto(), DialogoProduto),
            WidgetGerenciamento("Serviço", ModeloServico(), DialogoServico),
            WidgetGerenciamento("Suprimento", ModeloSuprimento(), DialogoSuprimento),
            WidgetGerenciamento("Fornecedor", ModeloFornecedor(), DialogoFornecedor),
            WidgetGerenciamento("Máquina", ModeloMaquina(), DialogoMaquina),
            WidgetGerenciamento("Funcionário", ModeloFuncionario(), DialogoFuncionario)
        ]
        for widget in widgets:
            self.stacked_widget.addWidget(widget)

    def switch_page(self, index):
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[index].setChecked(True)
        self.stacked_widget.setCurrentIndex(index)


def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
