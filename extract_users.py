import requests
import os
import time
import argparse
import json
from dotenv import load_dotenv
import sys
import io
from config import GIT_URL_USERS, SINCE, GIT_URL_USER_INFO

# Encodage UTF-8 pour éviter les erreurs d'affichage
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Charger les variables d'environnement (.env)
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

def check_rate_limit(response):
    """
    Vérifie les quotas de l'API GitHub et met le script en pause si la limite est atteinte.

    Args:
        response (requests.Response): La réponse HTTP de l'API GitHub.
    """
    remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

    if remaining == 0:
        wait_time = reset_time - int(time.time())
        if wait_time > 0:
            print(f"[Quota] Limite atteinte. Pause de {wait_time} secondes (~{wait_time // 60} min).")
            time.sleep(wait_time + 1)

def safe_request(url, max_retries=5):
    """
    Effectue une requête GET sécurisée avec gestion des erreurs, des quotas et des tentatives.

    Args:
        url (str): L'URL à interroger.
        max_retries (int): Le nombre maximum de tentatives en cas d'erreur.

    Returns:
        requests.Response | None: La réponse HTTP en cas de succès, sinon None.
    """
    delay = 5
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            status = response.status_code

            if status == 200:
                check_rate_limit(response)
                return response

            elif status == 403:
                print(f"[403] Accès interdit. Vérifie ton token ou quota. URL : {url}")
                check_rate_limit(response)
                time.sleep(delay)

            elif status == 429:
                print(f"[429] Trop de requêtes. Attente de {delay} secondes...")
                time.sleep(delay)
                delay *= 2

            elif 500 <= status < 600:
                print(f"[{status}] Erreur serveur GitHub. Tentative {attempt+1}/{max_retries}")
                time.sleep(delay)
                delay *= 2

            else:
                print(f"[{status}] Erreur inconnue pour URL : {url}")
                break

        except requests.exceptions.RequestException as e:
            print(f"[Exception] {e}")
            time.sleep(delay)

    return None

def fetch_users(max_users):
    """
    Récupère les profils d'utilisateurs GitHub via l'API publique jusqu'à atteindre le nombre demandé.

    Args:
        max_users (int): Nombre maximum d'utilisateurs à récupérer.

    Returns:
        list[dict]: Liste de dictionnaires contenant les données des utilisateurs.
    """
    users_data = []
    since = SINCE

    while len(users_data) < max_users:
        url = f"{GIT_URL_USERS}{since}"
        response = safe_request(url)

        if response is None:
            break

        users = response.json()
        if not users:
            break

        for user in users:
            login = user['login']
            detail_url = f"{GIT_URL_USER_INFO}/{login}"
            detail_response = safe_request(detail_url)

            if detail_response:
                detail = detail_response.json()
                users_data.append({
                    "login": detail.get("login"),
                    "id": detail.get("id"),
                    "created_at": detail.get("created_at"),
                    "avatar_url": detail.get("avatar_url"),
                    "bio": detail.get("bio")
                })

                if len(users_data) >= max_users:
                    break
            else:
                print(f"[Erreur] Impossible de récupérer les infos pour {login}")

        since = users[-1]['id']

    return users_data

def save_to_json(data, path="data/users.json"):
    """
    Enregistre une liste d'utilisateurs au format JSON dans le fichier spécifié.

    Args:
        data (list): Les données à enregistrer.
        path (str): Le chemin du fichier JSON de sortie.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Données enregistrées dans {path}")

if __name__ == "__main__":
    """
    Point d'entrée principal du script. Parse les arguments et lance l'extraction puis l'enregistrement des utilisateurs GitHub.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-users", type=int, default=30, help="Nombre d'utilisateurs à récupérer")
    args = parser.parse_args()

    print(f"🔍 Extraction de {args.max_users} utilisateurs depuis l'API GitHub...")
    utilisateurs = fetch_users(args.max_users)
    save_to_json(utilisateurs)
