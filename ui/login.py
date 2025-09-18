from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from services.api import ApiService

class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("🔑 Connexion")
        title.setAlignment(Qt.AlignCenter)
        title.setProperty("class", "pageTitle")  # <<< pour le QSS
        layout.addWidget(title)

        # Pseudo
        self.pseudo_input = QLineEdit()
        self.pseudo_input.setPlaceholderText("Pseudo")
        layout.addWidget(self.pseudo_input)

        # Mot de passe
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Bouton se connecter
        self.btn_login = QPushButton("Se connecter")
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

        # Bouton vers inscription
        self.btn_register = QPushButton("Pas de compte ? S'inscrire")
        self.btn_register.clicked.connect(lambda: self.main_window.navigate("register"))
        layout.addWidget(self.btn_register)

    def login(self):
        pseudo = self.pseudo_input.text().strip()
        password = self.password_input.text().strip()

        if not pseudo or not password:
            QMessageBox.warning(self, "Erreur", "Merci de remplir tous les champs.")
            return

        success, message = ApiService.login(pseudo, password)
        if success:
            QMessageBox.information(self, "Succès", f"Bienvenue {pseudo} !")
            self.main_window.navigate("store")
        else:
            QMessageBox.critical(self, "Erreur", f"Connexion échouée : {message}")
