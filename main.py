
from http.server import HTTPServer, SimpleHTTPRequestHandler

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets 
from PyQt5 import QtWebChannel
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
        self.browser.page().profile().clearHttpCache()#清除缓存
        self.browser.load(QtCore.QUrl('http://localhost:8000/test4.html'))
        self.setCentralWidget(self.browser)

        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject('backend', self)
        self.browser.page().setWebChannel(self.channel)

    @QtCore.pyqtSlot(QtCore.QJsonValue,result=list)
    def foo(self,condition):
        place_of_departure=condition["place_of_departure"].toInt()
        destination=condition["destination"].toInt()
        weather=condition["weather"].toString()

        print('bar')
        return [[31.768709, 117.189064],[31.765925, 117.185512],[31.755925, 117.185512]]

    def closeEvent(self, event):
        self.httpd.stop()
        self.close()

if __name__ == '__main__':

    app =QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())