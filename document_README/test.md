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

## 🔧 Variables d’environnement requises

Assurez-vous d’avoir un fichier .env avec :
```ini
ADMIN=user1
PASSWD=motdepasse
```
[⬅️ Retour au README principal](../README.md)