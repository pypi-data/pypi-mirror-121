from husteblume import api
from husteblume.user import User


class Stations(object):
    @staticmethod
    def fetch():
        r = api('get', 'https://api.husteblume-app.de/locations?locationType=STATIONS')
        json = r.json()
        result = Stations(json=json)
        return result

    def __init__(self, json: dict):
        self.json = json

    def from_name(self, searchname: str) -> str:
        for station, name in self.json.items():
            if name.lower() == searchname.lower():
                return station

    def from_station(self, searchstation: str) -> str:
        for station, name in self.json.items():
            if station.lower() == searchstation.lower():
                return name


class Regions(object):
    @staticmethod
    def fetch():
        r = api('get', 'https://api.husteblume-app.de/locations?locationType=REGIONS')
        json = r.json()
        result = Regions(json=json)
        return result

    def __init__(self, json: dict):
        self.json = json

    def from_name(self, searchname: str) -> str:
        for station, name in self.json.items():
            if name.lower() == searchname.lower():
                return station

    def from_region(self, searchregion: str) -> str:
        for station, name in self.json.items():
            if station.lower() == searchregion.lower():
                return name


class Forecast(object):
    @staticmethod
    def get(station: str, user: User):
        r = api('get', 'https://api.husteblume-app.de/forecast/' + station, user=user)

        f = Forecast(r.json())
        return f

    def __init__(self, json: dict):
        self.json = json
