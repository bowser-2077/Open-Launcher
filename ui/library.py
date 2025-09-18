from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os, requests, subprocess, zipfile, shutil, sys, platform
from services.api import ApiService

LIBRARY_PATH = "library"

class LibraryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("📚 Ma Bibliothèque")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.vbox = QVBoxLayout(self.container)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # Charger jeux
        self.load_library()

    def load_library(self):
        self.vbox.setAlignment(Qt.AlignTop)
        if not os.path.exists(LIBRARY_PATH):
            os.makedirs(LIBRARY_PATH)

        for folder in os.listdir(LIBRARY_PATH):
            game_folder = os.path.join(LIBRARY_PATH, folder)
            meta_file = os.path.join(game_folder, "meta.txt")
            if not os.path.isdir(game_folder) or not os.path.exists(meta_file):
                continue

            with open(meta_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                name = lines[0].strip()
                author = lines[1].strip()
                image_url = lines[2].strip()
                exe_path = os.path.join(game_folder, "extracted")

            frame = QFrame()
            frame.setStyleSheet("border: 1px solid #444; padding: 10px; margin: 5px;")
            hbox = QHBoxLayout(frame)

            # Cover
            try:
                img_data = requests.get(image_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                cover = QLabel()
                cover.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                hbox.addWidget(cover)
            except:
                hbox.addWidget(QLabel("[Image indisponible]"))

            # Infos + bouton lancer
            info_box = QVBoxLayout()
            lbl_name = QLabel(f"{name} - par {author}")
            lbl_name.setStyleSheet("font-size: 18px; font-weight: bold;")
            btn_launch = QPushButton("▶ Lancer")
            btn_launch.clicked.connect(lambda _, p=exe_path: self.launch_game(p))

            info_box.addWidget(lbl_name)
            info_box.addWidget(btn_launch)

            hbox.addLayout(info_box)
            self.vbox.addWidget(frame)

    def launch_game(self, path):
        """Lance le jeu depuis son dossier extrait"""
        if not os.path.exists(path):
            print("Erreur: dossier du jeu introuvable.")
            return

        # Cherche un exécutable
        exe = None
        for f in os.listdir(path):
            if f.endswith(".exe") or f.endswith(".py"):
                exe = os.path.join(path, f)
                break

        if exe:
            if exe.endswith(".exe"):
                subprocess.Popen([exe], cwd=path)
            elif exe.endswith(".py"):
                if platform.system() == "Windows":
                    subprocess.Popen(["python", exe], cwd=path, shell=True)
                else:
                    subprocess.Popen(["python3", exe], cwd=path)
        else:
            print("Aucun exécutable trouvé dans ce jeu.")
