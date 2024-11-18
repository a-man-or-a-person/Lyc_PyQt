import os
import Lyc_PyQt.UI.login_ui
import Lyc_PyQt.db_connection


class Login(Lyc_PyQt.UI.login_ui.LoginWindow):
    def __init__(self, parent):
        super().__init__()
        self.conn = Lyc_PyQt.db_connection.connect_db()
        self.cur = self.conn.cursor()
        self.parent = parent
        self.login_btn.clicked.connect(self.check_login)

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
