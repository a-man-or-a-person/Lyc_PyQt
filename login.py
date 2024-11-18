import os
import Lyc_PyQt.UI.login_ui
from Lyc_PyQt.db_connection import db_conn_wrap

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import PyQt6.QtWidgets

class CreateAccountDialog(Lyc_PyQt.UI.login_ui.CreateAccountDialog):
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


class Login(Lyc_PyQt.UI.login_ui.LoginWindow):
    def __init__(self, parent):
        super().__init__()
        # self.conn = Lyc_PyQt.db_connection.connect_db()
        # cursor = self.conn.cursor()
        self.parent = parent
        self.login_btn.clicked.connect(self.check_login)
        self.account_create_btn.clicked.connect(self.create_account)

    @db_conn_wrap
    def create_account(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]
        dialog = CreateAccountDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username, password = dialog.get_credentials()
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Success", "Account created successfully!")

    @db_conn_wrap
    def check_login(self, *args, **kwargs):
        if not ("conn" in kwargs or "cursor" in kwargs):
            PyQt6.QtWidgets.QMessageBox.critical(
                self, "DB_conn_error", "DB was not provided or couldn't connect"
            )
        conn = kwargs["conn"]
        cursor = kwargs["cursor"]
        username = self.username_input.text()
        password = self.password_input.text()
        cursor.execute(f"SELECT password FROM Users WHERE username = '{username}'")
        pas = cursor.fetchone()[0]
        if pas and password == pas:
            cursor.execute(f'SELECT userid FROM Users WHERE username = "{username}"')
            os.environ["USER"] = str(cursor.fetchone()[0])
            self.parent.show_main_window()
        else:
            self.username_input.clear()
            self.password_input.clear()
