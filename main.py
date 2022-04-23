from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets 
from PyQt5 import QtWebChannel


from model.map_model import map_model
from model.optimal_path_model import Dijkstra_Algorithm



class HttpDaemon(QtCore.QThread):
    def run(self):
        HOST, PORT = '127.0.0.1', 8000
        self._server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        self._server.serve_forever()
        

    def stop(self):
        self.terminate()

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.campus_map=map_model()
        self.navigation=Dijkstra_Algorithm(self.campus_map)


        self.httpd = HttpDaemon(self)
        self.httpd.start()
        self.setGeometry(0, 0, 1920, 1000)

        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.page().profile().clearHttpCache()#清除缓存
        self.browser.load(QtCore.QUrl('http://localhost:8000/map.html'))
        self.setCentralWidget(self.browser)

        self.channel = QtWebChannel.QWebChannel()
        self.channel.registerObject('backend', self)
        self.browser.page().setWebChannel(self.channel)

        

    @QtCore.pyqtSlot(QtCore.QJsonValue,result=list)
    def foo(self,condition):
        self.campus_map=map_model()
        place_of_departure=condition["place_of_departure"].toInt()
        destination=condition["destination"].toInt()
        weather=condition["weather"].toString()
        cur_time=condition["cur_time"].toString()

        test=[[self.campus_map.place_data[self.campus_map.name_reflect[edge["place_A"]]]["position"],self.campus_map.place_data[self.campus_map.name_reflect[edge["place_B"]]]["position"]] for edge in self.campus_map.edge_data]
        return test

    def closeEvent(self, event):
        self.httpd.stop()
        self.close()

if __name__ == '__main__':

    app =QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())