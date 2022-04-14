
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets 
import sys




class HttpDaemon(QtCore.QThread):
    
    def run(self):
        HOST, PORT = '127.0.0.1', 8000
        self._server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        self._server.serve_forever()
        

    def stop(self):
        # self._server.shutdown()
        # self._server.socket.close()
        # self.wait()
        self.terminate()

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.httpd = HttpDaemon(self)
        self.httpd.start()
        self.setGeometry(0, 0, 1280, 720)

        self.browser = QtWebEngineWidgets.QWebEngineView()
        # self.browser.loadFinished.connect(self._loadFinished)
        self.browser.page().profile().clearHttpCache()
        self.browser.load(QtCore.QUrl('http://localhost:8000/test4.html'))

        self.setCentralWidget(self.browser)

    def closeEvent(self, event):
        self.httpd.stop()
        self.close()

if __name__ == '__main__':

    app =QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())