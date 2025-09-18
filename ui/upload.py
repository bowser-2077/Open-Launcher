from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt
from services.api import ApiService

class UploadPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("⬆️ Upload de jeu")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)



        # Nom du jeu
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du jeu")
        layout.addWidget(self.name_input)

        # Auteur
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Auteur")
        layout.addWidget(self.author_input)

        # URL zip
        self.zip_url_input = QLineEdit()
        self.zip_url_input.setPlaceholderText("URL directe du fichier .zip")
        layout.addWidget(self.zip_url_input)

        # URL description markdown (optionnel)
        self.md_url_input = QLineEdit()
        self.md_url_input.setPlaceholderText("URL directe du fichier description (.md) - optionnel")
        layout.addWidget(self.md_url_input)

        # URL cover
        self.png_url_input = QLineEdit()
        self.png_url_input.setPlaceholderText("URL directe de l'image cover (.png)")
        layout.addWidget(self.png_url_input)

        # Donations
        self.chk_donation = QCheckBox("Afficher bouton donations (Seuls les liens sont acceptés)")
        layout.addWidget(self.chk_donation)
        self.donation_link = QLineEdit()
        self.donation_link.setPlaceholderText("Lien Page Paypal/Buy Me A Coffe/Patreon")
        layout.addWidget(self.donation_link)

        # Bouton upload
        self.btn_upload = QPushButton("Uploader le jeu")
        self.btn_upload.clicked.connect(self.upload_game)
        layout.addWidget(self.btn_upload)

    def upload_game(self):
        name = self.name_input.text().strip()
        author = self.author_input.text().strip()
        zip_url = self.zip_url_input.text().strip()
        md_url = self.md_url_input.text().strip()
        png_url = self.png_url_input.text().strip()
        donation_enabled = self.chk_donation.isChecked()
        donation_link = self.donation_link.text().strip()

        # Validation
        if not all([name, author, zip_url, png_url]):
            QMessageBox.warning(self, "Erreur", "Nom, auteur, URL ZIP et URL cover sont obligatoires.")
            return
        if donation_enabled and not donation_link:
            QMessageBox.warning(self, "Erreur", "Merci de renseigner le lien PayPal si les dons sont activés.")
            return

        try:
            # On peut récupérer description depuis l'URL markdown si souhaité
            description = ""
            if md_url:
                import requests
                r = requests.get(md_url)
                if r.status_code == 200:
                    description = r.text

            # Ajouter entrée dans la table 'games'
            game_data = {
                "name": name,
                "author": author,
                "description": description,
                "image_url": png_url,
                "download_url": zip_url,
                "donation_enabled": donation_enabled,
                "donation_link": donation_link if donation_enabled else ""
            }
            ApiService.add_game(game_data)
            QMessageBox.information(self, "Succès", "Jeu uploadé avec succès ! \n Merci de ne pas publier de jeux cracks/virus. \n Les jeux -18 sont autorisés mais il est obligatoire \n de le présicer dans le titre \n du jeu")

            # Clear form
            self.name_input.clear()
            self.author_input.clear()
            self.zip_url_input.clear()
            self.md_url_input.clear()
            self.png_url_input.clear()
            self.chk_donation.setChecked(False)
            self.donation_link.clear()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Échec de l'upload : {e}")
