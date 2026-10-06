"""
Càlcul de tots els talls d'una finestra/porta.
Equivalent al cos del btnAfegir_Click del VBA.
"""

from dades.perfils import obtenir_gruix_perfil
from dades.descomptes_vidre import obtenir_descompte_vidre


def calcular_talls(
    batents,
    marc_actual,
    perfil_full_a,
    tipus_junquillo,
    amplada,
    alcada,
    quantitat,
    angle_esq,
    angle_dret,
    color_actual,
    codi_feina,
    codi_client,
    farciment,
    afegir_gotero=False,
    reduccio_marc=None,
    reduccio_full_a=None
):
    """
    Calcula tots els talls d'una finestra/porta.

    Returns:
        dict amb:
            - 'talls': llista de diccionaris amb cada peça
            - 'vidre': info del vidre (mides, quantitat) o None
    """

    talls = []

    # ============================================================
    #  GRUIXOS
    # ============================================================
    gruix_marc = obtenir_gruix_perfil(marc_actual)
    gruix_full_a = obtenir_gruix_perfil(perfil_full_a)

    # ============================================================
    #  DIMENSIONS DE LA FULLA SEGONS TIPUS D'OBERTURA
    # ============================================================
    l_full_a_ba = 0
    l_full_a_al = 0
    l_inversor = 0
    full_a_ba_70 = 0
    full_a_al_70 = 0
    creuament_70 = 0
    full_a_ba_70p = 0
    full_a_al_70p = 0
    creuament_70p = 0
    full_a_ba_85 = 0
    full_a_al_85 = 0
    creuament_85 = 0
    full_a_ba_85p = 0
    full_a_al_85p = 0
    creuament_85p = 0
    full_a_ba_899 = 0
    full_a_al_899 = 0
    creuament_899 = 0
    full_a_ba_899p = 0
    full_a_al_899p = 0
    creuament_899p = 0

    # ------------------------------------------------------------
    #  BOCA 0: MARC (només marc)
    # ------------------------------------------------------------
    # (no necessita mides de fulla)

    # ------------------------------------------------------------
    #  BOCA 1: FINESTRA 1 FULLA
    # ------------------------------------------------------------
    if batents == 1:
        if marc_actual == "RT665+":
            l_full_a_ba = amplada - 41
            l_full_a_al = alcada - 41
        elif marc_actual == "RT660":
            l_full_a_ba = amplada - 75
            l_full_a_al = alcada - 75
        elif marc_actual in ("RT650", "RT851", "RT860"):
            l_full_a_ba = amplada - 51
            l_full_a_al = alcada - 51
        else:
            l_full_a_ba = amplada - 51
            l_full_a_al = alcada - 51

    # ------------------------------------------------------------
    #  BOCA 2: FINESTRA 2 FULLES
    # ------------------------------------------------------------
    elif batents == 2:
        if marc_actual == "RT665+":
            l_full_a_ba = amplada / 2 - 23
            l_full_a_al = alcada - 41
            l_inversor = alcada - 112
        elif marc_actual == "RT660":
            l_full_a_ba = amplada / 2 - 40
            l_full_a_al = alcada - 75
            l_inversor = alcada - 146
        elif marc_actual in ("RT650", "RT851", "RT860"):
            l_full_a_ba = amplada / 2 - 28
            l_full_a_al = alcada - 51
            l_inversor = alcada - 122
        else:
            l_full_a_ba = amplada / 2 - 28
            l_full_a_al = alcada - 51
            l_inversor = alcada - 122

    # ------------------------------------------------------------
    #  BOCA 3: CORREDERA 70 NORMAL
    # ------------------------------------------------------------
    elif batents == 3:
        full_a_ba_70 = amplada / 2 + 8
        full_a_al_70 = alcada - 55
        creuament_70 = alcada - 125

    # ------------------------------------------------------------
    #  BOCA 4: CORREDERA 70 PANORÀMICA
    # ------------------------------------------------------------
    elif batents == 4:
        full_a_ba_70p = amplada / 2 - 23
        full_a_al_70p = alcada - 55
        creuament_70p = alcada - 55

    # ------------------------------------------------------------
    #  BOCA 5: CORREDERA 85 NORMAL
    # ------------------------------------------------------------
    elif batents == 5:
        full_a_ba_85 = amplada / 2 - 6
        full_a_al_85 = alcada - 84
        creuament_85 = alcada - 84

    # ------------------------------------------------------------
    #  BOCA 6: CORREDERA 85 PANORÀMICA
    # ------------------------------------------------------------
    elif batents == 6:
        full_a_ba_85p = amplada / 2 - 39
        full_a_al_85p = alcada - 84
        creuament_85p = alcada - 84

    # ------------------------------------------------------------
    #  BOCA 7: CORREDERA 85 EMPOTRABLE
    # ------------------------------------------------------------
    elif batents == 7:
        full_a_ba_899 = amplada / 2 + 3
        full_a_al_899 = alcada - 68
        creuament_899 = alcada - 68

    # ------------------------------------------------------------
    #  BOCA 8: CORREDERA 85 EMPOTRABLE PANORÀMICA
    # ------------------------------------------------------------
    elif batents == 8:
        full_a_ba_899p = amplada / 2 - 30.5
        full_a_al_899p = alcada - 68
        creuament_899p = alcada - 68

    # ============================================================
    #  APLICAR REDUCCIÓ AL MARC (opcional, per talls a 90°)
    # ============================================================
    amplada_final = amplada
    alcada_final = alcada

    if reduccio_marc and angle_esq == 90 and angle_dret == 90:
        eix = reduccio_marc.get("eix", "A").upper()
        valor = reduccio_marc.get("valor", 0)
        if eix in ("A", "AMPLADA"):
            amplada_final = amplada - (2 * valor)
        elif eix in ("H", "ALCADA"):
            alcada_final = alcada - (2 * valor)

    # ============================================================
    #  AFEGIR MARC (MarcBA i MarcAL)
    # ============================================================
    mida_marc_ba = amplada_final + 62 if (batents <= 2 and marc_actual == "RT665+") else amplada_final
    mida_marc_al = alcada_final + 62 if (batents <= 2 and marc_actual == "RT665+") else alcada_final

    talls.append({
        "mida": mida_marc_ba,
        "angle_esq": angle_esq,
        "angle_dret": angle_dret,
        "quantitat": 2 * quantitat,
        "perfil": marc_actual,
        "gruix": gruix_marc,
        "descripcio": "MarcBA",
        "tipus_obertura": "",
        "color": color_actual,
        "codi_feina": codi_feina
    })

    talls.append({
        "mida": mida_marc_al,
        "angle_esq": angle_esq,
        "angle_dret": angle_dret,
        "quantitat": 2 * quantitat,
        "perfil": marc_actual,
        "gruix": gruix_marc,
        "descripcio": "MarcAL",
        "tipus_obertura": "",
        "color": color_actual,
        "codi_feina": codi_feina
    })

    # ============================================================
    #  BOCA 0: MARC (només marc)
    # ============================================================
    if batents == 0:
        pass  # No s'afegeix res més

    # ============================================================
    #  BOCA 1: FINESTRA 1 FULLA
    # ============================================================
    elif batents == 1:
        talls.append({
            "mida": l_full_a_ba,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 2 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": l_full_a_al,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 2 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })

    # ============================================================
    #  BOCA 2: FINESTRA 2 FULLES
    # ============================================================
    elif batents == 2:
        talls.append({
            "mida": l_full_a_ba,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": l_full_a_al,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        # Inversor
        talls.append({
            "mida": l_inversor,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 1 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Inversor",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })

    # ============================================================
    #  BOCA 3: CORREDERA 70 NORMAL
    # ============================================================
    elif batents == 3:
        talls.append({
            "mida": full_a_ba_70,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": full_a_al_70,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": creuament_70,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 2 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Creuament",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        if afegir_gotero:
            talls.append({
                "mida": amplada,
                "angle_esq": 90,
                "angle_dret": 90,
                "quantitat": 1 * quantitat,
                "perfil": "74663",
                "gruix": gruix_marc,
                "descripcio": "Goteron",
                "tipus_obertura": "",
                "color": color_actual,
                "codi_feina": codi_feina
            })

    # ============================================================
    #  BOCA 4: CORREDERA 70 PANORÀMICA
    # ============================================================
    elif batents == 4:
        talls.append({
            "mida": full_a_ba_70p,
            "angle_esq": 90,
            "angle_dret": 45,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": full_a_al_70p,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 2 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": creuament_70p,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 2 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Creuament",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        if afegir_gotero:
            talls.append({
                "mida": amplada,
                "angle_esq": 90,
                "angle_dret": 90,
                "quantitat": 1 * quantitat,
                "perfil": "74663",
                "gruix": gruix_marc,
                "descripcio": "Goteron",
                "tipus_obertura": "",
                "color": color_actual,
                "codi_feina": codi_feina
            })

    # ============================================================
    #  BOCA 5: CORREDERA 85 NORMAL
    # ============================================================
    elif batents == 5:
        talls.append({
            "mida": full_a_ba_85,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": full_a_al_85,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": creuament_85,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 2 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Creuament",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        if afegir_gotero:
            talls.append({
                "mida": amplada,
                "angle_esq": 90,
                "angle_dret": 90,
                "quantitat": 1 * quantitat,
                "perfil": "74663",
                "gruix": gruix_marc,
                "descripcio": "Goteron",
                "tipus_obertura": "",
                "color": color_actual,
                "codi_feina": codi_feina
            })

    # ============================================================
    #  BOCA 6: CORREDERA 85 PANORÀMICA
    # ============================================================
    elif batents == 6:
        talls.append({
            "mida": full_a_ba_85p,
            "angle_esq": 45,
            "angle_dret": 90,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": full_a_al_85p,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 2 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": creuament_85p,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 2 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Creuament",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        if afegir_gotero:
            talls.append({
                "mida": amplada,
                "angle_esq": 90,
                "angle_dret": 90,
                "quantitat": 1 * quantitat,
                "perfil": "74663",
                "gruix": gruix_marc,
                "descripcio": "Goteron",
                "tipus_obertura": "",
                "color": color_actual,
                "codi_feina": codi_feina
            })

    # ============================================================
    #  BOCA 7: CORREDERA 85 EMPOTRABLE
    # ============================================================
    elif batents == 7:
        talls.append({
            "mida": full_a_ba_899,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": full_a_al_899,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": creuament_899,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 2 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Creuament",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        if afegir_gotero:
            talls.append({
                "mida": amplada,
                "angle_esq": 90,
                "angle_dret": 90,
                "quantitat": 1 * quantitat,
                "perfil": "74663",
                "gruix": gruix_marc,
                "descripcio": "Goteron",
                "tipus_obertura": "",
                "color": color_actual,
                "codi_feina": codi_feina
            })

    # ============================================================
    #  BOCA 8: CORREDERA 85 EMPOTRABLE PANORÀMICA
    # ============================================================
    elif batents == 8:
        talls.append({
            "mida": full_a_ba_899p,
            "angle_esq": 45,
            "angle_dret": 90,
            "quantitat": 4 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaBA",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": full_a_al_899p,
            "angle_esq": angle_esq,
            "angle_dret": angle_dret,
            "quantitat": 2 * quantitat,
            "perfil": perfil_full_a,
            "gruix": gruix_full_a,
            "descripcio": "FullaAL",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        talls.append({
            "mida": creuament_899p,
            "angle_esq": 90,
            "angle_dret": 90,
            "quantitat": 2 * quantitat,
            "perfil": "RT003",
            "gruix": gruix_full_a,
            "descripcio": "Creuament",
            "tipus_obertura": "",
            "color": color_actual,
            "codi_feina": codi_feina
        })
        if afegir_gotero:
            talls.append({
                "mida": amplada,
                "angle_esq": 90,
                "angle_dret": 90,
                "quantitat": 1 * quantitat,
                "perfil": "74663",
                "gruix": gruix_marc,
                "descripcio": "Goteron",
                "tipus_obertura": "",
                "color": color_actual,
                "codi_feina": codi_feina
            })

    # ============================================================
    #  CÀLCUL DEL VIDRE
    # ============================================================
    vidre_info = None

    if farciment.upper() in ("VIDRE", "PANELL"):
        descompte_h, descompte_v = obtenir_descompte_vidre(
            batents, marc_actual, perfil_full_a, tipus_junquillo
        )

        if batents == 0:
            vidre_h = amplada - descompte_h
            vidre_v = alcada - descompte_v
            quantitat_vidre = quantitat
        elif batents == 1:
            vidre_h = l_full_a_ba - descompte_h
            vidre_v = l_full_a_al - descompte_v
            quantitat_vidre = quantitat
        elif batents == 2:
            vidre_h = l_full_a_ba - descompte_h
            vidre_v = l_full_a_al - descompte_v
            quantitat_vidre = 2 * quantitat
        elif batents == 3:
            vidre_h = full_a_ba_70 - descompte_h
            vidre_v = full_a_al_70 - descompte_v
            quantitat_vidre = 2 * quantitat
        elif batents == 4:
            vidre_h = full_a_ba_70p - descompte_h
            vidre_v = full_a_al_70p - descompte_v
            quantitat_vidre = 2 * quantitat
        elif batents == 5:
            vidre_h = full_a_ba_85 - descompte_h
            vidre_v = full_a_al_85 - descompte_v
            quantitat_vidre = 2 * quantitat
        elif batents == 6:
            vidre_h = full_a_ba_85p - descompte_h
            vidre_v = full_a_al_85p - descompte_v
            quantitat_vidre = 2 * quantitat
        elif batents == 7:
            vidre_h = full_a_ba_899 - descompte_h
            vidre_v = full_a_al_899 - descompte_v
            quantitat_vidre = 2 * quantitat
        elif batents == 8:
            vidre_h = full_a_ba_899p - descompte_h
            vidre_v = full_a_al_899p - descompte_v
            quantitat_vidre = 2 * quantitat
        else:
            vidre_h = 0
            vidre_v = 0
            quantitat_vidre = 0

        vidre_info = {
            "amplada": vidre_h,
            "alcada": vidre_v,
            "quantitat": quantitat_vidre,
            "tipus": farciment.upper()
        }

    return {
        "talls": talls,
        "vidre": vidre_info
    }