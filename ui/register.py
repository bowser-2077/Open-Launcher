from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from services.api import ApiService

class RegisterPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)

        title = QLabel("📝 Inscription")
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

        # Bouton s'inscrire
        self.btn_register = QPushButton("S'inscrire")
        self.btn_register.clicked.connect(self.register)
        layout.addWidget(self.btn_register)

        # Bouton retour login
        self.btn_login = QPushButton("Déjà un compte ? Se connecter")
        self.btn_login.clicked.connect(lambda: self.main_window.navigate("login"))
        layout.addWidget(self.btn_login)

    def register(self):
        pseudo = self.pseudo_input.text().strip()
        password = self.password_input.text().strip()

        if not pseudo or not password:
            QMessageBox.warning(self, "Erreur", "Merci de remplir tous les champs.")
            return

        success, message = ApiService.register(pseudo, password)
        if success:
            QMessageBox.information(self, "Succès", "Inscription réussie ! Tu peux maintenant te connecter.")
            self.main_window.navigate("login")
        else:
            QMessageBox.critical(self, "Erreur", f"Inscription échouée : {message}")
