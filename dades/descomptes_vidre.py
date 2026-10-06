"""
Fitxer de descomptes de vidre.
"""

def obtenir_descompte_vidre(batents, marc_actual, perfil_full_a, tipus_junquillo):
    descompte_h = 120
    descompte_v = 120

    if batents == 0:
        if marc_actual in ("RT650", "RT851", "RT860"):
            descompte_h = 107
            descompte_v = 107
        elif marc_actual == "RT660":
            descompte_h = 131
            descompte_v = 131
        elif marc_actual == "RT665+":
            descompte_h = 97
            descompte_v = 97

    elif batents == 1:
        if perfil_full_a == "RT661":
            if marc_actual in ("RT650", "RT851", "RT860"):
                descompte_h = 145
                descompte_v = 189
            elif marc_actual == "RT660":
                descompte_h = 169
                descompte_v = 213
            elif marc_actual == "RT665+":
                descompte_h = 135
                descompte_v = 179
        elif perfil_full_a in ("RT652", "RT659"):
            if marc_actual in ("RT650", "RT851", "RT860"):
                descompte_h = 146
                descompte_v = 146
            elif marc_actual == "RT660":
                descompte_h = 134
                descompte_v = 163
            elif marc_actual == "RT665+":
                descompte_h = 136
                descompte_v = 136

    elif batents == 2:
        if perfil_full_a == "RT661":
            if marc_actual in ("RT650", "RT851", "RT860"):
                descompte_h = 122
                descompte_v = 189
            elif marc_actual == "RT660":
                descompte_h = 134
                descompte_v = 213
            elif marc_actual == "RT665+":
                descompte_h = 117
                descompte_v = 179
        elif perfil_full_a in ("RT652", "RT659"):
            if marc_actual in ("RT650", "RT851", "RT860"):
                descompte_h = 122
                descompte_v = 146
            elif marc_actual == "RT660":
                descompte_h = 134
                descompte_v = 163
            elif marc_actual == "RT665+":
                descompte_h = 122
                descompte_v = 136

    elif batents == 3:
        descompte_h = 113
        descompte_v = 180

    elif batents == 4:
        descompte_h = 85
        descompte_v = 178

    elif batents == 5:
        descompte_h = 127
        descompte_v = 199

    elif batents == 6:
        descompte_h = 100
        descompte_v = 199

    elif batents == 7:
        descompte_h = 127
        descompte_v = 199

    elif batents == 8:
        descompte_h = 100
        descompte_v = 199

    return descompte_h, descompte_v