# 🧪 Tests automatisés (Pytest)

Ce fichier détaille le fonctionnement et l’organisation des tests unitaires utilisés pour valider l’API FastAPI.

### ✅ Objectif
Les tests ont pour but de vérifier le bon fonctionnement :
* des endpoints de l’API,
* de l’authentification,
* de la recherche et récupération des utilisateurs.

Ils sont exécutés avec **Pytest** et utilisent **FastAPI TestClient**.

## 📂 Emplacement des fichiers de test
```bash
tests/
└── test_routes.py
```

## 📄 fichier test_routes.py

### 🔐 Surcharge de l'authentification

Dans ce fichier, l’authentification est contournée avec :

```python
app.dependency_overrides[get_current_user] = lambda: "user1"
```

### 🧪 Couverture des tests

#### 🔹 Fixtures – Données simulées
* `test_token_fail()` : échec avec de mauvais identifiants → `401`
* `test_token_ok()` : succès avec les bons identifiants → `200`

#### 🔹 Endpoints publics/protégés
* `test_home()` : test de la route `/`
* `test_protected()` : test d’accès à `/protected` (**requiert auth**)

#### 🔹 Routes utilisateurs
* `test_get_all_users()` : récupération de tous les utilisateurs
* `test_get_user_ok()` : récupération d’un utilisateur existant
* `test_get_user_not_found()` : cas où l’utilisateur est introuvable
* `test_search()` : recherche d’un utilisateur via `/users/search?q=`

#### 🔹 Authentification (module `security`)
* `test_authenticate_user_valid()` : identifiants valides → True
* `test_authenticate_user_invalid_user()` : utilisateur inconnu → False
* `test_authenticate_user_invalid_password()` : mot de passe incorrect → False
* `test_create_access_token_and_decode()` : génération + décodage d’un token JWT
* `test_get_current_user_valid_token()` : extraction réussie depuis un token valide
* `test_get_current_user_invalid_token()` : échec d’extraction avec un token invalide → 401

## 🔧 Variables d’environnement requises

Assurez-vous d’avoir un fichier .env avec :
```ini
ADMIN=user1
PASSWD=motdepasse
```

## 🚀 Lancer les tests

Pour lancer tous les tests unitaires :
```bash
python -m pytest
```

Pour lancer tous les tests unitaires d'un fichier:
```bash
python -m pytest tests/test_routes.py
```

Pour lancer un test unitaire précis (pour la fonction `test_get_user_ok`) :
```bash
python -m pytest tests/test_routes.py -k test_get_user_ok
```
pour vérifier précisément les tests passé ou non:
```bash
python -m pytest -v
```
>les autres commande peuvent aussi avoir ce detail si on rajoute le `-v` après `pytest` 

[⬅️ Retour au README principal](../README.md)