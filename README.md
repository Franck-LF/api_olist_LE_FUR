# API des indicateurs de ventes Olist

> À compléter le J2 (mission 12). Remplace chaque « … ». Ce fichier s'adresse à un développeur
> qui découvre le projet : il doit pouvoir installer et lancer l'API sans te poser de question.

## Objet

Utiliser une API pour "exposer" un fichier CSV ainsi qu'une base de données à nos utilisateurs.
Savoir configurer une route.

## Prérequis

- Python 3.12.8 
- Les fichiers du projets

## Installation

1. Copie du répertoire avec les fichiers
2. Création d'un environnement virtuel venv

## Configuration

installation des modules python à partir du fichier "requirements"

## Lancement

py -m uvicorn main:app --reload

## Routes

**`GET /sante`**
- Rôle : Teste si la lecture du CSV se fait correctement et renvoie le nombre de lignes du CSV.
- Paramètres : aucun
- Exemple de réponse : 
`"statut": "ok",
  "source": "csv",
  "nb_lignes": 110197`

**`GET /indicateurs`**
- Rôle : Renvoie quelques informations élémentaires sur les données du CSV (CA, panier moyen ...)
- Paramètres : aucun
- Exemple de réponse : `"nb_lignes": 110197,
  "nb_commandes": 96478,
  "ca_total": 15424463.65,
  "panier_moyen": 159.88`


**`GET /ventes/mensuelles`**
- Rôle : Renvoie les informations "mois", "ca" et "nb_commandes" pour chaque mois dans la période envoyée dans la requête.
- Paramètres : Une date de début 'YYYY-MM' et une date de fin sous le même format.
- Exemple d'appel : `http://127.0.0.1:8000/ventes/mensuelles?debut=2017-01&fin=2017-12`

**`GET /categories/top`**
- Rôle : Renvoie les informations des catégories ayant le plus fort CA ainsi que leur part dans le CA total.
- Paramètres : n : le nombre de catégories à renvoyer.
- Exemple d'appel : `http://127.0.0.1:8000/categories/top?n=8`

**`GET /etats/{code_etat}`**
- Rôle : Renvoie le CA, le nombre de commandes et la part du CA de l'état.
- Paramètres : code_etat (chaine de caractères à 2 lettres)
- Exemple d'appel : `http://127.0.0.1:8000/etats/sp`

## Codes de réponse

- `200` : C'est le code succès, tout va bien.
- `400` : Si la date de "début" est après la date de "fin" de la période.
- `404` : Si l'état n'a effectué aucune vente ou bien que le code n'état n'existe pas dans le dataframe. (Remarque : Le code 404 est habituellement réservé si le serveur n'a pas trouvé la ressource, par exemple parce que l'URL est incorrecte (route non définie)).
- `422` : Si l'un des paramètres envoyés à la route ne respecte pas les contraintes prédéfinies.
- `503` : Le serveur n'est pas disponible, la requête ne peut pas être traités.

## Sécurité

- …
- …

## Données

Olist, *Brazilian E-Commerce Public Dataset* (Kaggle), licence CC BY-NC-SA 4.0. …
