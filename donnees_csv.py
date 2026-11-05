"""Accès aux données — version 1 : le fichier CSV exporté lundi (J1).

Ce module LIT et CALCULE. Il ne sait rien du web : c'est main.py qui expose les résultats.
Les zones « ... » sont à compléter (méthode dans la consigne, page 5).
"""
from pathlib import Path

import pandas as pd

from erreurs import SourceIndisponible

FICHIER = Path(__file__).parent / "data" / "ventes_olist.csv"
_ventes = None  # le fichier est lu une seule fois, au premier appel


def charger() -> pd.DataFrame:
    """Fourni — lit le CSV une seule fois et garde la table en mémoire."""
    global _ventes
    if _ventes is None:
        if not FICHIER.exists():
            raise SourceIndisponible(f"Fichier introuvable : {FICHIER}")
        _ventes = pd.read_csv(FICHIER, dtype={"mois": str, "customer_state": str},
                              parse_dates=["order_purchase_timestamp"])
    return _ventes


def source() -> str:
    """Fourni."""
    return "csv"


def compter_lignes() -> int:
    """Fourni."""
    return len(charger())


def indicateurs() -> dict:
    """Mission 2 — FOURNI : lis-le ligne à ligne, c'est le modèle des fonctions suivantes."""
    # On charge le csv 'data/ventes_olist.csv'
    # (fait une seule fois)
    v = charger()
    # On récupère le nombre de commandes (colonne 'order_id)
    nb_commandes = int(v["order_id"].nunique())
    # On calcule le CA (somme des montants)
    ca_total = float(v["montant"].sum())
    return {
        "nb_lignes": len(v),
        "nb_commandes": nb_commandes,
        "ca_total": round(ca_total, 2),
        "panier_moyen": round(ca_total / nb_commandes, 2),
    }


def ventes_mensuelles(debut: str | None = None, fin: str | None = None) -> list[dict]:
    """Mission 3 — CA et nombre de commandes par mois, entre debut et fin (inclus)."""
    v = charger()

    # 1. Filtrer sur la période. debut et fin sont des textes « AAAA-MM », ou None.
    if debut is not None:
        v = v[v["mois"] >= debut]
    if fin is not None:
        v = v[v["mois"] <= fin]

    # 2. Regrouper par mois : CA = somme de montant ; commandes = nombre de order_id DISTINCTS
    m = (v.groupby("mois")
          .agg(ca=("montant", "sum"), nb_commandes=("order_id", "nunique"))
          .reset_index()
          .sort_values("mois"))

    # 3. Convertir en liste de dictionnaires aux types Python simples (str, float, int)
    return [{"mois": r.mois, "ca": round(float(r.ca), 2), "nb_commandes": int(r.nb_commandes)}
            for r in m.itertuples()]


def top_categories(n: int = 10) -> list[dict]:
    """Mission 4 — les n catégories au plus fort CA, avec leur part du CA total (en %)."""
    v = charger()

    # 1. CA total, pour calculer les parts
    total = v['montant'].sum()

    # 2. CA par catégorie, trié du plus grand au plus petit, puis les n premiers
    cat = v.groupby("categorie")["montant"].sum().sort_values(ascending=False).head(n)

    print(100 * cat / total)
    print(f"Somme des {n} parts: {(100 * cat / total).sum()}")

    # 3. Une liste de dictionnaires : categorie, ca (arrondi à 2), part_ca (en %, arrondi à 2)
    return [{"categorie": nom, 
             "ca": round(float(ca), 2), 
             "part_ca": round(100 * float(ca / total), 2)} 
             for nom, ca in cat.items()]


def etat(code: str) -> dict | None:
    """Mission 5 — chiffres d'un État brésilien (ex. « SP ») ; None s'il n'a aucune vente."""
    v = charger()

    # 1. Garder les lignes de l'État demandé
    e = v[v["customer_state"] == code]

    # 2. Aucune ligne → renvoyer None (main.py transformera ce None en erreur 404)
    if e.empty:
        return None

    # 3. Calculer et renvoyer les 4 champs
    ca = float(e["montant"].sum())
    return [{
        "etat": code,
        "ca": float(ca),
        "nb_commandes": int(v.shape[0]),
        "part_ca": round(float(100 * ca / v['montant'].sum()), 2),  # part du CA total, en %, arrondie à 2 décimales
    }]


def ca_categorie(code_cat: str) -> dict | None:
    """Mission POUR ALLER PLUS LOIN — Le CA pour une catégorie."""
    v = charger()
    print("CODE CAT", code_cat)

    # 1. On garde les lignes correspondant à la catégorie
    e = v[v["categorie"] == code_cat]

    # 2. CA total pour la catégorie pour chaque mois
    m = (e.groupby("mois")
          .agg(ca=("montant", "sum"))
          .reset_index()
          .sort_values("mois"))

    # 3. On renvoie une liste de dictionnaires avec : "categorie", "mois", "CA"
    return [{"categorie": code_cat,
             "mois": r.mois, 
             "ca": round(float(r.ca), 2)} for r in m.itertuples()]