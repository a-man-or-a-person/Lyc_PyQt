import PyQt6.QtWidgets as QT


class LoginWindow(QT.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        layout = QT.QVBoxLayout(self)

        self.username_label = QT.QLabel("Username:")
        self.username_input = QT.QLineEdit()
        self.password_label = QT.QLabel("Password:")
        self.password_input = QT.QLineEdit()
        self.password_input.setEchoMode(QT.QLineEdit.EchoMode.Password)

        self.login_btn = QT.QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "password":
            self.accepted_login.emit()
        else:
            self.username_input.clear()
            self.password_input.clear()
