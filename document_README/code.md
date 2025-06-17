# 📘 Explication du code de base

Ce document détaille le fonctionnement et la structure des fichiers principaux de l’API GitHub Users.

## 📄 main.py

### Rôle :
* Crée l'application FastAPI.
* Charge les données JSON filtrées (filtered_users.json) au démarrage.
* Enregistre les routes via app.include_router(router).

### Points clés :

* **users_data** est une liste en mémoire qui contient tous les utilisateurs.
* Le fichier **filtered_users.json** doit être présent dans **data/**.

## 📄 models.py

### Rôle :
* Définit le **modèle Pydantic** `User` utilisé pour la validation et la sérialisation des données utilisateur.

### Exemple :

Un utilisateur est représenté comme :
```bash
{
  "login": "user1",
  "id": 123,
  "created_at": "2023-01-01T12:00:00Z",
  "avatar_url": "https://...",
  "bio": "Développeur"
}
```

## 📄 routes.py

Contient toutes les routes principales de l’API.

### ✅ Accès public :
* `GET /` → Retourne un message de bienvenue.
* `POST /token` → Génère un token JWT après vérification des identifiants.

### 🔒 Accès protégé (token requis) :
* `GET /users/` → Retourne la liste des utilisateurs.
* `GET /users/search?q=xxx` → Recherche un utilisateur par login.
* `GET /users/{login}` → Détail d’un utilisateur précis.
* `GET /protected` → Démonstration d’une route sécurisée.

## 📄 security.py

Gère l’authentification via JWT.

### Fonctionnalités :
* `authenticate_user()` → Vérifie les identifiants contre des valeurs définies dans .env.
* `create_access_token()` → Crée un JWT avec une durée d’expiration.
* `get_current_user()` → Décodage du token pour protéger les routes.

### Dépendances :
* `python-jose` pour manipuler les tokens.
* `secrets.compare_digest()` pour comparer les mots de passe de manière sécurisée.

## 📄 .env (non versionné)
Permet de stocker les paramètres sensibles :

```ini
SECRET_KEY=une_clé_secrète #
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN=admin123
PASSWD=password
```

### Variables définies :
|Variable|Description|
|---|---|
|SECRET_KEY|	Clé secrète utilisée pour signer et valider les JWT (JSON Web Tokens).
|ALGORITHM|	Algorithme de chiffrement pour les tokens JWT (par exemple HS256).
|ACCESS_TOKEN_EXPIRE_MINUTES|	Durée de validité des tokens d’accès en minutes (ex : 30 signifie que le token expire après 30 minutes).
|ADMIN|	Nom d’utilisateur administrateur autorisé à se connecter (exemple : admin123).
|PASSWD|	Mot de passe associé à l’administrateur (exemple : password).


## 📁 Exemple de flow d’authentification
1. `POST /token` avec login + mot de passe.
2. Récupérer le access_token.
3. Utiliser ce token dans le header :
```bash
Authorization: Bearer <token>
```
4. Accéder aux routes protégées.

[⬅️ Retour au README principal](../README.md)