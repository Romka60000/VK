from SignInButton import SignInButton
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import vk

class OAuthWindow(QWidget):
    success_login = pyqtSignal()

    
    def __init__(self, VKAPI):
        super(OAuthWindow, self).__init__()
        self.VKAPI = VKAPI
        self.setFixedSize(320, 150)
        self.setWindowTitle("Authorization")
        self.setWindowIcon(QIcon("pics/TitleIcon.png"))
        self.setStyleSheet("background-color: white;")

        self.login_label = QLabel("Login:")
        self.login_edit = QLineEdit()
        self.login_edit.setFixedSize(170,25)

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedSize(170, 25)

        self.wrong_label = QLabel("Wrong login or password")
        self.wrong_label.hide()

        self.emty_label = QLabel("Emty login or password")
        self.emty_label.hide()

        self.sign_in = SignInButton("Sign in")
        self.sign_in.setFixedHeight(30)

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox1.addWidget(self.login_label)
        self.hbox1.addWidget(self.login_edit)

        self.hbox2.addWidget(self.password_label)
        self.hbox2.addWidget(self.password_edit)

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignHCenter)
        self.vbox.addItem(self.hbox1)
        self.vbox.addItem(self.hbox2)
        self.vbox.addWidget(self.emty_label)
        self.vbox.addWidget(self.wrong_label)
        self.vbox.addWidget(self.sign_in)
        self.setLayout(self.vbox)

        self.sign_in.clicked.connect(self.onClick)

        self.show()

    def onClick(self):
        if self.login_edit.text() == '' or self.password_edit.text() == '':
            self.emty_label.show()
        else:
            self.emty_label.hide()
            try:
                self.VKAPI.login(self.login_edit.text(), self.password_edit.text())
                self.success_login.emit()
                self.hide()
            except Exception:
                self.wrong_label.show()
