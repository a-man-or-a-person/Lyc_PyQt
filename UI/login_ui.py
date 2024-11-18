import PyQt6.QtWidgets as QT


class LoginWindow(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        layout = QT.QVBoxLayout(self)
        self.btn_layout = QT.QHBoxLayout(self)

        self.username_label = QT.QLabel("Username:")
        self.username_input = QT.QLineEdit()
        self.password_label = QT.QLabel("Password:")
        self.password_input = QT.QLineEdit()
        self.password_input.setEchoMode(QT.QLineEdit.EchoMode.Password)

        self.login_btn = QT.QPushButton("Login")
        self.account_create_btn = QT.QPushButton("Create Account")

        self.btn_layout.addWidget(self.login_btn)
        self.btn_layout.addWidget(self.account_create_btn)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addLayout(self.btn_layout)


class CreateAccountDialog(QT.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Account")

        self.layout = QT.QVBoxLayout(self)

        # Username
        self.username_label = QT.QLabel("Username:")
        self.username_input = QT.QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        # Password
        self.password_label = QT.QLabel("Password:")
        self.password_input = QT.QLineEdit()
        self.password_input.setEchoMode(QT.QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        # Confirm Password
        self.confirm_password_label = QT.QLabel("Confirm Password:")
        self.confirm_password_input = QT.QLineEdit()
        self.confirm_password_input.setEchoMode(QT.QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.confirm_password_label)
        self.layout.addWidget(self.confirm_password_input)

        # Buttons
        self.button_layout = QT.QHBoxLayout()
        self.create_btn = QT.QPushButton("Create")
        self.cancel_btn = QT.QPushButton("Cancel")
        self.button_layout.addWidget(self.create_btn)
        self.button_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(self.button_layout)
