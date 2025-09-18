import time
from pypresence import Presence
import threading

class DiscordPresence:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.rpc = None
        self.connected = False

    def connect(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            print("[Discord] ✅ Rich Presence connecté")
        except Exception as e:
            print(f"[Discord] ❌ Erreur de connexion : {e}")

    def update(self, details: str = "Navigation", state: str = "Sur Open Launcher", large_image="icon", small_image=None):
        if not self.connected:
            return
        try:
            self.rpc.update(
                details=details,    # Exemple : "Sur la boutique"
                state=state,        # Exemple : "Découvre des jeux"
                large_image=large_image,
                small_image=small_image,
                start=time.time()
            )
        except Exception as e:
            print(f"[Discord] Erreur update : {e}")

    def close(self):
        if self.connected:
            try:
                self.rpc.clear()
                self.rpc.close()
                print("[Discord] 🔌 Rich Presence déconnecté")
            except:
                pass
