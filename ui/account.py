from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from services.api import ApiService


class AccountPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("👤 Mon compte")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Pseudo
        self.pseudo_input = QLineEdit()
        self.pseudo_input.setPlaceholderText("Pseudo")
        layout.addWidget(self.pseudo_input)

        # Mot de passe (changement)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nouveau mot de passe (laisser vide pour ne pas changer)")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Bouton sauvegarder
        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.save_changes)
        layout.addWidget(self.btn_save)

        # Charger les infos actuelles
        self.load_account_info()

    def load_account_info(self):
        """Charge les infos utilisateur depuis l'API"""
        try:
            user = ApiService.get_current_user()
            if user:
                self.pseudo_input.setText(user.get("pseudo", ""))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le compte : {e}")

    def save_changes(self):
        pseudo = self.pseudo_input.text().strip()
        password = self.password_input.text().strip() or None

        if not pseudo:
            QMessageBox.warning(self, "Erreur", "Le pseudo ne peut pas être vide.")
            return

        try:
            success, msg = ApiService.update_user(pseudo=pseudo, password=password)
            if success:
                QMessageBox.information(self, "Succès", "Compte mis à jour avec succès.")
                self.password_input.clear()
            else:
                QMessageBox.critical(self, "Erreur", msg)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer : {e}")
