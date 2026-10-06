"""
Finestra principal del programa Cutter - Versió moderna.
"""

import sys
import os
import re
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox,
    QListWidget, QMessageBox, QInputDialog, QFrame, QGridLayout,
    QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dades.perfils import obtenir_gruix_perfil
from logica.calculs import calcular_talls
from logica.gestor_dades import (
    afegir_tall, afegir_talls, llegir_talls, esborrar_talls,
    ordenar_per_tipus, ordenar_per_mida_desc, ordenar_per_codi_feina,
    importar_d2k
)
from logica.funcions import convertir_numero
from logica.impressio import (
    imprimir_ordre_feina, imprimir_etiquetes, _dibuixar_etiquetes_directe
)
from ui.finestra_peca_solta import FinestraPecaSolta


CARPETA_D2K = r"C:\MacrosTall"


def aplicar_tema_modern(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 247, 250))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)


class FinestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cutter V3.1")
        self.resize(1400, 900)

        central = QWidget()
        central.setObjectName("fons")
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(15, 15, 15, 15)
        layout_principal.setSpacing(12)

        # ============================================================
        # CAPÇALERA
        # ============================================================
        capcalera = QFrame()
        capcalera.setFixedHeight(70)
        capcalera.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
            }
        """)
        lc = QHBoxLayout(capcalera)
        lc.setContentsMargins(-5, 6, 20, 6)
        lc.setSpacing(12)

        # ---- LOGO (imatge) ----
        logo_label = QLabel()
        # Buscar el logo tant si és EXE com si és codi font
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_path, "logo.png")

        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(
                50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(logo_pixmap)
        logo_label.setStyleSheet("background: transparent;")
        lc.addWidget(logo_label)

        # ---- TEXT ----
        t = QLabel("Gestió de Talls")
        t.setStyleSheet(
            "color: white; font-size: 17pt; font-weight: bold; background: transparent;"
        )
        lc.addWidget(t)

        lc.addStretch()

        s = QLabel("Tanqui-Tanqui, s.l.")
        s.setStyleSheet(
            "color: #95a5a6; font-size: 10pt; background: transparent;"
        )
        lc.addWidget(s)

        layout_principal.addWidget(capcalera)

        # ---- Panells ----
        layout_panells = QHBoxLayout()
        layout_panells.setSpacing(15)
        layout_panells.addWidget(self.crear_panell_esquerra(), 1)
        layout_panells.addWidget(self.crear_panell_dreta(), 1)
        layout_principal.addLayout(layout_panells)

        # ---- Connexions ----
        self.cbo_batents.currentIndexChanged.connect(self.on_batents_canviat)
        self.cbo_perfil_marc.currentIndexChanged.connect(self.on_perfil_marc_canviat)
        self.cbo_perfil_fulla.currentIndexChanged.connect(self.on_perfil_fulla_canviat)
        self.btn_afegir_talls.clicked.connect(self.on_afegir_talls)
        self.btn_esborrar_llista.clicked.connect(self.on_esborrar_llista)
        self.btn_peca_solta.clicked.connect(self.on_peca_solta)
        self.btn_enviar_d2k.clicked.connect(self.on_enviar_d2k)
        self.btn_importar_d2k.clicked.connect(self.on_importar_d2k)
        self.btn_imprimir_ordre.clicked.connect(self.on_imprimir_ordre)
        self.btn_imprimir_etiquetes.clicked.connect(self.on_imprimir_etiquetes)
        self.btn_tancar.clicked.connect(self.on_tancar)
        self.btn_comanda_vidre.clicked.connect(self.on_comanda_vidre)
        self.chk_ordenar.stateChanged.connect(self.on_ordenar_canviat)
        self.chk_ordenar_client.stateChanged.connect(self.on_ordenar_canviat)

        try:
            esborrar_talls()
        except Exception:
            pass

        self.refrescar_llista()

    # ------------------------------------------------------------
    def etiqueta(self, text):
        l = QLabel(text)
        l.setStyleSheet(
            "font-size: 8pt; font-weight: bold; color: #0f172a; padding: 2px 0;"
        )
        return l

    def input(self, placeholder=""):
        i = QLineEdit()
        if placeholder:
            i.setPlaceholderText(placeholder)
        i.setMinimumHeight(32)
        i.setStyleSheet("""
            QLineEdit {
                background: white; border: 1px solid #dfe6e9;
                border-radius: 6px; padding: 4px 10px;
                font-size: 10pt; color: #2c3e50;
            }
            QLineEdit:focus { border: 2px solid #3498db; }
        """)
        return i

    def combo(self):
        c = QComboBox()
        c.setMinimumHeight(32)
        c.setStyleSheet("""
            QComboBox {
                background: white; border: 1px solid #dfe6e9;
                border-radius: 6px; padding: 4px 10px;
                font-size: 10pt; color: #2c3e50;
            }
            QComboBox:focus { border: 2px solid #3498db; }
        """)
        return c

    def boto(self, text, color, hover, altura=42):
        b = QPushButton(text)
        b.setMinimumHeight(altura)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}; color: white;
                border: none; border-radius: 8px;
                padding: 8px; font-weight: bold;
                font-size: 10pt;
            }}
            QPushButton:hover {{ background-color: {hover}; }}
        """)
        return b

    # ------------------------------------------------------------
    def crear_panell_esquerra(self):
        panell = QFrame()
        panell.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                border: 1px solid #dfe6e9;
            }
        """)

        layout = QVBoxLayout(panell)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(12)

        titol = QLabel("📐  DADES DEL TALL")
        titol.setStyleSheet("""
            font-size: 12pt; font-weight: bold; color: #2c3e50;
            padding-bottom: 6px; border-bottom: 2px solid #3498db;
        """)
        layout.addWidget(titol)

        # CLIENT + CODI FEINA + CODI BARRES
        self.txt_client = self.input("Client")
        self.txt_codi_feina = self.input("Ex: F1")
        self.txt_codi_barres = self.input("Ex: 12345678901")

        fila = QHBoxLayout()
        fila.setSpacing(10)
        c1 = QVBoxLayout(); c1.setSpacing(3)
        c1.addWidget(self.etiqueta("CLIENT"))
        c1.addWidget(self.txt_client)
        fila.addLayout(c1, 3)
        c2 = QVBoxLayout(); c2.setSpacing(3)
        c2.addWidget(self.etiqueta("CODI FEINA"))
        c2.addWidget(self.txt_codi_feina)
        fila.addLayout(c2, 2)
        c3 = QVBoxLayout(); c3.setSpacing(3)
        c3.addWidget(self.etiqueta("CODI BARRES"))
        c3.addWidget(self.txt_codi_barres)
        fila.addLayout(c3, 2)
        layout.addLayout(fila)

        # TIPUS D'OBERTURA
        layout.addWidget(self.etiqueta("TIPUS D'OBERTURA"))
        self.cbo_batents = self.combo()
        self.cbo_batents.addItems([
            "", "0 - MARC (Només Marc)", "1 - FINESTRA 1 F",
            "2 - FINESTRA PRACT. 2 F", "3 - CORR. PROS 70 2 F",
            "4 - CORR. PROS 70 2 F PAN", "5 - CORR. PROS 85 2 F",
            "6 - CORR. PROS 85 2 F PAN", "7 - CORR. PROS 85 2 F EMP.",
            "8 - CORR. PROS 85 2 F EMP.PAN"
        ])
        layout.addWidget(self.cbo_batents)

        # MARC + FULLA (4 columnes)
        self.cbo_perfil_marc = self.combo()
        self.txt_gruix_marc = self.input()
        self.cbo_perfil_fulla = self.combo()
        self.txt_gruix_fulla = self.input()

        fila = QHBoxLayout()
        fila.setSpacing(10)
        c1 = QVBoxLayout(); c1.setSpacing(3)
        c1.addWidget(self.etiqueta("PERFIL MARC"))
        c1.addWidget(self.cbo_perfil_marc)
        fila.addLayout(c1, 3)
        c2 = QVBoxLayout(); c2.setSpacing(3)
        c2.addWidget(self.etiqueta("GRUIX M"))
        c2.addWidget(self.txt_gruix_marc)
        fila.addLayout(c2, 1)
        c3 = QVBoxLayout(); c3.setSpacing(3)
        c3.addWidget(self.etiqueta("PERFIL FULLA"))
        c3.addWidget(self.cbo_perfil_fulla)
        fila.addLayout(c3, 3)
        c4 = QVBoxLayout(); c4.setSpacing(3)
        c4.addWidget(self.etiqueta("GRUIX F"))
        c4.addWidget(self.txt_gruix_fulla)
        fila.addLayout(c4, 1)
        layout.addLayout(fila)

        # ALÇADA + AMPLADA + QUANTITAT + COLOR
        self.txt_alcada = self.input()
        self.txt_amplada = self.input()
        self.txt_quantitat = self.input()
        self.txt_quantitat.setText("1")
        self.txt_color = self.input()

        fila = QHBoxLayout()
        fila.setSpacing(10)
        c1 = QVBoxLayout(); c1.setSpacing(3)
        c1.addWidget(self.etiqueta("ALÇADA (mm)"))
        c1.addWidget(self.txt_alcada)
        fila.addLayout(c1)
        c2 = QVBoxLayout(); c2.setSpacing(3)
        c2.addWidget(self.etiqueta("AMPLADA (mm)"))
        c2.addWidget(self.txt_amplada)
        fila.addLayout(c2)
        c3 = QVBoxLayout(); c3.setSpacing(3)
        c3.addWidget(self.etiqueta("QUANTITAT"))
        c3.addWidget(self.txt_quantitat)
        fila.addLayout(c3)
        c4 = QVBoxLayout(); c4.setSpacing(3)
        c4.addWidget(self.etiqueta("COLOR"))
        c4.addWidget(self.txt_color)
        fila.addLayout(c4)
        layout.addLayout(fila)

        # ANGLES + JUNQUILLO + FARCIMENT
        self.txt_angle_esq = self.input()
        self.txt_angle_esq.setText("45")
        self.txt_angle_dret = self.input()
        self.txt_angle_dret.setText("45")
        self.cbo_tipus_junquillo = self.combo()
        self.cbo_tipus_junquillo.addItems(["", "Tancat (vidre fix)", "Obert (amb rivets)"])
        self.cbo_farciment = self.combo()
        self.cbo_farciment.addItems(["", "VIDRE", "PANELL", "SENSE FARCIMENT"])

        fila = QHBoxLayout()
        fila.setSpacing(10)
        c1 = QVBoxLayout(); c1.setSpacing(3)
        c1.addWidget(self.etiqueta("ANGLE ESQ"))
        c1.addWidget(self.txt_angle_esq)
        fila.addLayout(c1)
        c2 = QVBoxLayout(); c2.setSpacing(3)
        c2.addWidget(self.etiqueta("ANGLE DRET"))
        c2.addWidget(self.txt_angle_dret)
        fila.addLayout(c2)
        c3 = QVBoxLayout(); c3.setSpacing(3)
        c3.addWidget(self.etiqueta("RIVETS"))
        c3.addWidget(self.cbo_tipus_junquillo)
        fila.addLayout(c3, 2)
        c4 = QVBoxLayout(); c4.setSpacing(3)
        c4.addWidget(self.etiqueta("FARCIMENT"))
        c4.addWidget(self.cbo_farciment)
        fila.addLayout(c4, 2)
        layout.addLayout(fila)

        # CHECKBOXES
        chk_css = """
            QCheckBox { font-size: 9pt; color: #0f172a; spacing: 6px; padding: 2px; font-weight: 600; }
            QCheckBox::indicator { width: 15px; height: 15px; border-radius: 3px; border: 2px solid #94a3b8; background: white; }
            QCheckBox::indicator:checked { background-color: #3498db; border: 2px solid #3498db; }
        """
        fila = QHBoxLayout(); fila.setSpacing(15)
        self.chk_tallar_rivets = QCheckBox("Tallar Rivets")
        self.chk_tallar_rivets.setStyleSheet(chk_css)
        fila.addWidget(self.chk_tallar_rivets)
        self.chk_afegir_gotero = QCheckBox("Afegir Goteró")
        self.chk_afegir_gotero.setStyleSheet(chk_css)
        fila.addWidget(self.chk_afegir_gotero)
        fila.addStretch()
        layout.addLayout(fila)

        fila = QHBoxLayout(); fila.setSpacing(15)
        self.chk_ordenar = QCheckBox("Ordre Major → menor")
        self.chk_ordenar.setStyleSheet(chk_css)
        fila.addWidget(self.chk_ordenar)
        self.chk_ordenar_client = QCheckBox("Ordena per Codi Feina")
        self.chk_ordenar_client.setStyleSheet(chk_css)
        fila.addWidget(self.chk_ordenar_client)
        fila.addStretch()
        layout.addLayout(fila)

        # INFO VIDRE
        self.lbl_vidre_info = QLabel("")
        self.lbl_vidre_info.setStyleSheet("""
            color: #2980b9; font-weight: bold; font-size: 10pt;
            padding: 7px 10px; background: #eaf4fd;
            border-radius: 6px; border-left: 4px solid #3498db;
        """)
        self.lbl_vidre_info.setMinimumHeight(32)
        layout.addWidget(self.lbl_vidre_info)

        # BOTONS
        self.btn_afegir_talls = self.boto("➕  AFEGIR TALLS", "#27ae60", "#229954", altura=52)
        layout.addWidget(self.btn_afegir_talls)

        fila = QHBoxLayout()
        fila.setSpacing(8)
        self.btn_peca_solta = self.boto("🔧 PEÇA SOLTA", "#3498db", "#2980b9")
        fila.addWidget(self.btn_peca_solta)
        self.btn_comanda_vidre = self.boto("📧 COMANDA VIDRE", "#e67e22", "#d35400")
        fila.addWidget(self.btn_comanda_vidre)
        self.btn_imprimir_etiquetes = self.boto("🏷️ ETIQUETES", "#16a085", "#138d75")
        fila.addWidget(self.btn_imprimir_etiquetes)
        layout.addLayout(fila)

        fila = QHBoxLayout()
        fila.setSpacing(8)
        self.btn_imprimir_ordre = self.boto("🖨️ ORDRE FEINA", "#16a085", "#138d75")
        fila.addWidget(self.btn_imprimir_ordre)
        self.btn_enviar_d2k = self.boto("📤 ENVIAR D2K", "#9b59b6", "#8e44ad")
        fila.addWidget(self.btn_enviar_d2k)
        self.btn_importar_d2k = self.boto("📥 IMPORTAR D2K", "#0891b2", "#0e7490")
        fila.addWidget(self.btn_importar_d2k)
        layout.addLayout(fila)

        fila = QHBoxLayout()
        fila.setSpacing(8)
        self.btn_esborrar_llista = self.boto("🗑️ ESBORRAR LLISTA", "#e74c3c", "#c0392b")
        fila.addWidget(self.btn_esborrar_llista)
        self.btn_tancar = self.boto("❌ TANCAR", "#95a5a6", "#7f8c8d")
        fila.addWidget(self.btn_tancar)
        layout.addLayout(fila)

        return panell

    def crear_panell_dreta(self):
        panell = QFrame()
        panell.setStyleSheet("""
            QFrame {
                background: white; border-radius: 10px;
                border: 1px solid #dfe6e9;
            }
        """)

        layout = QVBoxLayout(panell)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(10)

        lbl_titol = QLabel("📋  LLISTA DE TALLS")
        lbl_titol.setStyleSheet("""
            font-size: 12pt; font-weight: bold; color: #2c3e50;
            padding-bottom: 6px; border-bottom: 2px solid #3498db;
        """)
        layout.addWidget(lbl_titol)

        self.lst_talls = QListWidget()
        self.lst_talls.setFont(QFont("Consolas", 9))
        self.lst_talls.setAlternatingRowColors(True)
        self.lst_talls.setStyleSheet("""
            QListWidget {
                background: #fafbfc; border: 1px solid #dfe6e9;
                border-radius: 6px; padding: 4px;
                font-family: Consolas, "Courier New", monospace;
                font-size: 9pt;
            }
            QListWidget::item {
                padding: 6px 8px; border-bottom: 1px solid #f0f2f5;
                color: #2c3e50;
            }
            QListWidget::item:alternate { background: #f8f9fa; }
            QListWidget::item:hover { background: #eaf4fd; }
            QListWidget::item:selected { background: #3498db; color: white; }
        """)
        layout.addWidget(self.lst_talls)

        return panell

    # ============================================================
    #  LÒGICA
    # ============================================================
    def carregar_marcs_compatibles(self):
        self.cbo_perfil_marc.blockSignals(True)
        self.cbo_perfil_marc.clear()
        if self.cbo_batents.currentIndex() <= 0:
            self.cbo_perfil_marc.blockSignals(False)
            return
        b = int(self.cbo_batents.currentText()[0])
        if b == 0:
            marcs = ["RT650", "RT851", "RT860", "RT660", "RT665+", "RT865", "RT890", "RT896", "RT899"]
        elif b in (1, 2):
            marcs = ["RT650", "RT851", "RT860", "RT660", "RT665+"]
        elif b in (3, 4):
            marcs = ["RT865"]
        elif b in (5, 6):
            marcs = ["RT890", "RT895"]
        elif b in (7, 8):
            marcs = ["RT896", "RT899"]
        else:
            marcs = []
        self.cbo_perfil_marc.addItems(marcs)
        if marcs:
            self.cbo_perfil_marc.setCurrentIndex(0)
        self.cbo_perfil_marc.blockSignals(False)
        self.on_perfil_marc_canviat()

    def carregar_fulles_compatibles(self):
        self.cbo_perfil_fulla.blockSignals(True)
        self.cbo_perfil_fulla.clear()
        if self.cbo_batents.currentIndex() <= 0:
            self.cbo_perfil_fulla.blockSignals(False)
            return
        if self.cbo_perfil_marc.currentIndex() < 0:
            self.cbo_perfil_fulla.blockSignals(False)
            return
        b = int(self.cbo_batents.currentText()[0])
        m = self.cbo_perfil_marc.currentText()
        fulles = []
        if m in ("RT650", "RT851", "RT860", "RT660", "RT665+"):
            if b in (1, 2):
                fulles = ["RT651", "RT661", "RT667", "RT652", "RT662", "RT659", "RT666"]
        elif m == "RT865":
            if b in (3, 4):
                fulles = ["RT861"]
        elif m in ("RT890", "RT895"):
            if b in (5, 6):
                fulles = ["RT881"]
        elif m in ("RT896", "RT899"):
            if b in (7, 8):
                fulles = ["RT881"]
        self.cbo_perfil_fulla.addItems(fulles)
        if fulles:
            self.cbo_perfil_fulla.setCurrentIndex(0)
        self.cbo_perfil_fulla.blockSignals(False)
        self.on_perfil_fulla_canviat()

    def on_batents_canviat(self):
        self.txt_gruix_marc.clear()
        self.txt_gruix_fulla.clear()
        self.carregar_marcs_compatibles()

    def on_perfil_marc_canviat(self):
        if self.cbo_perfil_marc.currentIndex() < 0:
            return
        self.txt_gruix_marc.setText(str(obtenir_gruix_perfil(self.cbo_perfil_marc.currentText())))
        self.carregar_fulles_compatibles()

    def on_perfil_fulla_canviat(self):
        if self.cbo_perfil_fulla.currentIndex() < 0:
            return
        self.txt_gruix_fulla.setText(str(obtenir_gruix_perfil(self.cbo_perfil_fulla.currentText())))

    def on_afegir_talls(self):
        client = self.txt_client.text().strip().upper()
        if not client:
            QMessageBox.warning(self, "Falta client", "El camp CLIENT és obligatori!")
            return
        codi_feina = self.txt_codi_feina.text().strip().upper()
        if not codi_feina:
            QMessageBox.warning(self, "Falta codi", "El camp CODI FEINA és obligatori!")
            return
        try:
            for t in llegir_talls():
                if t["codi_feina"] == codi_feina:
                    QMessageBox.warning(self, "Codi duplicat", f"El codi '{codi_feina}' ja existeix!")
                    return
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        if self.cbo_batents.currentIndex() <= 0:
            QMessageBox.warning(self, "Falta obertura", "Selecciona tipus d'obertura!")
            return
        if self.cbo_perfil_marc.currentIndex() < 0:
            QMessageBox.warning(self, "Falta marc", "Selecciona perfil de marc!")
            return
        b = int(self.cbo_batents.currentText()[0])
        if b != 0 and self.cbo_perfil_fulla.currentIndex() < 0:
            QMessageBox.warning(self, "Falta fulla", "Selecciona perfil de fulla!")
            return
        amplada = convertir_numero(self.txt_amplada.text())
        if amplada <= 0:
            QMessageBox.warning(self, "Amplada", "Introdueix una amplada vàlida!")
            return
        alcada = convertir_numero(self.txt_alcada.text())
        if alcada <= 0:
            QMessageBox.warning(self, "Alçada", "Introdueix una alçada vàlida!")
            return
        perfil_fulla = self.cbo_perfil_fulla.currentText() if self.cbo_perfil_fulla.currentIndex() >= 0 else ""
        color_actual = self.txt_color.text().strip().upper() or "-"
        farciment = self.cbo_farciment.currentText() or "SENSE FARCIMENT"
        try:
            resultat = calcular_talls(
                batents=b, marc_actual=self.cbo_perfil_marc.currentText(),
                perfil_full_a=perfil_fulla,
                tipus_junquillo=self.cbo_tipus_junquillo.currentText(),
                amplada=amplada, alcada=alcada,
                quantitat=int(convertir_numero(self.txt_quantitat.text())) or 1,
                angle_esq=convertir_numero(self.txt_angle_esq.text()) or 45,
                angle_dret=convertir_numero(self.txt_angle_dret.text()) or 45,
                color_actual=color_actual, codi_feina=codi_feina,
                codi_client=client[:3], farciment=farciment,
                afegir_gotero=self.chk_afegir_gotero.isChecked()
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        try:
            afegir_talls(
                llista_talls=resultat["talls"], client=client,
                tipus_obertura=self.cbo_batents.currentText(),
                color=color_actual, codi_feina=codi_feina
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        vi = resultat["vidre"]
        if vi:
            self.lbl_vidre_info.setText(
                f"💎 {vi['tipus']}: {vi['quantitat']} unitat(s) de {vi['amplada']:.1f} x {vi['alcada']:.1f} mm"
            )
        else:
            self.lbl_vidre_info.setText("Sense farciment.")
        self.refrescar_llista()
        self.txt_amplada.clear()
        self.txt_alcada.clear()
        self.txt_client.clear()
        self.txt_codi_feina.clear()
        self.txt_gruix_marc.clear()
        self.txt_gruix_fulla.clear()
        self.txt_color.clear()
        self.cbo_batents.setCurrentIndex(0)
        self.cbo_perfil_marc.clear()
        self.cbo_perfil_fulla.clear()
        self.txt_client.setFocus()

    def refrescar_llista(self):
        try:
            talls = self._aplicar_ordenacio(llegir_talls())
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        self.lst_talls.clear()
        for t in talls:
            mida = t['mida'] or 0
            ae = t['angle_esq'] or 0
            ad = t['angle_dret'] or 0
            qt = t['quantitat'] or 0
            perfil = t['perfil'] or ""
            client = t['client'] or ""
            gruix = t['gruix'] or 0
            desc = t['descripcio'] or ""
            tipus_op = t['tipus_obertura'] or ""
            color = t['color'] or ""
            cf = t['codi_feina'] or ""
            text = (
                f"{mida:>6.0f}mm  {ae:>3.0f}°/{ad:>3.0f}°  {qt} pcs  "
                f"{perfil:<7}  {client:<5}  {gruix:>4.1f}  {desc:<10}  {tipus_op}  {color}  {cf}"
            )
            self.lst_talls.addItem(text)

    def _aplicar_ordenacio(self, talls):
        if self.chk_ordenar_client.isChecked() and self.chk_ordenar.isChecked():
            return sorted(talls, key=lambda t: (
                t.get('codi_feina') or '', self._tipus(t),
                t.get('perfil') or '', -(t.get('mida') or 0)
            ))
        elif self.chk_ordenar_client.isChecked():
            return sorted(talls, key=lambda t: (t.get('codi_feina') or ''))
        elif self.chk_ordenar.isChecked():
            return sorted(talls, key=lambda t: (
                self._tipus(t), t.get('perfil') or '', -(t.get('mida') or 0)
            ))
        return sorted(talls, key=lambda t: (t.get('ordre_original') or 0))

    def _tipus(self, t):
        d = (t.get('descripcio') or '').upper()
        if 'MARC' in d: return 0
        if 'FULLA' in d: return 1
        if 'GOTERON' in d: return 2
        if 'RIVET' in d: return 3
        if 'INVERSOR' in d or 'CREUAMENT' in d: return 4
        return 5

    def on_esborrar_llista(self):
        if QMessageBox.question(self, "Confirmar", "Esborrar tota la llista?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            esborrar_talls()
            self.lbl_vidre_info.clear()
            self.refrescar_llista()
            QMessageBox.information(self, "Fet", "Llista esborrada.")

    def on_peca_solta(self):
        FinestraPecaSolta(parent=self).exec_()

    def on_enviar_d2k(self):
        talls = llegir_talls()
        if not talls:
            QMessageBox.warning(self, "Buit", "No hi ha talls!")
            return
        if not os.path.exists(CARPETA_D2K):
            try:
                os.makedirs(CARPETA_D2K)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                return
        codi, ok = QInputDialog.getText(self, "Codi barres", "Codi inicial:",
                                        text=self.txt_codi_barres.text() or "12345678901")
        if not ok:
            return
        nom = f"ORDRE_TALL_D2K_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        ruta = os.path.join(CARPETA_D2K, nom)
        try:
            cb = float(codi)
        except Exception:
            cb = 12345678901
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                pa = ""
                ca = ""
                for t in talls:
                    p = t["perfil"] or "A"
                    c = t["color"] or "-"
                    if p != pa or c != ca:
                        g = t["gruix"] or 50
                        f.write(f"B,{p},{c},1,{g:.0f}\n")
                        pa = p
                        ca = c
                    md = int(t["mida"] * 10) if t["mida"] else 0
                    ae = int(t["angle_esq"] * 10) if t["angle_esq"] else 450
                    ad = int(t["angle_dret"] * 10) if t["angle_dret"] else 450
                    q = int(t["quantitat"]) if t["quantitat"] else 1
                    tp = t["descripcio"] or "Upright"
                    cl = t["client"] or "CLIENT"
                    cf = t["codi_feina"] or ""
                    f.write(f"P,{md},{0},{ae},{ad},{q:02d},,,{tp},,{cl} {cf},,,,{int(cb):013d}\n")
                    cb += 1
            QMessageBox.information(self, "Fet", f"Creat:\n{ruta}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_importar_d2k(self):
        talls_existents = llegir_talls()
        if talls_existents:
            resp = QMessageBox.question(
                self, "Ja hi ha dades",
                "Ja hi ha talls a la llista. Vols esborrar-los abans?",
                QMessageBox.Yes | QMessageBox.No
            )
            if resp == QMessageBox.Yes:
                esborrar_talls()
            else:
                return

        ruta, _ = QFileDialog.getOpenFileName(
            self, "Selecciona el fitxer D2K",
            "C:\\MacrosTall",
            "Fitxers D2K (*.txt)"
        )
        if not ruta:
            return

        talls = importar_d2k(ruta)
        if not talls:
            QMessageBox.warning(self, "Cap tall", "No s'han trobat talls al fitxer.")
            return

        for t in talls:
            afegir_tall(
                mida=t["mida"],
                angle_esq=t["angle_esq"],
                angle_dret=t["angle_dret"],
                quantitat=t["quantitat"],
                perfil=t["perfil"],
                client=t["client"],
                gruix=t["gruix"],
                descripcio=t["descripcio"],
                tipus_obertura=t["tipus_obertura"],
                color=t["color"],
                codi_feina=t["codi_feina"]
            )

        self.refrescar_llista()
        QMessageBox.information(
            self, "Importat",
            f"S'han importat {len(talls)} talls del fitxer."
        )

    def on_imprimir_ordre(self):
        talls = llegir_talls()
        if not talls:
            QMessageBox.warning(self, "Buit", "No hi ha talls!")
            return
        try:
            imprimir_ordre_feina(talls, self)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_imprimir_etiquetes(self):
        talls = llegir_talls()
        if not talls:
            QMessageBox.warning(self, "Buit", "No hi ha talls!")
            return

        mode = QMessageBox.question(
            self, "Mode d'impressió",
            f"Vols imprimir TOTES les etiquetes de cop?\n\n"
            f"SÍ = Imprimir tot de cop ({sum(int(t.get('quantitat') or 1) for t in talls)} etiquetes)\n"
            f"NO = Triar línia per línia\n"
            f"CANCEL·LAR = Cancel·lar la impressió",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if mode == QMessageBox.Cancel:
            return

        totes_de_cop = (mode == QMessageBox.Yes)

        printer = QPrinter(QPrinter.ScreenResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() != QPrintDialog.Accepted:
            return

        talls_a_imprimir = []
        if not totes_de_cop:
            for i, t in enumerate(talls):
                desc = t.get('descripcio') or ""
                mida = t.get('mida') or 0
                qt = t.get('quantitat') or 0
                resp = QMessageBox.question(
                    self, f"Imprimir línia {i+1} de {len(talls)}",
                    f"Vols imprimir aquesta línia?\n\n"
                    f"Tipus: {desc}\n"
                    f"Mida: {mida:.0f} mm\n"
                    f"Quantitat: {qt} pcs\n"
                    f"Color: {t.get('color') or '-'}\n"
                    f"Codi Feina: {t.get('codi_feina') or ''}",
                    QMessageBox.Yes | QMessageBox.No
                )
                if resp == QMessageBox.Yes:
                    talls_a_imprimir.append(t)
            if not talls_a_imprimir:
                QMessageBox.information(self, "Res", "No has triat cap línia.")
                return
        else:
            talls_a_imprimir = talls

        painter = QPainter(printer)
        try:
            _dibuixar_etiquetes_directe(painter, printer, talls_a_imprimir)
        finally:
            painter.end()

        total = sum(int(t.get('quantitat') or 1) for t in talls_a_imprimir)
        QMessageBox.information(self, "Fet", f"S'han imprès {total} etiquetes.")

    def on_comanda_vidre(self):
        info = self.lbl_vidre_info.text()
        if not info or "Sense" in info:
            QMessageBox.warning(self, "Sense vidre", "No hi ha vidre.")
            return
        m = re.search(r'(\d+)\s+unitat\(s\)\s+de\s+([\d.]+)\s+x\s+([\d.]+)', info)
        q, a, h = (m.group(1), m.group(2), m.group(3)) if m else ("?", "?", "?")
        cos = (
            "Benvolguts/des,\n\n"
            "Us fem una comanda de vidre:\n"
            f"Quantitat: {q} unitats\n"
            f"Mides: {a} x {h} mm\n\n"
            "Gràcies,\nTanqui-Tanqui, s.l."
        )
        try:
            import win32com.client
            o = win32com.client.Dispatch("Outlook.Application")
            mail = o.CreateItem(0)
            mail.To = "proveidor@vidre.com"
            mail.Subject = "Comanda de vidre"
            mail.Body = cos
            mail.Display()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_tancar(self):
        if QMessageBox.question(self, "Sortir", "Sortir?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.close()

    def on_ordenar_canviat(self):
        self.refrescar_llista()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    aplicar_tema_modern(app)
    finestra = FinestraPrincipal()
    finestra.showMaximized()
    finestra.raise_()
    finestra.activateWindow()
    sys.exit(app.exec_())