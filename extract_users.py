import requests
import os
import time
import argparse
import json
from dotenv import load_dotenv
import sys
import io

# Encodage UTF-8 pour éviter les erreurs d'affichage
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Charger les variables d'environnement (.env)
load_dotenv()
token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

# Vérifie les quotas API et met en pause si nécessaire
def check_rate_limit(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

    if remaining == 0:
        wait_time = reset_time - int(time.time())
        if wait_time > 0:
            print(f"[Quota] Limite atteinte. Pause de {wait_time} secondes (~{wait_time // 60} min).")
            time.sleep(wait_time + 1)

# Fonction de requête HTTP sécurisée avec gestion des erreurs
def safe_request(url, max_retries=5):
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

# Fonction principale pour extraire les utilisateurs
def fetch_users(max_users):
    users_data = []
    since = 0

    while len(users_data) < max_users:
        url = f"https://api.github.com/users?since={since}"
        response = safe_request(url)

        if response is None:
            break

        users = response.json()
        if not users:
            break

        for user in users:
            login = user['login']
            detail_url = f"https://api.github.com/users/{login}"
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

# Fonction d'enregistrement JSON
def save_to_json(data, path="data/users.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Données enregistrées dans {path}")

# Point d'entrée du script
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-users", type=int, default=30, help="Nombre d'utilisateurs à récupérer")
    args = parser.parse_args()

    print(f"🔍 Extraction de {args.max_users} utilisateurs depuis l'API GitHub...")
    utilisateurs = fetch_users(args.max_users)
    save_to_json(utilisateurs)
