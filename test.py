
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication
import subprocess
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setGeometry(5, 30, 1355, 730)
        # self.browser = QWebEngineView()
        # 1 加载html代码\
        self.browser = QWebEngineView()
        # self.browser.loadFinished.connect(self._loadFinished)
        self.browser.load(QUrl.fromLocalFile(r'C:\Users\van\Desktop\map_path\test4.html'))
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    # os.system("python test3.py")
    # port=str(8000)
    # httpd = HTTPServer(("127.0.0.1", int(port)), SimpleHTTPRequestHandler)
    # print("Serving HTTP on localhost port " + port + " (http://localhost:" + port + "/) ...")
    # httpd.serve_forever()
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()
   
    sys.exit(app.exec())
    
