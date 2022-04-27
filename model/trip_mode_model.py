from enum import Enum, auto

class Trip_mode(Enum):
    walk=auto()
    drive=auto()
    cycle=auto()

if __name__=='__main__':
    print(Trip_mode.walk.name=='walk')