"""
Funcions d'impressió: ordre de feina i etiquetes.
"""

from datetime import datetime
import os

from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter, QFont, QPdfWriter, QPageSize, QPen, QColor
from PyQt5.QtCore import QSizeF, QMarginsF


# ============================================================
#  ORDRE DE FEINA
# ============================================================

def imprimir_ordre_feina(talls, parent=None):
    """Imprimeix l'ordre de feina."""
    printer = QPrinter(QPrinter.ScreenResolution)
    dialog = QPrintDialog(printer, parent)
    if dialog.exec_() != QPrintDialog.Accepted:
        return
    painter = QPainter(printer)
    try:
        _dibuixar_ordre(painter, printer, talls)
    finally:
        painter.end()


def _dibuixar_ordre(painter, printer, talls):
    """Dibuixa l'ordre de feina amb taula, dibuix i tot."""
    from logica.esquema import dibuixar_esquema

    # ---- COLOR NEGRE ----
    pen = QPen(QColor(0, 0, 0))
    pen.setWidth(1)
    painter.setPen(pen)

    page_rect = printer.pageRect(QPrinter.DevicePixel)
    page_alt = page_rect.height()
    page_ample = page_rect.width()

    margin_x = 40
    margin_y = 40
    x = margin_x
    y = margin_y

    # ---- Capçalera ----
    painter.setFont(QFont("Arial", 14, QFont.Bold))
    painter.drawText(x, y, "Tanqui-Tanqui, s.l.")
    y += 30

    painter.setFont(QFont("Arial", 16, QFont.Bold))
    painter.drawText(x, y, "ORDRE DE FEINA")
    y += 35

    painter.setFont(QFont("Arial", 10))
    painter.drawText(x, y, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y += 30

    # ---- Agrupar per CODI FEINA ----
    grups = {}
    ordre_codis = []
    for t in talls:
        codi = t.get('codi_feina') or "(SENSE CODI)"
        if codi not in grups:
            grups[codi] = []
            ordre_codis.append(codi)
        grups[codi].append(t)

    # ---- Columnes ----
    pesos = [
        ("Client", 8), ("Mida", 8), ("Perfil", 10), ("Descripció", 14),
        ("Qu.", 5), ("AE", 5), ("AD", 5), ("Gr.", 7),
        ("Tipus Obertura", 20), ("Color", 7), ("Codi", 7), ("OK", 4),
    ]
    total_pes = sum(p[1] for p in pesos)
    ample_disponible = page_ample - (2 * margin_x)

    columnes = []
    for nom, pes in pesos:
        columnes.append((nom, int((pes / total_pes) * ample_disponible)))
    total_amplada = sum(c[1] for c in columnes)

    # ---- Iterar grups ----
    for codi in ordre_codis:
        files = grups[codi]

        if y + 350 > page_alt - margin_y:
            printer.newPage()
            y = margin_y

        # ---- Capçalera de grup ----
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(x, y, f"CODI FEINA: {codi}")
        y += 20

        # ---- Capçalera de taula ----
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        fm = painter.fontMetrics()
        altura_fila = fm.height() + 6

        x_col = x
        for nom, amplada in columnes:
            painter.drawRect(x_col, y, amplada, altura_fila)
            painter.drawText(x_col + 2, y + fm.height() - 2, nom)
            x_col += amplada
        y += altura_fila

        # ---- Files de la taula ----
        painter.setFont(QFont("Arial", 8))
        fm = painter.fontMetrics()
        altura_fila = fm.height() + 6

        for t in files:
            if y + altura_fila > page_alt - margin_y:
                printer.newPage()
                y = margin_y
                painter.setFont(QFont("Arial", 8))

            mida = t.get('mida') or 0
            ae = t.get('angle_esq') or 0
            ad = t.get('angle_dret') or 0
            qt = t.get('quantitat') or 0
            perfil = t.get('perfil') or ""
            client = t.get('client') or ""
            gruix = t.get('gruix') or 0
            desc = t.get('descripcio') or ""
            tipus_op = t.get('tipus_obertura') or ""
            color = t.get('color') or ""
            cf = t.get('codi_feina') or ""

            if client and desc.startswith(client[:3] + "-"):
                desc = desc[len(client[:3]) + 1:]

            valors = [client, f"{mida:.0f}", perfil, desc, f"{qt}",
                      f"{ae:.0f}", f"{ad:.0f}", f"{gruix:.1f}",
                      tipus_op, color, cf, ""]

            x_col = x
            for i, (nom, amplada) in enumerate(columnes):
                painter.drawRect(x_col, y, amplada, altura_fila)
                painter.drawText(x_col + 2, y + fm.height() - 2, valors[i])
                x_col += amplada
            y += altura_fila

        # ============================================================
        # DIBUIX DE L'ESQUEMA
        # ============================================================
        amp_marc = 0
        alt_marc = 0
        amp_fulla = 0
        alt_fulla = 0
        tipus_dibuix = ""

        for t in files:
            desc_u = (t.get('descripcio') or "").upper()
            mida_t = t.get('mida') or 0

            if amp_marc == 0 and "MARCBA" in desc_u:
                amp_marc = mida_t
            if alt_marc == 0 and "MARCAL" in desc_u:
                alt_marc = mida_t
            if amp_fulla == 0 and "FULLABA" in desc_u:
                amp_fulla = mida_t
            if alt_fulla == 0 and "FULLAAL" in desc_u:
                alt_fulla = mida_t
            if tipus_dibuix == "" and t.get('tipus_obertura'):
                tipus_dibuix = t.get('tipus_obertura')

        if amp_marc > 0 and alt_marc > 0:
            if y + 320 > page_alt - margin_y:
                printer.newPage()
                y = margin_y

            centre_x = (page_ample - 250) / 2
            if centre_x < x:
                centre_x = x

            dibuixar_esquema(
                painter, centre_x, y + 40,
                amp_marc, alt_marc,
                amp_fulla, alt_fulla,
                tipus_dibuix
            )
            y += 320

        y += 30


# ============================================================
#  ETIQUETES - GENERAR PDF DIRECTE
# ============================================================

def imprimir_etiquetes(talls, parent=None):
    """Genera un PDF amb etiquetes de 65×40 mm (una per pàgina)."""
    from PyQt5.QtWidgets import QFileDialog, QMessageBox

    if not talls:
        return

    carpeta = r"C:\MacrosTall"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    nom_defecte = os.path.join(
        carpeta,
        f"Etiquetes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    ruta, _ = QFileDialog.getSaveFileName(
        parent, "Guardar PDF d'etiquetes",
        nom_defecte,
        "PDF (*.pdf)"
    )
    if not ruta:
        return

    writer = QPdfWriter(ruta)
    writer.setPageSize(QPageSize(QSizeF(65, 40), QPageSize.Millimeter))
    writer.setResolution(300)
    writer.setPageMargins(QMarginsF(0, 0, 0, 0))

    painter = QPainter(writer)
    try:
        _dibuixar_etiquetes_directe(painter, writer, talls)
    finally:
        painter.end()

    QMessageBox.information(
        parent, "PDF creat",
        f"S'ha creat el PDF:\n\n{ruta}"
    )


def _dibuixar_etiquetes_directe(painter, writer, talls):
    """Dibuixa una etiqueta per pàgina (65×40 mm). SENSE requadre."""

    painter.setPen(QPen(QColor(0, 0, 0)))

    page_rect = writer.pageLayout().paintRectPixels(writer.resolution())
    page_ample = page_rect.width()
    page_alt = page_rect.height()

    # Expandir la llista segons quantitat
    etiquetes = []
    for t in talls:
        quantitat = int(t.get('quantitat') or 1)
        for _ in range(quantitat):
            etiquetes.append(t)

    for i, t in enumerate(etiquetes):
        if i > 0:
            writer.newPage()

        client = t.get('client') or ""
        desc = t.get('descripcio') or ""
        mida = t.get('mida') or 0
        color = t.get('color') or ""
        codi_feina = t.get('codi_feina') or ""

        if client and desc.startswith(client[:3] + "-"):
            desc = desc[len(client[:3]) + 1:]

        # ---- TEXT ----
        tx = 25
        ty = 50

        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(tx, ty, f"Client: {client}")
        ty += 40

        painter.setFont(QFont("Arial", 10))
        painter.drawText(tx, ty, f"Tipus: {desc}")
        ty += 35

        painter.drawText(tx, ty, f"Mida: {mida:.0f} mm")
        ty += 35

        painter.drawText(tx, ty, f"Color: {color}")
        ty += 40

        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(tx, ty, f"Codi: {codi_feina}")