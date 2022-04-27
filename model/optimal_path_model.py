try:
    from model.trip_mode_model import Trip_mode
    from model.weather_model import Weather
    from model.map_model import map_model
except ModuleNotFoundError:
    from trip_mode_model import Trip_mode
    from weather_model import Weather
    from map_model import map_model

from datetime import time
from copy import deepcopy


class Dijkstra_Algorithm():
    def __init__(self, map_data: map_model) -> None:
        self.map_data = map_data
        self.reason=[]
        self.reason_edge=set()
        self.busy_times = ((time(hour=7, minute=50), time(hour=8, minute=20)),
                           (time(hour=11, minute=40),time(hour=12, minute=10)), 
                           (time(hour=17,minute=10),time(hour=17,minute=40)))


    def solve(self, weather:Weather, trip_mode:Trip_mode, cur_time:time, place_of_departure:int,destination:int):
        self.reason=[]
        self.reason_edge=set()
        if place_of_departure==destination:
            self.reason.append("起点和终点一致,无需求解")
            return None

        unreachable = 10000
        
        if weather==Weather.rain or weather==Weather.snow:
            if weather==Weather.rain:
                self.reason.append("天气为雨,切换为驾驶模式")
            else:
                self.reason.append("天气为雪,切换为驾驶模式")
            trip_mode=Trip_mode.drive


        if (trip_mode == Trip_mode.drive or trip_mode==Trip_mode.cycle):
            self.reason.append("将寻找最近停车点")
            points=self.map_data.park_points if trip_mode == Trip_mode.drive else self.map_data.bicycle_park_points

            navigation_path_from_departure = []
            navigation_path_from_departure_distance = unreachable
            for point in points:
                navigation_path, path_distance = self.abstract_solve( weather,trip_mode,cur_time,place_of_departure, point)
                if path_distance < navigation_path_from_departure_distance:
                    navigation_path_from_departure=navigation_path
                    navigation_path_from_departure_distance=path_distance

            navigation_path_to_destination=[]
            navigation_path_to_destination_distance=unreachable
            for point in points:
                navigation_path, path_distance = self.abstract_solve( weather,trip_mode,cur_time,destination, point)
                if path_distance < navigation_path_to_destination_distance:
                    navigation_path_to_destination=navigation_path
                    navigation_path_to_destination_distance=path_distance
            
            mid_path,_=self.abstract_solve( weather,trip_mode,cur_time,
                                            place_of_departure=self.map_data.id_reflect[navigation_path_from_departure[-1]["id"]],
                                            destination=self.map_data.id_reflect[navigation_path_to_destination[-1]["id"]])

            return navigation_path_from_departure[:-1]+mid_path+navigation_path_to_destination[-2::-1]

            
        else:
            path,_=self.abstract_solve(weather,trip_mode,cur_time,place_of_departure,destination)
            return path

    def abstract_solve(self, weather:Weather, trip_mode:Trip_mode, cur_time:time, place_of_departure:int,destination:int):
        unreachable = 10000
        place_of_departure_index = place_of_departure
        destination_index = destination

        point_distance = [unreachable for i in range(len(self.map_data.place_data))]
        point_distance[place_of_departure_index] = 0
        # for edge in self.map_data.edges[place_of_departure_index]:
        #     point_distance[edge[0]] = edge[1]

        path = [[] for i in range(len(self.map_data.place_data))]
        path[place_of_departure_index] = [place_of_departure_index]
        visit = set()
        not_visit = set([i for i in range(len(self.map_data.place_data))])
        last_visit = place_of_departure_index


        while last_visit != destination_index:
            not_visit.remove(last_visit)
            visit.add(last_visit)

            for edge in self.map_data.edges[last_visit]:
                changed_edge_value=self.changed_edge_value(trip_mode=trip_mode,edge=(last_visit,edge[0]),cur_time=cur_time,edge_value=edge[1])
                if point_distance[edge[0]] > point_distance[last_visit] + changed_edge_value:
                    point_distance[edge[0]] = point_distance[last_visit] + changed_edge_value
                    path[edge[0]] = deepcopy(path[last_visit])
                    path[edge[0]].append(edge[0])

            min_dst = unreachable

            for place_index in not_visit:
                if min_dst > point_distance[place_index]:
                    min_dst = point_distance[place_index]
                    last_visit = place_index

        return [self.map_data.place_data[i] for i in path[destination_index]], point_distance[destination]

    def cur_time_is_busy(self, cur_time: time):
        for busy_time in self.busy_times:
            if busy_time[0] <= cur_time and cur_time <= busy_time[1]:
                return True
        return False

    def changed_edge_value(self,trip_mode:Trip_mode,edge:tuple,cur_time:time,edge_value:int):
        if trip_mode==Trip_mode.cycle or trip_mode==Trip_mode.drive:
            if self.cur_time_is_busy(cur_time) :
                if edge in self.map_data.possible_busy_edges:
                    if edge not in self.reason_edge :
                        self.reason_edge.add(edge)
                        self.reason_edge.add((edge[1],edge[0]))
                        self.reason.append("路径 {} 到 {} 在 {} 时刻人流量大,请尽量避免,".format(self.map_data.place_data[edge[0]]["name"],self.map_data.place_data[edge[1]]["name"],cur_time.__str__()))
                    return edge_value*6
        
        return edge_value




if __name__ == '__main__':
    demo = Dijkstra_Algorithm(map_model())
    path = demo.solve(weather=Weather.cloudy,
                      cur_time=time(hour=0,minute=10),
                      trip_mode=Trip_mode.cycle,
                      place_of_departure=0,
                      destination=1)
    for edge in path:
        print(edge)
