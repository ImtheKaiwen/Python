import sys
import bcrypt
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                password TEXT,
                                first_name TEXT,
                                last_name TEXT,
                                profile_picture BLOB)''')
        self.conn.commit()

    def add_user(self, username, password, first_name, last_name, profile_picture=None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("INSERT INTO users (username, password, first_name, last_name, profile_picture) VALUES (?, ?, ?, ?, ?)",
                            (username, hashed_password, first_name, last_name, profile_picture))
        self.conn.commit()

    def verify_user(self, username, password):
        self.cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):  # password.encode() kısmı gerekli
                return True
        return False


    def get_user_data(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def update_user_data(self, username, first_name=None, last_name=None, profile_picture=None):
        if first_name:
            self.cursor.execute("UPDATE users SET first_name=? WHERE username=?", (first_name, username))
        if last_name:
            self.cursor.execute("UPDATE users SET last_name=? WHERE username=?", (last_name, username))
        if profile_picture:
            self.cursor.execute("UPDATE users SET profile_picture=? WHERE username=?", (profile_picture, username))
        self.conn.commit()

class MainMenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hoş Geldiniz")
        self.setGeometry(100, 100, 400, 200)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.login_button = QPushButton('Giriş Yap', self)
        self.login_button.clicked.connect(self.open_login_window)

        self.register_button = QPushButton('Kayıt Ol', self)
        self.register_button.clicked.connect(self.open_register_window)

        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(100, 100, 400, 400)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)

        self.form_layout.addRow('Kullanıcı Adı:', self.username_input)
        self.form_layout.addRow('Şifre:', self.password_input)
        self.form_layout.addRow('Ad:', self.first_name_input)
        self.form_layout.addRow('Soyad:', self.last_name_input)

        self.register_button = QPushButton('Kaydol', self)
        self.register_button.clicked.connect(self.register_user)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.register_button)
        
        self.setLayout(self.layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()

        if username and password and first_name and last_name:
            self.db.add_user(username, password, first_name, last_name)
            self.show_message("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
            LoginWindow()
        else:
            self.show_message("Lütfen tüm alanları doldurun.")

    def show_message(self, message):
        self.message_label = QLabel(message, self)
        self.layout.addWidget(self.message_label)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(100, 100, 400, 400)
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addRow('Kullanıcı Adı:', self.username_input)
        self.form_layout.addRow('Şifre:', self.password_input)
        
        self.login_button = QPushButton('Giriş Yap', self)
        self.login_button.clicked.connect(self.login_user)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.login_button)
        
        self.setLayout(self.layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if self.db.verify_user(username, password):
            self.open_profile_window(username)
        else:
            self.show_message("Geçersiz kullanıcı adı veya şifre!")

    def show_message(self, message):
        self.error_label = QLabel(message, self)
        self.layout.addWidget(self.error_label)

    def open_profile_window(self, username):
        self.profile_window = ProfileWindow(username)
        self.profile_window.show()
        self.close()

class ProfileWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Profil Bilgileri")
        self.setGeometry(100, 100, 400, 400)
        self.db = Database()
        self.username = username
        self.init_ui()

    def init_ui(self):
        user_data = self.db.get_user_data(self.username)

        self.layout = QVBoxLayout()
        self.first_name_input = QLineEdit(user_data[2], self)
        self.last_name_input = QLineEdit(user_data[3], self)

        self.layout.addWidget(QLabel(f'Kullanıcı Adı: {self.username}'))
        self.layout.addWidget(QLabel(f'Ad: {user_data[2]}'))
        self.layout.addWidget(QLabel(f'Soyad: {user_data[3]}'))

        self.profile_pic_label = QLabel(self)
        self.set_profile_picture(user_data[4])

        self.select_pic_button = QPushButton('Profil Resmi Seç', self)
        self.select_pic_button.clicked.connect(self.select_profile_picture)

        self.first_name_update_button = QPushButton('Adı Güncelle', self)
        self.first_name_update_button.clicked.connect(self.update_first_name)

        self.last_name_update_button = QPushButton('Soyadı Güncelle', self)
        self.last_name_update_button.clicked.connect(self.update_last_name)

        self.layout.addWidget(self.profile_pic_label)
        self.layout.addWidget(self.select_pic_button)
        self.layout.addWidget(self.first_name_update_button)
        self.layout.addWidget(self.last_name_update_button)

        self.setLayout(self.layout)

    def set_profile_picture(self, img_data):
        if img_data:
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            self.profile_pic_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        else:
            self.profile_pic_label.setText("Profil Resmi Yok")

    def select_profile_picture(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Tüm Dosyalar (*);;PNG Dosyaları (*.png);;JPEG Dosyaları (*.jpg *.jpeg)", options=options)
        if file_name:
            img = Image.open(file_name)
            img = img.convert('RGB')
            img.save(file_name)
            with open(file_name, 'rb') as file:
                img_data = file.read()
            self.db.update_user_data(self.username, profile_picture=img_data)
            self.set_profile_picture(img_data)

    def update_first_name(self):
        new_first_name = self.first_name_input.text()
        if new_first_name:
            self.db.update_user_data(self.username, first_name=new_first_name)

    def update_last_name(self):
        new_last_name = self.last_name_input.text()
        if new_last_name:
            self.db.update_user_data(self.username, last_name=new_last_name)

def main():
    app = QApplication(sys.argv)

    main_window = MainMenuWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
