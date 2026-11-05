# Journal de l'API Olist — FastAPI

**Nom : LE FUR Franck** 
**Dates :** J1 04/11/2026 · J2 05/11/2026
**Fichier rendu :** api_olist_LE_FUR.zip

> Compétences : WCS C1.6 · C2.4 · C2.1 · C2.5 (niveau 2 · Adapter) — Simplon C6 · C7 (partiel)
> Remplis les parties **dans l'ordre**. Remplace chaque « … ». Une phrase suffit sauf mention contraire.

**Chiffres de référence (export de lundi)**
- Lignes : 110 197 · Commandes livrées : 96 478
- CA total : 15 424 463,65 R$ · Panier moyen : 159,88 R$
- Novembre 2017 : 1 154 559,53 R$ et 7 289 commandes
- SP : 5 771 713,93 R$, 40 501 commandes, 37,42 % du CA

---

# J1 — L'API sur le fichier CSV

<a id="j-m1"></a>
## M1 — Lancer l'API et la tester

- Version de Python : `3.12.8`
- Commande de lancement que j'ai utilisée : `py --version`
- Code et `nb_lignes` renvoyés par `/sante` : 110197
- Différence entre `/docs` et `/sante` ouverts dans le navigateur : `/docs` renvoie la documntation automatiquement générée par FastAPI, cette documentation nous montre les routes disponibles et comment les utiliser. `/sante` est une route spécifique qui renvoie des informations comme le nombre de ligne dans le CSV : /data/ventes_olist.csv
- Problème rencontré et solution (ou « aucun ») : aucun

<a id="j-m2"></a>
## M2 — Lire une route complète

### Le trajet d'une requête `GET /indicateurs`, en 4 étapes

1. Le navigateur envoie `/indicateurs` à l'adresse `localhost` (`http://127.0.0.1:8000`)
2. FastAPI exécute la fonction `indicateurs()` du fichier `main.py`, qui appelle la méthode `indicateurs()` de la classe `donnees`
3. Cette fonction lit le fichier CSV `ventes_olist.csv` et renvoie le nombre de lignes du csv, le nombre de commandes (en fonction de la colonne "order_id), le chiffre d'affaires total (calculé à partir de la colonne `montant`), la valeur du panier moyen (CA / nb_commandes)
4. Le modèle `Pydantic Indicateurs` vérifie la structure attendue de la réponse puis FastAPI renvoie les résultat sous forme d'un JSON avec le code 200

### L'expérience du contrat

- Quand j'ai mis `panier_moyen` en commentaire dans le modèle, la réponse est un JSON qui ne contient pas le 'panier moyen' (il n'y a plus que 3 éléments dans le JSON).
- Conclusion : La route renvoie un dictionnaire avec le 'panier moyen' mais comme celui-ci est inconnu dans le modèle (car mis en commentaire) l'application ne l'affiche pas dans la page web.

### Pourquoi deux fichiers (`main.py` et `donnees_csv.py`) ?

