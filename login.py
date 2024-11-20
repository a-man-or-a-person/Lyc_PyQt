import os
import UI.login_ui
import db_connection

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class CreateAccountDialog(UI.login_ui.CreateAccountDialog):
    def __init__(self):
        super().__init__()
        self.create_btn.clicked.connect(self.create_account)
        self.cancel_btn.clicked.connect(self.reject)


    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        if username and password:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields!")


    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()


class Login(UI.login_ui.LoginWindow):
    def __init__(self, parent):
        super().__init__()
        self.conn = db_connection.connect_db()
        self.cur = self.conn.cursor()
        self.parent = parent
        self.login_btn.clicked.connect(self.check_login)
        self.account_create_btn.clicked.connect(self.create_account)

    def create_account(self):
        dialog = CreateAccountDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password = dialog.get_credentials()
            self.cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Account created successfully!")

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.cur.execute(f"SELECT password FROM Users WHERE username = '{username}'")
        pas = self.cur.fetchone()[0]
        if pas and password == pas:
            self.cur.execute(f'SELECT userid FROM Users WHERE username = "{username}"')
            os.environ["USER"] = str(self.cur.fetchone()[0])
            self.parent.show_main_window()
        else:
            self.username_input.clear()
            self.password_input.clear()
