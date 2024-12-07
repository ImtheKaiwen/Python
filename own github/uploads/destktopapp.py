import sys
import threading
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from app import app  # Flask uygulamanızın bulunduğu dosya

# Flask'ı arka planda çalıştırmak için bir fonksiyon
def run_flask():
    app.run(host='127.0.0.1', port=5000, use_reloader=False)  # Flask'ı başlat

# PyQt5 ile masaüstü uygulaması penceresi oluşturma
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notlar Uygulaması")
        self.setGeometry(100, 100, 1024, 768)
        
        # WebEngineView ile Flask sayfasını açıyoruz
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))
        
        # Layout ve pencere düzeni
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

# Flask'ı başlatacak ve ardından PyQt5 penceresini açacak kod
if __name__ == '__main__':
    # Flask'ı başlat
    threading.Thread(target=run_flask).start()

    # PyQt5 uygulaması başlat
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
