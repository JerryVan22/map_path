from enum import Enum, auto
class Weather(Enum):
    sunny=auto()
    cloudy=auto()
    rain=auto()

if __name__=='__main__':
    print(Weather.sunny.name=="cloudy")