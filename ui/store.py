from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QFrame, QMessageBox, QProgressDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import requests, os, zipfile, webbrowser
from services.api import ApiService
from services.downloader import DownloadThread  # Thread async
import json

LIBRARY_PATH = "library"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1417872503610544340/vOiA9KRXRE9UvLIagRjwdu2EpeuOB3_XihP8MIOfDP40p84ct1pxhWmOPUoeRQ8Ao45r"  # 🔴 Mets ton webhook ici


class StorePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("🎮 Store")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # ScrollArea pour la liste des jeux
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)

        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # Charger les jeux
        self.load_games()

    def load_games(self):
        self.vbox.setAlignment(Qt.AlignTop)

        games = ApiService.fetch_games()
        if not games:
            self.vbox.addWidget(QLabel("Aucun jeu disponible."))
            return

        for game in games:
            frame = QFrame()
            frame.setStyleSheet("border: 1px solid #444; padding: 10px; margin: 5px;")
            hbox = QHBoxLayout(frame)

            # Image du jeu
            if game.get("image_url"):
                try:
                    img_data = requests.get(game["image_url"]).content
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_data)
                    cover = QLabel()
                    cover.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    hbox.addWidget(cover)
                except Exception as e:
                    print(f"Erreur chargement image: {e}")
                    hbox.addWidget(QLabel("[Image indisponible]"))

            # Infos du jeu
            info_box = QVBoxLayout()
            name = QLabel(f"{game['name']} - par {game['author']}")
            name.setStyleSheet("font-size: 18px; font-weight: bold;")
            desc = QLabel(game.get("description", ""))
            desc.setWordWrap(True)

            # Boutons
            btn_download = QPushButton("📥 Télécharger")
            btn_download.clicked.connect(lambda _, g=game: self.download_game(g))

            btn_report = QPushButton("⚠️ Signaler")
            btn_report.clicked.connect(lambda _, g=game: self.report_game(g))

            info_box.addWidget(name)
            info_box.addWidget(desc)
            info_box.addWidget(btn_download)
            info_box.addWidget(btn_report)

            # Bouton donation si activé
            if game.get("donation_enabled"):
                btn_donate = QPushButton("💖 Faire un don")
                btn_donate.clicked.connect(lambda _, g=game: self.open_donation(g))
                info_box.addWidget(btn_donate)

            hbox.addLayout(info_box)
            self.vbox.addWidget(frame)

    # --- DOWNLOAD THREAD ---
    def download_game(self, game):
        save_path = os.path.join("downloads", game["name"] + ".zip")
        os.makedirs("downloads", exist_ok=True)

        self.progress = QProgressDialog("Téléchargement en cours...", "Annuler", 0, 100, self)
        self.progress.setWindowTitle("Téléchargement")
        self.progress.setValue(0)
        self.progress.show()

        self.thread = DownloadThread(game["download_url"], save_path)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(lambda path: self.download_finished(path, game))
        self.thread.error.connect(lambda msg: QMessageBox.critical(self, "Erreur", msg))
        self.thread.start()

    def download_finished(self, path, game):
        # Extraire directement après téléchargement
        game_folder = os.path.join(LIBRARY_PATH, game["id"])
        os.makedirs(game_folder, exist_ok=True)

        extract_path = os.path.join(game_folder, "extracted")
        os.makedirs(extract_path, exist_ok=True)

        try:
            with zipfile.ZipFile(path, "r") as zf:
                zf.extractall(extract_path)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d’extraire le jeu: {e}")
            return

        with open(os.path.join(game_folder, "meta.txt"), "w", encoding="utf-8") as f:
            f.write(game["name"] + "\n")
            f.write(game["author"] + "\n")
            f.write(game.get("image_url", "") + "\n")

        QMessageBox.information(self, "Succès", f"✅ Jeu {game['name']} installé dans la bibliothèque.")
        self.progress.close()

    # --- DONATION ---
    def open_donation(self, game):
        if game.get("donation_link"):
            webbrowser.open(game["donation_link"])

    # --- REPORT WEBHOOK ---
    def report_game(self, game):
        data = {
            "content": f"⚠️ Un utilisateur a signalé le jeu **{game['name']}** (par {game['author']})."
        }
        try:
            r = requests.post(DISCORD_WEBHOOK, json=data, headers={"Content-Type": "application/json"})
            if r.status_code == 204:
                QMessageBox.information(self, "Signalement", f"Le jeu {game['name']} a été signalé avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", f"Impossible d’envoyer le signalement (code {r.status_code})")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l’envoi du signalement : {e}")