- `main.py` contient les routes (les points d'entrée), ces routes font appel aux différents modules python, notamment le module `donnees_csv` qui contient les manipulations faites sur le fichier CSV.

### Comparaison avec lundi

- `nb_commandes` : 96478 (lundi : 96 478)
- `ca_total` : 15 424 463.65 (lundi : 15 424 463,65)

<a id="j-m3"></a>
## M3 — Ventes mensuelles

### Tests

- Sans paramètre : 23 mois, du 2016-09 au 2018-08
- `debut=2017-01` et `fin=2017-12` : 12 mois ; novembre 2017 = 1 154 559.53 R$ et 7289 commandes
- `debut=2018-02` et `fin=2017-01` : code 400 , message `« debut » doit être antérieur ou égal à « fin ».`
- `debut=2017-13` : code 422

### Questions

1. Différence entre un paramètre de chemin et un paramètre de requête, avec un exemple de cette API : …
2. Qui renvoie le code 400 (toi ou FastAPI) ? Et le code 422 ? Pourquoi cette différence ? Nous déclenchons l'erreur 400 nous-même dans notre code lorsque nous détectons que la date de "début" est après la date de "fin". FastAPI renvoie un code erreur 422 lorsqu'il détecte que les paramètres ne respectent pas les contraintes que l'on a spécifiées, dans l'exemple lorsque l'on met une date avec un mois "13" on ne respecte plus la RegEx : `pattern=r"^\d{4}-(0[1-9]|1[0-2])$` et FastAPI renvoie l'erreur 422.

<a id="j-m4"></a>
## M4 — Top catégories

### Tests

- Sans paramètre : 10 catégories ; la première est "health_beauty avec 9.16 %
- Somme des 10 parts : 62.4 %
- `n=3` : Requête : `http://127.0.0.1:8000/categories/top?n=3` la somme des 3 parts est 25.3 %
- `n=0` : code 422 · `n=51` : code 422. Dans ces deux cas, Les arguments de la requête ne respectent pas la contrainte `int = Query(10, ge=1, le=50)`

### Question

- Que reçoit Rafael s'il n'envoie pas `n` ? Où est-ce décidé dans le code ? Sans préciser l'argument n, c'est la valeur 10 qui est prise par défaut. On le voit ici : `int = Query(10, ge=1, le=50)`, le 10 signifie "valeur par défaut", "ge" et "le" définissent le min et max autorisé pour "n".

<a id="j-m5"></a>
## M5 — Chiffres d'un État

### Mon modèle `Etat` (copie le code)

```python
class VentesEtat(BaseModel):
    etat: str
    ca: float
    nb_commandes: int
    part_ca: float
```

### Tests

- `/etats/SP` : CA 5771713.93 , commandes 110197 , part 37.42 %
- `/etats/sp` : identique (oui / non) : OUI
- `/etats/XX` : code 404 , message "Aucune vente pour l'État « SX » (ou bien cet état n'existe pas)."
- `/etats/SPX` : code 422

### Question

- Pourquoi un État sans vente renvoie 404 et pas une réponse vide avec le code 200 ?
Parce que dès que le filtre `e = v[v["customer_state"] == code]` renvoie un dataframe vide nous renvoyons un code erreur 404. Il y a 2 sources possibles d'un dataframe vide à cette étape : 1 l'état n'existe pas, 2 : Les ventes de l'état sont réellement vides. Il faudrait affiner l'étude et tester si le code état existe réellement dans la base.

<a id="j-m6"></a>
## M6 — Recette complète dans /docs

Pour chaque test : le code obtenu, puis une valeur lue dans la réponse.

1. `GET /sante` (attendu 200) : "nb_lignes" : 110197
2. `GET /indicateurs` (attendu 200) : "ca_total": 15424463.65
3. `GET /ventes/mensuelles` sans paramètre (attendu 200, 23 mois) : "mois": "2016-10", "ca": 46490.66, "nb_commandes": 265
4. `GET /ventes/mensuelles?debut=2018-01` (attendu 200) : nombre de mois 8
5. `GET /ventes/mensuelles?debut=2018-02&fin=2017-01` (attendu 400) : CODE 400 et MESSAGE : "detail":"« debut » doit être antérieur ou égal à « fin »."
6. `GET /ventes/mensuelles?fin=nov` (attendu 422) : CODE 422 et MESSAGE indiquant que le pattern RegEx n'est pas respecté.
7. `GET /categories/top` (attendu 200, 10 catégories) : CODE 200 et les 10 catégories ayant le plus gros CA.
8. `GET /categories/top?n=50` (attendu 200) : dernière catégorie de la liste "books_technical" avec une part de 0.15 %
9. `GET /categories/top?n=0` (attendu 422) : CODE 422 et MESSAGE nous indiquant que n doit être strictement supérieur à 0.
10. `GET /etats/RJ` (attendu 200) : part du CA 13.33 %
11. `GET /etats/XX` (attendu 404) : CODE 404 et MESSAGE : "Aucune vente pour l'État « XX » (ou bien cet état n'existe pas)."
12. `GET /etats/SPX` (attendu 422) : CODE 422 et MESSAGE : "Le code_etat ne respecte pas le RegEx" ("String should match pattern '^[A-Za-z]{2}$'","input":"SPX")

### Bilan du J1

1. Ce qui fonctionne : On sait créer des routes GET (avec ou sans paramètres), faire des appels d'API et gérer les erreurs.
2. Ce qui me reste à comprendre ou à terminer : …

---

# J2 — L'API sur PostgreSQL

<a id="j-m7"></a>
## M7 — Charger les ventes dans PostgreSQL

- Base utilisée : …
- Résultat du contrôle final du script : … lignes, … commandes, … de CA
- Droit donné à `lecteur_olist` sur la table, et pourquoi seulement celui-là : …

<a id="j-m8"></a>
## M8 — Mettre les secrets dans `.env`

- Résultat de la commande de test : …
- Rôle de `.env` : …
- Rôle de `.env.exemple` : …
- Rôle de la ligne `.env` dans `.gitignore` : …
- J'ai vérifié qu'aucun `.py` ne contient le mot de passe (oui / non) : …

<a id="j-m9"></a>
## M9 — Réécrire les fonctions en SQL

### Résultat de `verifier_sources.py`

- Bilan affiché : … / 8
- Fonction qui m'a demandé le plus de corrections, et pourquoi : …

### Ma requête de `top_categories()` (copie-la)

```sql
…
```

### Sécurité

- Pourquoi `%(code)s` plutôt qu'une f-string ? Donne l'exemple d'une valeur dangereuse. …
- Pourquoi faire calculer PostgreSQL plutôt que Python ? …

<a id="j-m10"></a>
## M10 — Basculer l'API sur PostgreSQL

- `/sante` après la bascule : source … , lignes …
- Pourquoi il faut relancer l'API après avoir modifié `.env` : …
- Test de panne (`PGPORT=5999`) : code … , message …
- Ce qu'aurait vu Rafael sans le gestionnaire d'erreur `SourceIndisponible` : …
- Ce que Rafael a dû changer dans son code pour la bascule : …

<a id="j-m11"></a>
## M11 — Écrire le client de Rafael

- Bilan affiché par `client.py` : … / 10
- Nombre de lignes de `ca_mensuel_2017.csv`, en-tête compris : …
- Différence entre `.status_code` et `.json()` : …
- Utilité du paramètre `timeout` : …

<a id="j-m12"></a>
## M12 — README et rendu

- Le test de remise à zéro a fonctionné en suivant seulement le README (oui / non) : …
- Ce que j'ai dû corriger dans le README après ce test : …
- Contenu de mon zip, fichier par fichier : …

### Mes choix techniques (3 à 5 lignes)

- Source de données retenue et pourquoi : …
- Compte de connexion et pourquoi : …
- Gestion des erreurs : …
- Ce que j'ajouterais pour mettre l'API en production : …

### Message à Mariana (3 lignes, sans jargon)

- Ce que Rafael peut faire maintenant : …
- D'où viennent les chiffres : …
- Le chiffre qui prouve que c'est juste : …
