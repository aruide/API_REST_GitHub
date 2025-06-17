# Extraction et Filtrage des Données GitHub

Ce projet contient deux scripts principaux pour extraire et traiter des données utilisateurs depuis l'API GitHub. Le but est d’obtenir un jeu de données nettoyé et filtré d’utilisateurs GitHub répondant à certains critères métier.

## 📁 Contenu des scripts
|Script|Description|
|---|---|
|extract_users.py|Extraction des utilisateurs depuis l’API GitHub|
|filtered_users.py|Nettoyage, suppression des doublons et filtrage métier|

## Extraction des utilisateurs (extract_users.py)

### Fonction principale
* fetch_users(max_users)
* Extrait des utilisateurs en paginant via le paramètre since de l’API GitHub.
* Pour chaque utilisateur, récupère les détails complets via une requête secondaire.
* Respecte les quotas d’API GitHub et gère les erreurs/retries.
* Stocke les utilisateurs sous forme de dictionnaires avec ces champs :
login, id, created_at, avatar_url, bio.

### Gestion des quotas API
* Lit les headers de réponse pour connaître le quota restant et le temps de reset.
* Met en pause le script si le quota est épuisé pour éviter des erreurs 403.
* Gère aussi les erreurs 429 (trop de requêtes) et 5xx (erreur serveur).

### Fonction d’enregistrement
`save_to_json(data, path="data/users.json")`
* Sauvegarde les données extraites au format JSON UTF-8.

### Usage
```bash
python extract_users.py --max-users 50
```
Extrait 50 utilisateurs depuis GitHub et sauvegarde dans `data/users.json`.

## Filtrage des utilisateurs (`filtered_users.py`)

### Étapes du filtrage
1. Chargement des données JSON
    * Lit le fichier data/users.json et vérifie la structure.

2. Suppression des doublons
    * Élimine les utilisateurs en double selon leur id.

3. Filtrage métier
    * Ne garde que les utilisateurs dont :
        * La date de création est postérieure au 1er janvier 2015.
        * Le champ bio est non vide.
        * L’URL d’avatar est présente.

4. Sauvegarde des résultats
    * Enregistre les utilisateurs filtrés dans data/filtered_users.json.

### Usage
```bash
python filtered_users.py
```
Affiche un résumé du traitement avec le nombre d’utilisateurs chargés, doublons supprimés, et utilisateurs finaux retenus.

## ⚠️ Pré-requis et notes
* Un token GitHub valide doit être défini dans le fichier .env sous la variable GITHUB_TOKEN.
* Le dossier data doit être accessible en écriture.
* Le script filtered_users.py attend que le fichier data/users.json soit déjà présent (généré par extract_users.py).

## 🔗 Fichiers de configuration
Le fichier config.py contient les constantes d’URL et paramètres utilisés par les scripts :
```python
GIT_URL_USERS = "https://api.github.com/users?since="
SINCE = 10367555
GIT_URL_USER_INFO = "https://api.github.com/users"
```

### Description des variables
* `GIT_URL_USERS`
    * URL de base pour récupérer la liste des utilisateurs GitHub.
    * Le paramètre since est un ID utilisateur :
        * La requête https://api.github.com/users?since=10367555 retournera les utilisateurs ayant un ID supérieur à ce nombre.
        * Cela permet de paginer les résultats et d’extraire des lots successifs d’utilisateurs.

* `SINCE`
    * Valeur initiale utilisée pour le paramètre since dans la première requête.
    * Ce nombre est un ID GitHub à partir duquel l’extraction commence.
    * Cette valeur peut être ajustée selon les besoins (par exemple, pour ne pas reprendre des utilisateurs déjà extraits).

* `GIT_URL_USER_INFO`
    * URL de base pour récupérer les détails complets d’un utilisateur donné.
    * Lors de l’extraction, après avoir obtenu la liste basique des utilisateurs, une requête supplémentaire est faite avec :
https://api.github.com/users/<login>
    * Cela permet d’obtenir des informations détaillées (date de création, bio, avatar, etc.) nécessaires pour le filtrage.

### Pourquoi externaliser ces variables ?
* **Facilité de maintenance** : si GitHub modifie ses endpoints, il suffit de changer une valeur dans config.py sans modifier plusieurs fichiers.

* **Personnalisation** : possibilité d’adapter facilement le point de départ (SINCE) pour reprendre l’extraction à un certain stade.

* **Clarté** : regroupe toutes les URLs dans un seul fichier, rendant le code plus lisible et modulaire.

### Exemple d’utilisation dans les scripts
```bash
url = f"{GIT_URL_USERS}{since}"  # Construction dynamique de l'URL pour lister les utilisateurs
detail_url = f"{GIT_URL_USER_INFO}/{login}"  # URL pour récupérer les infos détaillées d'un utilisateur
```

## Résumé du flux
1. Extraction :
    * `extract_users.py` → `data/users.json`

2. Filtrage :
    * `filtered_users.py` → `data/filtered_users.json`

[⬅️ Retour au README principal](../README.md)