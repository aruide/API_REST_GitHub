import json
import os
from datetime import datetime, timezone

# Chargement des utilisateurs depuis le fichier JSON
def load_users(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        users = json.load(f)

    # Vérification de la structure
    required_keys = {"login", "id", "created_at", "avatar_url", "bio"}
    cleaned = []
    for user in users:
        if isinstance(user, dict) and required_keys.issubset(user):
            cleaned.append(user)
        else:
            print(f"[⚠️  Ignoré] Structure invalide : {user}")
    return cleaned

# Suppression des doublons par ID
def remove_duplicates(users):
    unique_users = {}
    for user in users:
        unique_users[user["id"]] = user
    return list(unique_users.values()), len(users) - len(unique_users)

# Filtrage métier
def filter_users(users):
    filtered = []
    date_min = datetime(2008, 1, 1, tzinfo=timezone.utc)

    for user in users:
        bio = user.get("bio")
        avatar_url = user.get("avatar_url", "").strip()
        created_at_str = user.get("created_at", "")
        try:
            created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        except ValueError:
            continue

        if bio and avatar_url and created_at > date_min:
            filtered.append({
                "login": user["login"],
                "id": user["id"],
                "created_at": user["created_at"],
                "avatar_url": user["avatar_url"],
                "bio": user["bio"]
            })

    return filtered

# Sauvegarde des utilisateurs filtrés
def save_filtered_users(users, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# Script principal
if __name__ == "__main__":
    input_file = "data/users.json"
    output_file = "data/filtered_users.json"

    all_users = load_users(input_file)
    initial_count = len(all_users)

    deduped_users, nb_doublons = remove_duplicates(all_users)
    filtered_users = filter_users(deduped_users)

    save_filtered_users(filtered_users, output_file)

    print("\n✅ Résumé du traitement :")
    print(f"Utilisateurs chargés   : {initial_count}")
    print(f"Doublons supprimés     : {nb_doublons}")
    print(f"Utilisateurs filtrés   : {len(filtered_users)}")
