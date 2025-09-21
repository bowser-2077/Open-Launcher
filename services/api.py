import bcrypt
import os
from supabase import create_client

SUPABASE_URL = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SUPABASE_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

LIBRARY_PATH = "library"

class ApiService:

    session_user = None

    # ----------------- Inscription -----------------
    @classmethod
    def register(cls, pseudo, password):
        # Vérifie si le pseudo existe déjà
        res = supabase.table("users").select("*").eq("pseudo", pseudo).execute()
        if res.data:
            return False, "Pseudo déjà utilisé"

        # Hash du mot de passe
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Création de l'utilisateur
        supabase.table("users").insert({
            "pseudo": pseudo,
            "password_hash": pw_hash
        }).execute()
        return True, ""

    # ----------------- Login -----------------
    @classmethod
    def login(cls, pseudo, password):
        res = supabase.table("users").select("*").eq("pseudo", pseudo).execute()
        if not res.data:
            return False, "Pseudo inconnu"

        user = res.data[0]
        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            cls.session_user = user
            return True, ""
        return False, "Mot de passe incorrect"

    # ----------------- Jeux -----------------
    @classmethod
    def fetch_games(cls):
        res = supabase.table("games").select("*").execute()
        return res.data if res.data else []

    @classmethod
    def upload_file(cls, local_path, bucket_name):
        filename = os.path.basename(local_path)
        with open(local_path, "rb") as f:
            supabase.storage.from_(bucket_name).upload(filename, f, {"cacheControl": "3600", "upsert": True})
        return supabase.storage.from_(bucket_name).get_public_url(filename)

    @classmethod
    def add_game(cls, game_data):
        supabase.table("games").insert(game_data).execute()

