"""
Funcions per enviar correus (Outlook o client per defecte).
"""

import urllib.parse
import webbrowser


def enviar_correu(destinatari, assumpte, cos, parent=None):
    """
    Obre el client de correu per defecte amb les dades omplertes.
    Prioritat: Outlook → si falla, client per defecte.
    """
    # Primer intentem amb Outlook
    try:
        import win32com.client

        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = destinatari
        mail.Subject = assumpte
        mail.Body = cos
        mail.Display()
        return True
    except Exception as e:
        print(f"Outlook no disponible: {e}. Provant client per defecte...")

    # Si Outlook falla, provem el client per defecte
    try:
        # Construir l'enllaç mailto
        mailto = f"mailto:{destinatari}"
        params = {
            "subject": assumpte,
            "body": cos,
        }
        mailto += "?" + urllib.parse.urlencode(params)
        webbrowser.open(mailto)
        return True
    except Exception as e:
        print(f"Error obrint client de correu: {e}")
        return False