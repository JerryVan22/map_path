from enum import Enum, auto

class trip_mode(Enum):
    walk=auto()
    drive=auto()
    cycle=auto()

if __name__=='__main__':
    print(trip_mode.walk.name=='walk')