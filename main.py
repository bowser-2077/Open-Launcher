import sys
from PySide6.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from ui.login import LoginPage
from ui.register import RegisterPage
from ui.store import StorePage
from ui.library import LibraryPage
from ui.upload import UploadPage
from ui.account import AccountPage

# --- Import Rich Presence ---
from services.discord_presence import DiscordPresence

DISCORD_CLIENT_ID = "1417596911195787426"


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # --- Initialiser la Rich Presence ---
        self.discord_rpc = DiscordPresence(DISCORD_CLIENT_ID)
        self.discord_rpc.connect()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Menu en haut
        self.menu = QWidget()
        self.menu_layout = QHBoxLayout(self.menu)
        self.menu_layout.setContentsMargins(3, 3, 3, 3)
        self.menu_layout.setSpacing(5)

        self.btn_store = QPushButton("Store")
        self.btn_library = QPushButton("Library")
        self.btn_upload = QPushButton("Upload")
        self.btn_account = QPushButton("Account")

        for btn, page in [(self.btn_store, "store"), (self.btn_library, "library"),
                          (self.btn_upload, "upload"), (self.btn_account, "account")]:
            btn.clicked.connect(lambda checked, p=page: self.navigate(p))
            self.menu_layout.addWidget(btn)

        self.layout.addWidget(self.menu)

        # QStackedWidget pour les pages
        self.pages = QStackedWidget()
        self.layout.addWidget(self.pages)

        # Initialisation des pages
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.store_page = StorePage(self)
        self.library_page = LibraryPage(self)
        self.upload_page = UploadPage(self)
        self.account_page = AccountPage(self)

        # Ajout des pages
        for page in [self.login_page, self.register_page, self.store_page,
                     self.library_page, self.upload_page, self.account_page]:
            self.pages.addWidget(page)

        self.setWindowTitle("Open Launcher")
        self.resize(1, 1)

        # Page de départ
        self.navigate("login")

    def navigate(self, page_name: str):
        mapping = {
            "login": self.login_page,
            "register": self.register_page,
            "store": self.store_page,
            "library": self.library_page,
            "upload": self.upload_page,
            "account": self.account_page
        }
        if page_name in mapping:
            self.pages.setCurrentWidget(mapping[page_name])

        # Cacher menu si login/register
        self.menu.setVisible(page_name not in ["login", "register"])

        # --- Mettre à jour Rich Presence ---
        if page_name == "login":
            self.discord_rpc.update(details="Écran de connexion", state="Se connecte au launcher")
        elif page_name == "register":
            self.discord_rpc.update(details="Écran d'inscription", state="Crée un compte")
        elif page_name == "store":
            self.discord_rpc.update(details="Sur la boutique", state="Explore des jeux")
        elif page_name == "library":
            self.discord_rpc.update(details="Dans sa bibliothèque", state="Regarde ses jeux")
        elif page_name == "upload":
            self.discord_rpc.update(details="Upload de jeu", state="Partage du contenu")
        elif page_name == "account":
            self.discord_rpc.update(details="Crée de grandes choses", state="Paramètres du profil")

    def closeEvent(self, event):
        # Nettoyage Rich Presence
        self.discord_rpc.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Appliquer le style global ---
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
