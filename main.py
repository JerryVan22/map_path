from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import datetime

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets 
from PyQt5 import QtWebChannel


from model.map_model import map_model
from model.optimal_path_model import Dijkstra_Algorithm
from model.trip_mode_model import Trip_mode
from model.weather_model import Weather


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
        # self.campus_map=map_model()
        place_of_departure=condition["place_of_departure"].toInt()
        destination=condition["destination"].toInt()
        trip_mode=Trip_mode[condition["trip_mode"].toString()]
        weather=Weather[condition["weather"].toString()]
        cur_time=datetime.datetime.strptime(condition["cur_time"].toString(), '%H:%M').time()
        test=self.navigation.solve(weather,trip_mode,cur_time,place_of_departure,destination)
        res=[]

        path_name=[]
        if test is not None:
            for i in range(len(test)):
                path_name.append(test[i]["name"])

            path_name="路径为: "+str.join(",",path_name)
            self.navigation.reason.append(path_name)

            for i in range(len(test)-1):
                res.append([test[i]["position"],test[i+1]["position"]])

        reason=str.join("\n",self.navigation.reason)
        res.append(reason)
        # test_2=[[self.campus_map.place_data[self.campus_map.name_reflect[edge["place_A"]]]["position"],self.campus_map.place_data[self.campus_map.name_reflect[edge["place_B"]]]["position"]] for edge in self.campus_map.edge_data]
        return res
    

    @QtCore.pyqtSlot(result=list)
    def draw_all_edges(self):
        return [[self.campus_map.place_data[self.campus_map.name_reflect[edge["place_A"]]]["position"],self.campus_map.place_data[self.campus_map.name_reflect[edge["place_B"]]]["position"]] for edge in self.campus_map.edge_data]


    def closeEvent(self, event):
        self.httpd.stop()
        self.close()

if __name__ == '__main__':

    app =QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())