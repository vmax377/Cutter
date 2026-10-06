"""Diàleg compacte i modern per afegir una peça solta."""
import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dades.perfils import obtenir_gruix_perfil
from logica.funcions import convertir_numero
from logica.gestor_dades import afegir_tall


class FinestraPecaSolta(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Afegir peça solta")
        self.setMinimumSize(570, 560)
        self.resize(620, 610)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { background: #f4f7fb; color: #172033; font-family: 'Segoe UI'; font-size: 9pt; }
            QFrame#card { background: white; border: 1px solid #e1e7ef; border-radius: 10px; }
            QLabel { color: #475569; font-weight: 600; }
            QLineEdit, QComboBox {
                background: #fff; color: #172033; border: 1px solid #d5deea;
                border-radius: 6px; padding: 6px 8px; min-height: 24px;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #2563eb; }
            QPushButton { border: none; border-radius: 7px; padding: 9px 14px; font-weight: 700; min-height: 20px; }
            QPushButton#primary { background: #2563eb; color: white; }
            QPushButton#primary:hover { background: #1d4ed8; }
            QPushButton#secondary { background: #e2e8f0; color: #334155; }
            QPushButton#secondary:hover { background: #cbd5e1; }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 14)
        root.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("Peça solta")
        title.setStyleSheet("font-size: 14pt; font-weight: 700; color: #172033;")
        header.addWidget(title)
        header.addStretch()
        hint = QLabel("Introducció manual")
        hint.setStyleSheet("font-size: 8pt; color: #64748b; font-weight: 400;")
        header.addWidget(hint)
        root.addLayout(header)

        card = QFrame()
        card.setObjectName("card")
        grid = QGridLayout(card)
        grid.setContentsMargins(14, 13, 14, 13)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)
        root.addWidget(card, 1)

        self.txt_client = QLineEdit()
        self.txt_client.setPlaceholderText("Nom del client")
        self.txt_codi_feina = QLineEdit()
        self.txt_codi_feina.setPlaceholderText("Codi de feina")

        self.cbo_tipus_peca = QComboBox()
        self.cbo_tipus_peca.addItems([
            "MarcBA", "MarcAL", "FullaBA", "FullaAL", "Inversor",
            "Creuament", "CreuamentPVC", "RivetBA", "RivetAL", "Goteron"
        ])
        self.cbo_perfil = QComboBox()
        self.cbo_perfil.addItems([
            "RT650", "RT851", "RT860", "RT660", "RT665+", "RT865", "RT866",
            "RT877", "RT862", "RT890", "RT879", "RT896", "RT899", "RT651",
            "RT652", "RT653", "RT654", "RT658", "RT659", "RT661", "RT663",
            "RT667", "RT668", "RT861", "RT881", "74663"
        ])

        self.txt_mida = QLineEdit()
        self.txt_mida.setPlaceholderText("mm")
        self.txt_gruix = QLineEdit()  # Editable; el perfil només proposa un valor inicial
        self.txt_color = QLineEdit()
        self.txt_color.setPlaceholderText("Color / acabat")
        self.txt_angle_esq = QLineEdit("45")
        self.txt_angle_dret = QLineEdit("45")
        self.txt_quantitat = QLineEdit("1")

        def add_field(row, col, label, widget, span=1):
            cell = QWidget()
            box = QVBoxLayout(cell)
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(3)
            box.addWidget(QLabel(label))
            box.addWidget(widget)
            grid.addWidget(cell, row, col, 1, span)

        add_field(0, 0, "CLIENT", self.txt_client)
        add_field(0, 1, "CODI DE FEINA", self.txt_codi_feina)
        add_field(1, 0, "TIPUS DE PEÇA", self.cbo_tipus_peca)
        add_field(1, 1, "PERFIL", self.cbo_perfil)
        add_field(2, 0, "MIDA (mm)", self.txt_mida)
        add_field(2, 1, "GRUIX (mm) · EDITABLE", self.txt_gruix)
        add_field(3, 0, "ANGLE ESQUERRE (°)", self.txt_angle_esq)
        add_field(3, 1, "ANGLE DRET (°)", self.txt_angle_dret)
        add_field(4, 0, "QUANTITAT", self.txt_quantitat)
        add_field(4, 1, "COLOR / ACABAT", self.txt_color)

        buttons = QHBoxLayout()
        buttons.addStretch()
        self.btn_cancel = QPushButton("Cancel·lar")
        self.btn_cancel.setObjectName("secondary")
        self.btn_afegir = QPushButton("Afegir peça")
        self.btn_afegir.setObjectName("primary")
        self.btn_cancel.clicked.connect(self.close)
        self.btn_afegir.clicked.connect(self.on_afegir)
        buttons.addWidget(self.btn_cancel)
        buttons.addWidget(self.btn_afegir)
        root.addLayout(buttons)

        self.cbo_tipus_peca.currentIndexChanged.connect(self.on_tipus_canviat)
        self.cbo_perfil.currentIndexChanged.connect(self.on_perfil_canviat)

        if self.parent_window:
            for field_name, source_name in ((self.txt_client, "txt_client"),
                                            (self.txt_codi_feina, "txt_codi_feina"),
                                            (self.txt_color, "txt_color")):
                source = getattr(self.parent_window, source_name, None)
                if source is not None:
                    field_name.setText(source.text())
        self.on_tipus_canviat()
        self.on_perfil_canviat()

    def on_tipus_canviat(self):
        angle = "90" if self.cbo_tipus_peca.currentText() == "Goteron" else "45"
        self.txt_angle_esq.setText(angle)
        self.txt_angle_dret.setText(angle)

    def on_perfil_canviat(self):
        """Proposa el gruix del perfil, però permet corregir-lo manualment després."""
        perfil = self.cbo_perfil.currentText()
        gruix = obtenir_gruix_perfil(perfil)
        self.txt_gruix.setText(str(gruix))

    def on_afegir(self):
        client = self.txt_client.text().strip().upper()
        if not client:
            QMessageBox.warning(self, "Falta client", "El camp client és obligatori.")
            self.txt_client.setFocus()
            return

        codi_feina = self.txt_codi_feina.text().strip().upper()
        if not codi_feina:
            QMessageBox.warning(self, "Falta codi", "El codi de feina és obligatori.")
            self.txt_codi_feina.setFocus()
            return

        mida = convertir_numero(self.txt_mida.text())
        if mida <= 0:
            QMessageBox.warning(self, "Mida incorrecta", "Introdueix una mida vàlida.")
            self.txt_mida.setFocus()
            return

        quantitat_num = convertir_numero(self.txt_quantitat.text())
        quantitat = int(quantitat_num) if quantitat_num > 0 else 1
        gruix = convertir_numero(self.txt_gruix.text())
        if gruix <= 0:
            QMessageBox.warning(self, "Gruix incorrecte", "Introdueix un gruix superior a zero.")
            self.txt_gruix.setFocus()
            return

        tipus_peca = self.cbo_tipus_peca.currentText()
        perfil = self.cbo_perfil.currentText()
        angle_esq = convertir_numero(self.txt_angle_esq.text())
        angle_dret = convertir_numero(self.txt_angle_dret.text())
        color = self.txt_color.text().strip().upper() or "-"

        try:
            afegir_tall(
                mida=mida,
                angle_esq=angle_esq if angle_esq else 45,
                angle_dret=angle_dret if angle_dret else 45,
                quantitat=quantitat,
                perfil=perfil,
                client=client,
                gruix=gruix,
                descripcio=tipus_peca,
                tipus_obertura="Peça solta",
                color=color,
                codi_feina=codi_feina,
            )
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No s'ha pogut afegir la peça:\n\n{exc}")
            return

        if self.parent_window:
            self.parent_window.refrescar_llista()
        self.txt_mida.clear()
        self.txt_quantitat.setText("1")
        self.txt_mida.setFocus()
        QMessageBox.information(self, "Fet", "Peça afegida correctament.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = FinestraPecaSolta()
    dialog.show()
    sys.exit(app.exec_())
