"""
Funcions generals del programa.
"""


def convertir_numero(text):
    """Converteix text amb coma decimal a número."""
    if text is None:
        return 0.0
    text = str(text).strip().replace(",", ".")
    if text == "":
        return 0.0
    try:
        return float(text)
    except (ValueError, TypeError):
        return 0.0


def set_perfil_combo(combo, text_buscat):
    """Selecciona un ítem dins un QComboBox pel seu text."""
    index = combo.findText(text_buscat)
    if index >= 0:
        combo.setCurrentIndex(index)
    else:
        combo.setCurrentIndex(-1)


def format_numero(valor, decimals=1):
    """Formata un número amb coma decimal."""
    if valor is None:
        return "0"
    return f"{valor:.{decimals}f}".replace(".", ",")


def netejar_text(text):
    """Neteja un text."""
    if text is None:
        return ""
    return str(text).strip()