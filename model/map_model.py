# coding=utf-8
import json

class map_model():
    def __init__(self) -> None:
        self.place_data=None
        self.id_reflect=None
        self.name_reflect=None
        self.bicycle_park_points=None
        self.park_points=None
        self.read_points()
            
        self.edge_data=None
        self.possible_busy_edges=set()
        self.edges=[ [] for i in range(len(self.place_data))]
        self.read_edges()


        
        # test=[[self.place_data[self.name_reflect[edge["place_A"]]]["position"],self.place_data[self.name_reflect[edge["place_B"]]]["position"]]  for edge in self.edge_data]
        # print(test)

    def read_points(self):
        with open(file='./data/place.json', mode='r',encoding='utf-8') as f:
            self.place_data=json.load(f)
            self.id_reflect=dict([(self.place_data[i]["id"],i) for i in range(len(self.place_data))])
            self.name_reflect=dict([(self.place_data[i]["name"],i) for i in range(len(self.place_data))])
            self.bicycle_park_points=[i for i in range(len(self.place_data)) if self.place_data[i]["type"]=="bicycle park"]
            self.park_points=[i for i in range(len(self.place_data)) if self.place_data[i]["type"]=="park"]
        
    def read_edges(self):
            with open(file='./data/edge.json', mode='r',encoding='utf-8') as f:
                self.edge_data=json.load(f)
            
                for edge in self.edge_data:
                    
                    id_a=self.name_reflect[edge["place_A"]]
                    id_b=self.name_reflect[edge["place_B"]]
                
                    self.edges[id_a].append([id_b,edge["distance"]])
                    self.edges[id_b].append([id_a,edge["distance"]])

                    if edge["type"]=="possible busy":
                        self.possible_busy_edges.add((id_a,id_b))
                        self.possible_busy_edges.add((id_b,id_a))
                pass



if __name__=='__main__':
    test=map_model()