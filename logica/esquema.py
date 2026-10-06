"""
Dibuix d'esquemes de finestres/portes.
"""

from PyQt5.QtGui import QPen, QFont


def dibuixar_esquema(painter, x, y, amplada_marc, alcada_marc,
                     amplada_fulla, alcada_fulla, tipus_obertura):
    """Dibuixa l'esquema d'una finestra al painter."""

    if amplada_marc <= 0 or alcada_marc <= 0:
        return

    # ---- ESCALA (màxim 180x220 píxels) ----
    escala = min(180.0 / amplada_marc, 220.0 / alcada_marc)

    wM = amplada_marc * escala
    hM = alcada_marc * escala

    separacio = 22

    # ---- 1. LÍNIA DISCONTÍNUA AL VOLTANT ----
    pen_dash = QPen()
    pen_dash.setWidth(1)
    pen_dash.setStyle(2)  # DashLine
    painter.setPen(pen_dash)
    painter.drawRect(
        int(x - separacio),
        int(y - separacio),
        int(wM + 2 * separacio),
        int(hM + 2 * separacio)
    )

    # ---- 2. MARC EXTERIOR ----
    pen_gruix = QPen()
    pen_gruix.setWidth(2)
    painter.setPen(pen_gruix)
    painter.drawRect(int(x), int(y), int(wM), int(hM))

    # ---- 3. FULLES ----
    marge = 8
    wInt = wM - 2 * marge
    hInt = hM - 2 * marge

    tipus = tipus_obertura.upper()

    num_fulles = 0
    if "2 F" in tipus:
        num_fulles = 2
    elif "1 F" in tipus:
        num_fulles = 1

    pen_fi = QPen()
    pen_fi.setWidth(1)
    painter.setPen(pen_fi)

    if num_fulles == 1:
        painter.drawRect(
            int(x + marge),
            int(y + marge),
            int(wInt),
            int(hInt)
        )
    elif num_fulles == 2:
        w_meitat = wInt / 2
        painter.drawRect(
            int(x + marge),
            int(y + marge),
            int(w_meitat),
            int(hInt)
        )
        painter.drawRect(
            int(x + marge + w_meitat),
            int(y + marge),
            int(w_meitat),
            int(hInt)
        )

    # ---- 4. MIDA A (a dalt, dins la franja discontínua) ----
    painter.setPen(QPen())
    painter.setFont(QFont("Arial", 8))

    # Centrar "A 1000" a la part superior, dins la franja discontínua
    text_a = f"A {amplada_marc:.0f}"
    # Posició: una mica per sobre del marc, al mig de la franja
    y_a = int(y - separacio + 4)
    painter.drawText(
        int(x),
        y_a,
        int(wM),
        separacio - 6,
        0x0004 | 0x0080,  # AlignCenter | AlignVCenter
        text_a
    )

    # ---- 5. MIDA H (a la dreta, girat 270°) ----
    painter.save()
    # Posicionar al bell mig de la franja dreta (entre el marc i la línia discontínua)
    centre_franja_x = x + wM + (separacio / 2)
    centre_franja_y = y + hM / 2
    painter.translate(int(centre_franja_x), int(centre_franja_y))
    painter.rotate(270)
    text_h = f"H {alcada_marc:.0f}"
    # Dibuixar centrat horitzontalment i verticalment
    painter.drawText(
        -50, -8,     # offset horitzontal i vertical
        100, 16,     # amplada i alçada
        0x0004,      # AlignCenter
        text_h
    )
    painter.restore()